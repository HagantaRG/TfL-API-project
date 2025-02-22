from __future__ import annotations

class ArrivalResponse:
    arrivals: list[Arrival]

class Arrival:
    id: str
    operation_type: int
    vehicle_id: str
    naptan_id: str
    station_name: str
    line_id: str
    line_name: str
    platform_name: str
    direction: str
    bearing: str
    destination_naptan_id: str
    destination_name: str
    timestamp: str
    time_to_station: str
    current_location: str
    towards: str
    expected_arrival: str
    time_to_live: str
    mode_name: str
    timing: Timing

class Timing:
    countdown_server_adjustment: str
    source: str
    insert: str
    read: str
    sent: str
    received: str

