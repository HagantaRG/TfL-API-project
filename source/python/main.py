# Import standard modules
from datetime import datetime
from time import sleep, time
import json
# Import third-party modules
from requests import Response
# Import private modules
from tfl_api_client import TflAPIClient
from db_client import DBClient
from db_schemas import ApiLake
from configs import DEFAULT_DB_CLIENT

# Initial try -- just have something that keeps running until stopped, that continuously pings ONE endpoint, and shoves
# that data into the DB.
tfl_client: TflAPIClient = TflAPIClient()
db_client: DBClient = DEFAULT_DB_CLIENT

with db_client as db_connection:
    while True:
        # Sample, grabbing from Wimbledon
        query_time: datetime = datetime.now()
        response: Response = tfl_client.get_arrivals("940GZZLUWIM")
        response_json = response.json()
        db_client.execute_query(
            query=f"INSERT INTO api_lake ({ApiLake.TIME}, {ApiLake.JSON}, {ApiLake.STATUS_CODE}, {ApiLake.ENDPOINT_URL}) VALUES (%s, %s, %s, %s)",
            params=(query_time, json.dumps(response_json), response.status_code, response.url)
        )
        print("Done!")
        sleep(30)
        ...
