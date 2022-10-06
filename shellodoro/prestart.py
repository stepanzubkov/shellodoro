from .config import DATA_DIR, MODES_FILE, STATS_FILE


def create_user_files():
    """Creates user files (stats, modes) in XDG_DATA_HOME
    ($HOME/.local/share/shellodoro/ by default)"""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
    if not MODES_FILE.is_file():
        create_modes_file()
    if not STATS_FILE.is_file():
        create_stats_file()


def create_modes_file():
    """Create modes file and write basic modes to it"""
    with MODES_FILE.open("w") as modes:
        modes.write(
            """
{
    "default": {
        "work_time": 20,
        "break_time": 5,
        "long_break_time": 15,
        "long_break_freq": 4
    },
    "52/17": {
        "work_time": 52,
        "break_time": 17,
        "long_break_time": 30,
        "long_break_freq": 4
    },
    "90/30": {
        "work_time": 90,
        "break_time": 30,
        "long_break_time": 45,
        "long_break_freq": 4
    }
}
            """
        )


def create_stats_file():
    """Creates stats file with empty stats"""
    with STATS_FILE.open("w") as stats:
        stats.write(
            """{}
            """
        )
