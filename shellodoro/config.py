import os
from pathlib import Path


DATA_DIR = Path(
    os.getenv("XDG_DATA_HOME")
    or Path(os.getenv("HOME")) / ".local" / "share" / "shellodoro"
)

MODES_FILE = DATA_DIR / "modes.json"
STATS_FILE = DATA_DIR / "stats.json"
