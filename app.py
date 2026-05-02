from fastapi import FastAPI, Request, HTTPException
from head.geojson_validate import validate_features
from head.geojson_output import linestring_to_polygon

app = FastAPI()

@app.post("/process")
async def process(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if not validate_features(data):
        raise HTTPException(status_code=400, detail="Invalid GeoJSON")

    output = linestring_to_polygon(data["features"])
    print(f"Output features count: {len(output['features'])}")
    return output