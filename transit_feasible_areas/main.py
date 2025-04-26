# Imports --------------------------------------------------
from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import googlemaps
from backend.inputs import geocode_address
from backend import get_relevant_stops as st
from backend.get_api import get_distance, get_points

# App handler -----------------------------------------------

app = FastAPI()

def create_googlemaps_object():
    return googlemaps.Client(key="xx")

googlemap = create_googlemaps_object()

# Resources -------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Endpoints -------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="map.html",
    )

@app.post("/")
async def login(
    request: Request,
    time: Annotated[str, Form],
    money: Annotated[str, Form],
    address: Annotated[str, Form]
):
    location_data = geocode_address(address)

    if "error" in location_data:
        return location_data  # Later show a better error page

    lat = location_data["latitude"]
    lng = location_data["longitude"]

    # Now find nearby stops
    stops_df = st.relevant_stops(lng, lat)

    # Get json with isopolygon and properties
    isodistance = get_distance(lng, lat, "bycicle", 900)
    coords_map = isodistance["features"]["geometry"]["coordinates"]
    

    # get json with points of interest
    geometry_id = isodistance["properties"]["id"]
    points = get_points(geometry_id, lng, lat)

    stops = stops_df.to_dict(orient="records")

    return templates.TemplateResponse(
        request=request, name="map_with_isochrone.html", context={"shape": coords_map}
    )

    # return {
    #     "time": time,
    #     "money": money,
    #     "address_info": location_data,
    #     "nearby_stops": stops,
    #     "isodistance": geometry_id,
    #     "points": points
    # }


# # EOF. ----------------------------------------------------
