from datetime import date
import pytest
import config, holdout


def test_tune_range_ok():
    holdout.load_range(date(2010, 1, 1), date(2018, 12, 31), purpose="tune")


def test_test_range_needs_final_flag():
    with pytest.raises(holdout.HoldoutViolation):
        holdout.load_range(date(2019, 1, 1), date(2026, 9, 30), purpose="peek")


def test_straddle_rejected():
    with pytest.raises(holdout.HoldoutViolation):
        holdout.load_range(date(2018, 1, 1), date(2020, 1, 1), purpose="x", final_run=True)


def test_test_set_one_shot(tmp_path, monkeypatch):
    monkeypatch.setattr(holdout, "LOCK", tmp_path / "lock")
    holdout.load_range(date(2019, 1, 1), date(2026, 9, 30), purpose="final", final_run=True)
    with pytest.raises(holdout.HoldoutViolation):
        holdout.load_range(date(2019, 1, 1), date(2026, 9, 30), purpose="again", final_run=True)
