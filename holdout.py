"""Guard for the untouched 2019-2026 test set.

Any code that loads data after TUNE_END must go through `load_range`. The first
test-set read writes a lock file; a second read raises unless the lock is removed
deliberately (which should be recorded in reports/DEVIATIONS.md).
"""
from datetime import date
import json
from pathlib import Path
import config

LOCK = config.ROOT / "results" / "test" / ".test_used.lock"


class HoldoutViolation(RuntimeError):
    pass


def load_range(start: date, end: date, *, purpose: str, final_run: bool = False):
    """Validate a requested date range. Returns (start, end) if allowed."""
    touches_test = end > config.TUNE_END
    if not touches_test:
        return start, end
    if start <= config.TUNE_END:
        raise HoldoutViolation("Range straddles tune/test boundary; split it.")
    if not final_run:
        raise HoldoutViolation("Test-set access requires final_run=True (one-shot).")
    if LOCK.exists():
        raise HoldoutViolation(f"Test set already used: {LOCK.read_text()}")
    LOCK.write_text(json.dumps({"purpose": purpose, "at": date.today().isoformat()}))
    return start, end
