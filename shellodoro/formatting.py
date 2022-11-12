"""
Text formatting functions
"""

from datetime import datetime, timedelta
from typing import Dict

import click

from .models.mode import Mode


def format_modes(modes: Dict[str, Mode]) -> str:
    """Formats modes json into beautiful string

    Args:
        modes (Dict[Mode]): Modes

    Returns:
        str: Result string
    """
    result = ""
    for i in modes.keys():
        result += click.style(f"{i}:\n", fg="green")
        for j in modes[i].keys():
            result += f"\t{j}: {modes[i][j]}\n"

    return result


def stats_to_graph(stats: Dict[str, int]) -> str:
    """Converts stats to graph

    ## Example
    ```
    4              #
    3  #           #
    2  #  #        #
    1  #  #        #
      01 02 03 04 05 06 07
      01.01.2023 - 07.01.2023
    ```

    Args:
        stats (Dict[str, int]): Stats

    Returns:
        str: Formatted graph of stats
    """

    now = datetime.now()
    previous_week = [
        (now - timedelta(days=x)).strftime("%d.%m.%Y") for x in range(7, -1, -1)
    ]
    graph_height = max(stats.get(day, 0) for day in previous_week)
    graph = ""
    for i in range(graph_height, 0, -1):
        graph += str(i)
        for day in previous_week:
            if stats.get(day, 0) >= 1:
                graph += "  #"
            else:
                graph += "   "
        graph += "\n"

    graph += " "
    for day in previous_week:
        graph += f" {day[:2]}"

    graph += f"\n  {previous_week[0]} - {previous_week[-1]}"

    return graph
