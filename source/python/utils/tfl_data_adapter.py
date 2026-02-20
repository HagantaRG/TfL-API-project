import logging
import re

from requests import Response

from source.python.datatypes import Train, Stop, Line, Route
from source.python.utils.tfl_api_client import TflAPIClient

## This library takes care of parsing all the data we get from the TfL API into usable stuff. Will probably need to be refactored later,
## if I am to be honest.

api_client = TflAPIClient()
logger = logging.getLogger(__name__)

# I *really* don't like that we need to put in a dictionary of stops as an input.
# but whatever, we can resolve that later, probably.
def parse_line(
        line_id: str,
        stop_dict: dict[str, Stop]
) -> Line | None:
    """
    :param line_id: the ID of the line you are trying to parse. e.g. waterloo-city
    :param stop_dict: dictionary of all stops that have been parsed so far. If none, enter an empty dict
    :return: the line you parsed. If an error is encountered, nothing is returned.
    """
    new_line = Line(
        line_id=line_id,
        stops=[],
        routes=[],
        line_name=""
    )
    line_json: dict = api_client.get_stop_points_for_line(line_id).json()
    new_line.line_name = line_json[0]["lineName"]
    try:
        for stop in line_json:
            if stop["id"] not in stop_dict.keys():
                new_stop: Stop = Stop(
                    stop_name=stop["commonName"],
                    lat=float(stop["lat"]),
                    long=float(stop["lon"]),
                    naptan_id=stop["id"],
                    lines=[new_line]
                )
                stop_dict[stop["id"]] = new_stop
            else:
                stop_dict[stop["id"]].lines.append(new_line)
            new_line.stops.append(stop_dict[stop["id"]])
        return new_line
    except KeyError as error:
        logger.error(
            f"Error in encountered in parsing line {line_id}: {error} \n"
            f"Line {line_id} has not been parsed."
        )

def parse_routes(
        line: Line,
        stop_dict: dict[str, Stop]
) -> None:
    """
    :param line: the line you are trying to parse routes for.
    :param stop_dict: dictionary of all stops that have been parsed so far.
    """
    # *Routes* are distinct from *lines*. What we should really paint on the map are the
    # *routes* that trains can take. For linear lines (e.g. victoria), this doesn't make much of a difference.
    # However, for lines that fork (e.g. Northern) a collection of stops wouldn't actually be enough for us to
    # draw lines, since we wouldn't know how to deal with the train lines after it forks @ Kennington.

    route_json: dict = dict() # New method for the api_client to grab all routes for a line.
    for route in route_json:
        new_route: Route = Route(
            stops = []
        )
        for stops in route:
            # Or something like this. I'll need to look at the JSON schema first once I have internet.
            new_route.stops.append(stop_dict[stops["id"]])
        line.routes.append(new_route)

    ...


# I guess this definitely needs us to know what stops exist first. Bah! Fine. Load trains, then load stops.
# Put on backburner. It is *very* hard to accurately place trains, so let's not linger on positional data for the moment.
# We can at least say that a train is in X position, between two stations.
# We can indicate this with like a little number on the rail segment. That should be easy enough.
def parse_trains(
        line_id: str,
        stop_dict: dict[str, Stop]
) -> list[Train] | None:
    train_list: list[Train] = []
    trains_json: dict = api_client.get_arrivals_for_line(line_id).json()
    try:
        for train in trains_json:
            new_train: Train = Train(
                next_stop=stop_dict[train["naptanId"]]
            )
        return train_list
    except KeyError as error:
        logger.error(
            f"Error in encountered in parsing trains for line {line_id}: {error} \n"
            f"Line {line_id} has not been parsed."
        )


