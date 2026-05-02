from island_process import islands_groups, group_by_type
from shapely.geometry import Polygon
from shapely.ops import unary_union

def build_boundaries(groups):
    polygons = []
    for key, val in groups.items():
        for v in val:
            poly = Polygon(v)
            if not poly.is_valid:
                poly = poly.buffer(0)
            polygons.append(poly)
    if not polygons:
        return None

    merged = unary_union(polygons)
    hull = merged.convex_hull
    return list(hull.exterior.coords)

def linestring_to_polygon(features):
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

