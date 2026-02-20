from source.python.utils.tfl_data_adapter import parse_line, parse_routes
from source.python.datatypes import Stop, Line, Route

# Absolute first version goal:
# draw grid of all stops (cartesian plane is OK)
# connect points on grid w/ routes (we can ignore the *hellscape* that is the district line for now...)

line_ids: list[str] = [
    "waterloo_city",
    "victoria"
]
stop_dict: dict[str, Stop] = {}
line_dict: dict[str, Line] = {}

lat_max: float = -10000
lat_min: float = 10000
lon_max: float = -10000
lon_min: float = 10000

# This should get all the lines + routes we care about.
for line_id in line_ids:
    line_dict[line_id] = parse_line(line_id, stop_dict)
    parse_routes(line_dict[line_id], stop_dict)

# Draw! NB please normalise the lat-longs so we don't have a ridiculous variance.
for line in line_dict.values():
    ...