from typing import Final

class ApiLake:
    """
    This class contains the columns of the api_lake table within the TfL apps DB.

    Primary key: ID
    """
    TIME: Final[str] = "time"
    JSON: Final[str] = "json"
    ENDPOINT_URL: Final[str] = "endpoint_url"
    STATUS_CODE: Final[str] = "status_code"
    ID: Final[str] = "id"
