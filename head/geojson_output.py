from head.island_process import islands_groups, group_by_type
from shapely.geometry import MultiPoint

def build_boundaries(groups):
    polygons = []
    for key, val in groups.items():
        for v in val:
            polygons.extend(v)
    if not polygons:
        return None

    hull = MultiPoint(polygons).convex_hull
    if hull.geom_type != 'Polygon':
        return None
    return list(hull.exterior.coords)

def linestring_to_polygon(features):
    print("linestring_to_polygon called")
    output = {
        "type": "FeatureCollection",
        "features": [
        ]
    }
    groups = group_by_type(features)
    islands_gr = islands_groups(groups)
    for key, val in islands_gr.items():
        for v in val:
            feature = {
                "type": "Feature",
                "properties": {"type": key},
                "geometry": {"type": "Polygon", "coordinates": [[list(point) for point in v]]}
            }
            output["features"].append(feature)
    bound = build_boundaries(islands_gr)
    if bound is not None:
        feature = {
            "type": "Feature",
            "properties": {"class": "boundaries"},
            "geometry": {"type": "Polygon", "coordinates": [[list(point) for point in bound]]}
        }
        output["features"].append(feature)
    return output

