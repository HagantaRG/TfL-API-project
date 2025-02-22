from csv import DictWriter

import requests
import csv

trackernet_filename: str = "trackernet-codes.txt"
result_csv_filename: str = "trackernet-results.csv"
csv_fields = [
    "Station Name",
    "Station Code",
    "Line Code",
    "Result Code"
]

line: str = "D"
station: str = "WIM"
URL: str = f"https://api.tfl.gov.uk/trackernet/PredictionDetailed/{line}/{station}"
headers: dict = {
    "app_key": "5eadabdde47c4f6a84af7e9271492623"
}

trial = requests.get(
    url=URL,
    headers=headers
)

with open(trackernet_filename) as trackernet_text, open(result_csv_filename, "w", newline="") as output_csv:
    line_code: str
    writer: csv.DictWriter = csv.DictWriter(output_csv, fieldnames=csv_fields)
    writer.writeheader()
    for line in trackernet_text:
        if line[0] == "-":
            line_code = line[1]
            continue
        else:
            station_code: str = line[0:3]
            station_name: str = line[4:-1]
            URL: str = f"https://api.tfl.gov.uk/trackernet/PredictionDetailed/{line_code}/{station_code}"
            print(f"Querying TrackerNet for {station_name} on line code {line_code}")
            result = requests.get(
                url=URL,
                headers=headers
            )
            print(f"Query finished, with result code {result.status_code}")
            data_dict: dict[str, str|int] = {
                csv_fields[0]: station_name,
                csv_fields[1]: station_code,
                csv_fields[2]: line_code,
                csv_fields[3]: result.status_code
            }
            writer.writerow(data_dict)
            output_csv.flush()
        ...
