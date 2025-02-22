
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


