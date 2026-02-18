import logging
import re

from requests import Response

from source.python.datatypes import Train, Stop, Line
from source.python.utils.tfl_api_client import TflAPIClient


api_client = TflAPIClient()
logger = logging.getLogger(__name__)

def parse_line(
        line_id: str
) -> Line | None:
    new_line = Line(line_name=line_id)
    line_json: dict = api_client.get_stop_points_for_line(line_id).json()
    try:
        for stop in line_json:
            new_stop: Stop = Stop(
                stop_name=stop["commonName"],
                lat=float(stop["lat"]),
                long=float(stop["lon"]),
                naptan_id=stop["id"]
            )
            new_line.stops.append(new_stop)
        return new_line
    except KeyError as error:
        logger.error(
            f"Error in encountered in parsing line {line_id}: {error} \n"
            f"Line {line_id} has not been parsed."
        )

# I guess this definitely needs us to know what stops exist first. Bah! Fine. Load trains, then load stops.
def parse_trains(
        line_id: str
) -> list[Train] | None:
    train_list: list[Train] = []
    trains_json: dict = api_client.get_arrivals_for_line(line_id).json()
    try:
        for train in trains_json:
            new_train: Train = Train(
                next_stop=train["stationName"],
                previous_stop=re.search("Between (.*) and (.*)", train["currentLocation"]),
                destination_stop=train["destinationName"]
            )
        return train_list
    except KeyError as error:
        logger.error(
            f"Error in encountered in parsing trains for line {line_id}: {error} \n"
            f"Line {line_id} has not been parsed."
        )
