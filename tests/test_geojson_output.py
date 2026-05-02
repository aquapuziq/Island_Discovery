import json
from geojson_output import linestring_to_polygon

def test_linestring_to_polygon():
    with open("test_islands.json") as file:
        data = json.load(file)
    output = linestring_to_polygon(data["features"])
    assert output == {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"type": "a"}, "geometry": {"type": "Polygon", "coordinates": [[[0, 1], [1, 1], [1, 0], [0, 0], [0, 1]]]}}, {"type": "Feature", "properties": {"class": "boundaries"}, "geometry": {"type": "Polygon", "coordinates": [[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]]]}}]}