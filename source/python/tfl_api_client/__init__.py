
# Import third-party libraries
from requests import get, Response
from requests.auth import HTTPBasicAuth

class TflAPIClient:
    base_url: str
    # TODO: What to do about consecutive errors -- how would I chuck them out?
    # TODO: Also empty results.
    def __init__(
            self,
            base_url: str = ...
    ):
        self.base_url = base_url if base_url is not ... else "https://api.tfl.gov.uk"

    def get_arrivals(
            self,
            stop_point_id: str
    ):
        url: str = f"{self.base_url}/StopPoint/{stop_point_id}/Arrivals"
        response: Response = get(
            url=url
        )
        return response

    def get_modal_disruptions(
            self,
            modes: list[str]
    ):

        url: str = f"{self.base_url}/Line/Mode/{",".join(modes)}/Disruption"
        response: Response = get(
            url=url
        )
        return response

    def get_stops_sequence(
            self,
            line_id: str,
            direction: str,
            exclude_crowding: str = ...,
            service_types: str|list[str] = ...
    ):
        url: str = f"{self.base_url}/Line/{line_id}/Route/Sequence/{direction}"
        params = ...
        if (exclude_crowding is not ...) or (service_types is not ...):
            params = {}
            if exclude_crowding is not ... :
                params["excludeCrowding"] = exclude_crowding
            if service_types is not ... :
                params["serviceTypes"] = service_types

        response: Response = get(
            url=url,
            params=params if params is not ... else None
        )
        return response

