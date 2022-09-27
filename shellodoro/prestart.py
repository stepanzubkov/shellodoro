from config import DATA_DIR, MODES_FILE, STATS_FILE


def create_user_files():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
    if not MODES_FILE.is_file():
        create_modes_file()
    if not STATS_FILE.is_file():
        create_stats_files()


def create_modes_file():
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


def create_stats_files():
    with STATS_FILE.open("w") as stats:
        stats.write(
            """
{
    "days": [
        {
            "name": "Monday",
            "pomodoros": 0
        },
        {
            "name": "Tuesday",
            "pomodoros": 0
        },
        {
            "name": "Wednesday",
            "pomodoros": 0
        },
        {
            "name": "Thursday",
            "pomodoros": 0
        },
        {
            "name": "Friday",
            "pomodoros": 0
        },
        {
            "name": "Saturday",
            "pomodoros": 0
        },
        {
            "name": "Sunday",
            "pomodoros": 0
        }
    ]
}
            """
        )
