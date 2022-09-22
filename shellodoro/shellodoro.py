import click
import sys
import time
import json
from pathlib import Path

from .tools import ftime, send_notify, add_pomodoro, get_json, to_graph


if not Path("modes.json").is_file():
    with open("modes.json", "w") as f:
        f.write(
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

if not Path("stats.json").is_file():
    with open("stats.json", "w") as f:
        f.write(
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


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--list-modes", "-l", is_flag=True, help="List pomodoro modes")
@click.option("--stats", "-s", is_flag=True, help="Show user statistics")
def main(ctx, list_modes, stats):
    """Pomodoro timer in terminal"""
    if ctx.invoked_subcommand is None:
        # List all pomodoro modes
        if list_modes:
            with open("modes.json", "r") as f:
                modes = json.load(f)
                for i in modes.keys():
                    click.secho(f"{i}:", fg="green")
                    for j in modes[i].keys():
                        click.echo(f"\t{j}: {modes[i][j]}")
        if stats:
            to_graph(get_json("stats.json"))


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
def start(mode, session_size, work_label, break_label):
    """Starts a pomodoro timer with choosed mode and size"""
    with open("modes.json", "r") as f:
        json_inner = f.read()
        # Check existing mode
        if mode not in json.loads(json_inner).keys():
            raise NameError(f'Mode "{mode}" does not exist')
        else:
            mode_data = json.loads(json_inner)[mode]

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
def add(name, work_time, break_time, long_break_time, long_break_freq):
    """Add a pomodoro mode"""
    modes = get_json("modes.json")
    if name in modes.keys():
        click.secho("Error: This mode already exists", fg="red")
        return
    with open("modes.json", "w") as f:
        modes[name] = {
            "work_time": work_time,
            "break_time": break_time,
            "long_break_time": long_break_time,
            "long_break_freq": long_break_freq,
        }
        json.dump(modes, f, indent=4)
    click.secho("The mode was created successfully!", fg="green")


@main.command()
@click.argument("name")
def delete(name):
    """Delete pomodoro mode"""

    modes = get_json("modes.json")
    if name not in modes.keys():
        click.secho("Error: This mode does not exist", fg="red")
        return
    with open("modes.json", "w") as f:
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
def edit(name, work_time, break_time, long_break_time, long_break_freq):
    """Edit pomodoro mode"""
    modes = get_json("modes.json")
    if name not in modes.keys():
        click.secho("Error: This mode does not exist", fg="red")
        return
    with open("modes.json", "w") as f:
        current_mode = modes[name]
        modes[name] = {
            "work_time": work_time if work_time else current_mode["work_time"],
            "break_time": break_time if break_time else current_mode["break_time"],
            "long_break_time": long_break_time
            if long_break_time
            else current_mode["long_break_time"],
            "long_break_freq": long_break_freq
            if long_break_freq
            else current_mode["long_break_freq"],
        }
        json.dump(modes, f, indent=4)
    click.secho("The mode was edited successfully!", fg="green")


if __name__ == "__main__":
    main()
