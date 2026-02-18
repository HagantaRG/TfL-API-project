from __future__ import annotations

class Train:
    destination_stop: Stop
    previous_stop: Stop
    next_stop: Stop
    ...

class Stop:
    adjacent_stops: list[Stop]
    lat: float
    long: float
    lines: list[Line]
    ...

class Line:
    stops: list[Stop]
    ...