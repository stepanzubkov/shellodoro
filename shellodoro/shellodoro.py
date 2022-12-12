"""
Main executable file
"""

import click
import sys
import time
import json
from typing import Dict, Any

from .config import MODES_FILE, STATS_FILE
from .tools import ftime, send_notify, add_pomodoro, get_json
from .formatting import format_modes, stats_to_graph
from .prestart import create_user_files
from .models.mode import Mode


create_user_files()


@click.group(invoke_without_command=True)
@click.pass_context
def main(_ctx: Any) -> None:
    """Pomodoro timer in terminal"""


@main.command()
def list_modes() -> None:
    """Lists all pomodoro modes"""
    with MODES_FILE.open() as f:
        modes: Dict[str, Mode] = json.load(f)
        click.echo(format_modes(modes))


@main.command()
def stats() -> None:
    """Shows statistics by last week"""
    click.echo(stats_to_graph(get_json(STATS_FILE)))


@main.command()
@click.option(
    "--mode", "-m", default="default", help="Mode for pomodoro timer", show_default=True
)
@click.option(
    "--session-size",
    "-s",
    default=5,
    help="Sets session size in pomodoros",
    show_default=True,
    type=click.IntRange(1, 20),
)
@click.option(
    "--work-label",
    "-w",
    default="It`s time for work!",
    help="Sets work time label",
    show_default=True,
)
@click.option(
    "--break-label",
    "-b",
    default="It`s time for break!",
    help="Sets break time label",
    show_default=True,
)
def start(mode, session_size, work_label, break_label) -> None:
    """Starts a pomodoro timer with choosed mode and size"""
    with MODES_FILE.open() as f:
        json_inner: str = f.read()
        # Check existing mode
        if mode not in json.loads(json_inner).keys():
            raise NameError(f'Mode "{mode}" does not exist')
        else:
            mode_data: Mode = Mode(**json.loads(json_inner)[mode])

    click.secho(
        f"Pomodoro timer with mode {mode} and session size {session_size} pomodoros launched!",
        fg="green",
    )
    for i in range(1, session_size + 1):
        click.echo("\n" + "#" * 30)
        click.secho(f"Pomodoro {i}/{session_size} started!", fg="green")
        click.secho(work_label, fg="green")
        send_notify(text=work_label)
        # Work timer
        for tick in range(1, mode_data["work_time"] * 60 + 1):
            sys.stdout.write("\r")
            sys.stdout.write(ftime(seconds=tick))
            sys.stdout.flush()
            time.sleep(1)
        add_pomodoro()
        # For last pomodoro
        if i < session_size:
            # Break timer
            send_notify(text=break_label)
            click.secho("\n" + break_label, fg="red")
            for tick in range(
                1,
                mode_data["break_time"] * 60 + 1
                if i % mode_data["long_break_freq"]
                else mode_data["long_break_time"] * 60 + 1,
            ):
                sys.stdout.write("\r")
                sys.stdout.write(ftime(seconds=tick))
                sys.stdout.flush()
                time.sleep(1)

    send_notify(text="Thank you for using shellodoro! :)")
    click.echo("\nThank you for using shellodoro! :)")


@main.command()
@click.argument("name")
@click.option(
    "--work-time", "-w", default=20, show_default=True, help="Sets a work time"
)
@click.option(
    "--break-time", "-b", default=5, show_default=True, help="Sets a break time"
)
@click.option(
    "--long-break-time",
    "-l",
    default=15,
    show_default=True,
    help="Sets a long break time",
)
@click.option(
    "--long-break-freq",
    "-f",
    default=4,
    show_default=True,
    help="Sets a long break frequency",
)
def add(name, work_time, break_time, long_break_time, long_break_freq) -> None:
    """Adds a pomodoro mode"""
    modes: Dict[str, Mode] = get_json(MODES_FILE)
    if name in modes.keys():
        click.secho("Error: This mode already exists", fg="red")
        return
    with MODES_FILE.open("w") as f:
        modes[name] = Mode(
            work_time=work_time,
            break_time=break_time,
            long_break_time=long_break_time,
            long_break_freq=long_break_freq,
        )
        json.dump(modes, f, indent=4)
    click.secho("The mode was created successfully!", fg="green")


@main.command()
@click.argument("name")
def delete(name) -> None:
    """Deletes pomodoro mode"""

    modes: Dict[str, Mode] = get_json(MODES_FILE)
    if name not in modes.keys():
        click.secho("Error: This mode does not exist", fg="red")
        return
    with MODES_FILE.open("w") as f:
        del modes[name]
        json.dump(modes, f, indent=4)
    click.secho("The mode was deleted successfully!", fg="green")


@main.command()
@click.argument("name")
@click.option("--work-time", "-w", type=int, show_default=True, help="Sets a work time")
@click.option(
    "--break-time", "-b", type=int, show_default=True, help="Sets a break time"
)
@click.option(
    "--long-break-time",
    "-l",
    type=int,
    show_default=True,
    help="Sets a long break time",
)
@click.option(
    "--long-break-freq",
    "-f",
    type=int,
    show_default=True,
    help="Sets a long break frequency",
)
def edit(name, work_time, break_time, long_break_time, long_break_freq) -> None:
    """Edits pomodoro mode"""
    modes: Dict[str, Mode] = get_json(MODES_FILE)
    if name not in modes.keys():
        click.secho("Error: This mode does not exist", fg="red")
        return
    with MODES_FILE.open("w") as f:
        current_mode: Mode = modes[name]
        modes[name] = Mode(
            work_time=work_time if work_time else current_mode["work_time"],
            break_time=break_time if break_time else current_mode["break_time"],
            long_break_time=long_break_time
            if long_break_time
            else current_mode["long_break_time"],
            long_break_freq=long_break_freq
            if long_break_freq
            else current_mode["long_break_freq"],
        )
        json.dump(modes, f, indent=4)
    click.secho("The mode was edited successfully!", fg="green")


if __name__ == "__main__":
    main()
