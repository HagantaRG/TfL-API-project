from requests import Response
from dataclasses import dataclass

from utils.tfl_api_client import TflAPIClient

tfl_client: TflAPIClient = TflAPIClient()


@dataclass
class StopPoint:
    # I feel like I'm reinventing the idea of linked list here. Or one of those graph theory datatypes...
    # There's probably like. A reasonable canon way to do this. I'll shop around later.
    next_stop_ids: set[str]
    start: bool



def construct_route_map_for_line(
        line: str,
        direction: str = "Inbound"
) -> dict[str, StopPoint]:
    """
    First pass at making a function to construct a route map for a given line. First attempt should succeed
    at making a route map for the Victoria line.
    :param direction: WHICH WAY ARE WE GOING?
    :param line: the ID of the line you would like to generate a route map for.
    :return: a data structure containing a route map of the desired line.
    """
    route_dict: dict[str, StopPoint] = {}
    response: Response = tfl_client.get_stops_sequence(
        line_id=line,
        direction=direction
    )
    for route in response.json()["orderedLineRoutes"]:
        route_id_sequence: list[str] = route["naptanIds"]
        first_stop_id: str = route_id_sequence[0]
        if first_stop_id not in route_dict:
            route_dict[route_id_sequence[0]] = StopPoint(
                next_stop_ids=set(),
                start=True
            )
        else:
            route_dict[first_stop_id].start = True
        route_dict[route_id_sequence[0]].next_stop_ids.add(route_id_sequence[1])

        for stop_num, stop_id in enumerate(route_id_sequence[1:-2]):
            ## TODO: Please make an actual like. Data type for this API response. This is horrendous.
            ## TODO: How does branching work? Maybe the next station parameter *IS* important.
            if stop_id not in route_dict:
                route_dict[stop_id] = StopPoint(
                    next_stop_ids=set(),
                    start=False
                )
            route_dict[stop_id].next_stop_ids.add(route_id_sequence[stop_num+1])
    return route_dict

## I guess this is when I use a linked list. This seems reasonable.
## Very dummy first attempt
baboom = construct_route_map_for_line("northern")
print("HAHAHAHA")