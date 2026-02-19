import logging
import re

from requests import Response

from source.python.datatypes import Train, Stop, Line
from source.python.utils.tfl_api_client import TflAPIClient

## This library takes care of parsing all the data we get from the TfL API into usable stuff. Will probably need to be refactored later,
## if I am to be honest.

api_client = TflAPIClient()
logger = logging.getLogger(__name__)

# I *really* don't like that we need to put in a dictionary of stops as an input.
# but whatever, we can resolve that later probably.
def parse_line(
        line_id: str,
        stop_dict: dict[str, Stop]
) -> Line | None:
    new_line = Line(line_id=line_id)
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


