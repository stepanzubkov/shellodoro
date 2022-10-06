from operator import itemgetter
from datetime import datetime, timedelta
import subprocess
import json
from plyer import notification
from sys import platform
from pathlib import Path

from .config import STATS_FILE


def send_notify(text: str):
    """Function to sending notifications to user"""
    if platform == "win32":
        notification.notify(message=text, app_name="Shellodoro", title="Shellodoro")
    # Linux and other UNIX OS`s
    else:
        subprocess.Popen(
            ["notify-send", "Shellodoro", text, "-a", "Shellodoro", "-i", "terminal"]
        )


def ftime(seconds: int):
    """Time formatting function for pomodoro timer"""
    m = seconds // 60
    s = seconds - m * 60
    format_m = str(m) if m >= 10 else f"0{m}"
    format_s = str(s) if s >= 10 else f"0{s}"
    return f"{format_m}:{format_s}"


def to_graph(data: dict):
    now = datetime.now()
    previous_week = [
        (now - timedelta(days=x)).strftime("%d.%m.%Y") for x in range(7, -1, -1)
    ]
    for i in range(max(data.get(key, 0) for key in previous_week), 0, -1):
        print(
            str(i),
            *["#" if data.get(day, 0) >= i else " " for day in previous_week],
            sep="  ",
        )
    print("  ", *[day[:2] for day in previous_week], sep=" ")
    print("  ", previous_week[0], "-", previous_week[-1])


def add_pomodoro():
    with STATS_FILE.open("r") as file:
        json_inner = json.loads(file.read())
    with STATS_FILE.open("w") as file:
        current_date = datetime.now().strftime("%d.%m.%Y")
        if current_date in json_inner.keys():
            json_inner[current_date] += 1
        else:
            json_inner[current_date] = 1
        json.dump(json_inner, file, indent=4)


def get_json(file: Path):
    with file.open() as f:
        json_inner = f.read()
        obj = json.loads(json_inner)
    return obj
