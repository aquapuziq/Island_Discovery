import json
from head.geojson_validate import validate_features

def test_validate_features():
    with open("test_islands.json") as file:
        data = json.load(file)
    assert validate_features(data) == True

def test_validate_not_features():
    data = {"type": "Feature", "geometry": {}}
    assert validate_features(data) == False

def test_validate_miss_features():
    data = {"type": "FeatureCollection"}
    assert validate_features(data) == False