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
@app.post("/")
async def login(
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
    stops_df = st.relevant_stops(lat, lng)

    # (optional) If you want to return as a dictionary list:
    stops = stops_df.to_dict(orient="records")

    return {
        "time": time,
        "money": money,
        "address_info": location_data,
        "nearby_stops": stops
    }


# # EOF. ----------------------------------------------------
