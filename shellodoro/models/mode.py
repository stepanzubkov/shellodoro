from typing import TypedDict


class Mode(TypedDict):
    work_time: int
    break_time: int
    long_break_time: int
    long_break_freq: int

