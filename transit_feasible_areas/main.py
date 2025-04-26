# Imports --------------------------------------------------
from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import googlemaps
from backend.inputs import geocode_address

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
    time: Annotated[str, Form],
    money: Annotated[str, Form],
    address: Annotated[str, Form]
):
    # Geocode the address
    location_data = geocode_address(address)

    if "error" in location_data:
        return location_data  # You could later return a nicer error page

    # For now, just return everything together
    return {
        "time": time,
        "money": money,
        "address_info": location_data
    }


# # EOF. ----------------------------------------------------
