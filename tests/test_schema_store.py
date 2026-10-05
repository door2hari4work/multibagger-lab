from datetime import date
import pytest
from mblab.schema import Thesis, Evidence, Scenario, ExitTrigger, AdversarialReview, EntryPlan, Status, EntryState, validate
from mblab import store


def good_entry_thesis():
    return Thesis(ticker="ABC", company="ABC Ltd", market="IN", research_level=5, status=Status.ATTRACTIVE_ENTRY.value,
                  entry=EntryPlan(state=EntryState.ATTRACTIVE_ENTRY.value, ideal_zone=[820, 880], invalidation_price=700),
                  exit_rules=[ExitTrigger(type="thesis_invalidation", condition="order book falls below Rs X")],
                  adversarial=AdversarialReview(done=True, verdict="survives", reviewer="devils_advocate"),
                  evidence=[Evidence(id="e1", claim="Revenue up 40% YoY", kind="FACT", source_type="filing", source_url="https://x/y", source_date="2026-09-20")])


def test_entry_call_valid_when_rules_met():
    assert validate(good_entry_thesis(), today=date(2026, 10, 5)) == []


def test_entry_call_blocked_without_adversarial_review_or_low_level_or_stale():
    t = good_entry_thesis(); t.adversarial = AdversarialReview(); assert any("adversarial" in p for p in validate(t, today=date(2026, 10, 5)))
    t = good_entry_thesis(); t.research_level = 2; assert any("research_level" in p for p in validate(t, today=date(2026, 10, 5)))
    t = good_entry_thesis(); assert any("newer than" in p for p in validate(t, today=date(2027, 6, 1)))


def test_fact_needs_source_and_certainty_language_banned():
    t = Thesis(ticker="A", company="A", market="US", evidence=[Evidence(id="e", claim="x", kind="FACT")]); assert any("FACT needs" in p for p in validate(t))
    t = Thesis(ticker="A", company="A", market="US", thesis="This will become a multibagger"); assert any("certainty" in p for p in validate(t))
    t = Thesis(ticker="A", company="A", market="US", bull_case=Scenario("bull", "x", probability=0.4, probability_is_model_estimate=False)); assert any("model estimates" in p for p in validate(t))


def test_store_versions_are_append_only_and_changelog(tmp_path):
    t = Thesis(ticker="XYZ", company="XYZ", market="US", thesis="v1 idea"); store.save_new_version(t, base=tmp_path)
    t2 = store.load("US", "XYZ", base=tmp_path); t2.thesis = "v2 idea"; t2.research_level = 2; store.save_new_version(t2, reason="new filing", base=tmp_path)
    assert store.versions("US", "XYZ", base=tmp_path) == [1, 2]
    assert store.load("US", "XYZ", 1, base=tmp_path).thesis == "v1 idea"            # history untouched
    l = store.load("US", "XYZ", base=tmp_path); assert l.version == 2 and l.parent_version == 1 and l.change_log[0] == "new filing" and any("research_level" in c for c in l.change_log)


def test_invalid_thesis_is_rejected(tmp_path):
    with pytest.raises(store.ThesisInvalid): store.save_new_version(Thesis(ticker="Q", company="Q", market="US", thesis="guaranteed winner"), base=tmp_path)


def test_roundtrip():
    t = good_entry_thesis(); assert Thesis.from_dict(t.to_dict()).to_dict() == t.to_dict()
