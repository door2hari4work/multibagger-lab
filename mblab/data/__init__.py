"""Data layer: universe lists, cached prices with reliability checks, fundamentals."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / "data" / "cache"
RAW_DIR = ROOT / "data" / "raw"
PIT_DIR = ROOT / "data" / "pit"
