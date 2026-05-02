# Island Discovery

A microservice that processes GeoJSON data and identifies closed loops ("islands")
formed by `LineString` features, converting them into `Polygon` features.

## Algorithm

The service groups `LineString` features by their `type` property, then builds
an undirected graph where segment endpoints are nodes and segments are edges.
For each connected component it checks the Eulerian circuit condition (all vertices
have even degree). If satisfied, the circuit is traversed using Hierholzer's algorithm
to reconstruct the full polygon circuit including all intermediate coordinates.

In addition to per-island polygons, a single boundary polygon encompassing all
discovered islands is emitted with `{"class": "boundaries"}`.

## Project Structure

```
Island_Discovery/
1) head/                # all logic
    island_process.py   # graph building, cycle detection, Hierholzer algorithm (Eulerian circuit)
    geojson_output.py   # polygon assembly, boundaries building
    geojson_validate.py # GeoJSON format validation
2) samples/             # sample GeoJSON (and JSON) input files
3) tests/               # pytest unit-tests 
4) app.py               # FastAPI application
5) requirements.txt
6) Dockerfile
```

## Build and Run

```bash
docker build -t island-discovery .
```
```bash
docker run -p 8080:8080 island-discovery
```

## Testing the Endpoint

Send a sample JSON to the `/process` endpoint:

```bash
curl -X POST http://localhost:8080/process -H "Content-Type: application/json" -d @samples/re_12023011321012.json
```

Expected response — a GeoJSON `FeatureCollection` containing one `Polygon` per
discovered island with `{"type": "<...>"}` and one boundary `Polygon`
with `{"class": "boundaries"}`.

Input JSON has no `LineString` features

```bash
curl -X POST http://localhost:8080/process -H "Content-Type: application/json" -d @samples/without_linestring.json
```
Expected response — a GeoJSON `{"type":"FeatureCollection","features":[]}`

Test invalid input (expect `400` and `{"detail":"Invalid JSON"}`):

```bash
curl -X POST http://localhost:8080/process -H "Content-Type: application/json" -d @samples/invalid_json.json
```

Test invalid GeoJSON (without "FeatureCollection" type or "features") (expect `400` and `{"detail":"Invalid GeoJSON"}`):

```bash
curl -X POST http://localhost:8080/process -H "Content-Type: application/json" -d @samples/invalid_geojson.json
```

## Visualizing Results

To visually verify the output, paste the response GeoJSON into [geojson.io](https://geojson.io/next/).
The discovered islands will appear as polygons on the map, and the boundary polygon
will encompass all of them.

for example file `samples/re_12021310131033.json`
before:
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/ba8d9a38-7409-4793-a173-9e9a0acbb744" />

after:
<img width="300" height="250" alt="image" src="https://github.com/user-attachments/assets/f9ff010e-d1e2-438b-8d78-d0d4ab5e8e6c" />

## Testing

Default unit-testing via pytest
just install dependencies and run the test suite:

```bash
pip install pytest
pytest tests/                          # run all tests
pytest tests/test_name.py              # run just one test file; for example pytest tests/test_geojson_output.py
pytest tests/test_name.py::test_func   # run one concrete test from concrete file;
# for example:
pytest tests/test_island_process.py::test_build_graph
```

### Test cases
1) `test_island_process.py`
- `test_build_graph` — graph built correctly from a single LineString segment
- `test_is_island` — three segments forming a triangle produce a valid island
- `test_find_islands` — two segments of the same type form one closed loop
- `test_group_by_type_from_json` — grouping correctly ignores Points and separates by type
- `test_find_islands_no_circuit` — an open chain of segments produces no islands
- `test_find_islands_many` — three separate triangles produce three independent islands
- `test_islands_groups_mixed` — one type forms an island, another type produces no cycle
2) `test_geojson_validate.py`
- `test_validate_features` — valid GeoJSON passes validation
- `test_validate_not_features` — wrong types and lists returns False
- `test_validate_miss_features` — missing features key returns False
3) `test_geojson_output.py`
- `test_linestring_to_polygon` — `linestring_to_polygon` func return correct GeoJSON

### AI Usage
I used Claude Sonet 4.6 web to understand which technology stack to use, for example:
1) I initially wanted to use Django because I already had experience with it, but I came to the conclusion that it was overkill.
2) The neural network suggested using the Shapely library to build a boundary polygon.
3) I also didn't know about Hierholzer's algorithm for determining whether a graph is an Euler circuit.
4) Understanding the GeoJSON structure.
5) A quick search for relevant resources and libraries to study how the above works.

All the code was written by me, except for fixing an issue with coordinate intersection and the resulting lack of a boundary polygon (geojson_output.py function build_boundaries and MultiPoint method).
