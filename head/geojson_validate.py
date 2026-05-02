def validate_features(data):
    if data.get("type") != "FeatureCollection":
        return False
    if type(data.get("features")) != list:
        return False
    return True