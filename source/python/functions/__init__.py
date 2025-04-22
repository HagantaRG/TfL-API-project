from requests import Response
from dataclasses import dataclass

from tfl_api_client import TflAPIClient

tfl_client: TflAPIClient = TflAPIClient()

@dataclass
class StopPoint:
    stop_id: str
    name: str
    # Naive assumption that if a station exists on a line, it *must* mean that you can interchange onto that line.
    # I see no way this can go wrong. Because I haven't thought about it.
    lines: list[str]
    next_stop_id: str


def construct_route_map_for_line(
        line: str,
        direction: str = "Inbound"
):
    """
    First pass at making a function to construct a route map for a given line. First attempt should succeed
    at making a route map for the Victoria line.
    :param direction: WHICH WAY ARE WE GOING?
    :param line: the ID of the line you would like to generate a route map for.
    :return: a data structure containing a route map of the desired line.
    """
    route_dict: dict[str,list[StopPoint]] = {line:[]}
    response: Response = tfl_client.get_stops_sequence(
        line_id=line,
        direction=direction
    )
    for route in response.json()["stopPointSequences"]:
        for stop in route["stopPoint"]:
            ## TODO: Please make an actual like. Data type for this API response. This is horrendous.
            ## TODO: How does branching work? Maybe the next station parameter *IS* important.
            route_dict[line].append(
                StopPoint(
                    stop_id=stop["stationId"],
                    lines=[line["id"] for line in stop["lines"]],
                    name=stop["name"]
                    )
            )
    return route_dict

    ## I guess this is when I use a linked list. This seems reasonable.
    ## Very dummy first attempt
