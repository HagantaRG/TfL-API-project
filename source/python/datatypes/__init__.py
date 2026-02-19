from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Train:
    destination_stop: Stop
    previous_stop: Stop
    next_stop: Stop
    ...

@dataclass
class Stop:
    lat: float
    long: float
    lines: list[Line]
    stop_name: str
    naptan_id: str
    ...

@dataclass
class Line:
    stops: list[Stop]
    line_name: str
    routes: list[Route]
    line_id: str
    ...

@dataclass
class Route:
    stops: list[Stop]
    line_name: str