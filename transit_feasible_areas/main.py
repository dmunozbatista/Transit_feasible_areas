# Imports --------------------------------------------------
from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend import get_relevant_stops as st

# App handler -----------------------------------------------

app = FastAPI()

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
async def login(time: Annotated[str, Form()], money: Annotated[str, Form()], address: Annotated[str, Form()]):
    return {"time": time, "money":money, "address":address}


# # EOF. ----------------------------------------------------

# get the lat and lon from address

lat = 41.781729
lon = -87.60491761427323

# get bus and bike stations
st.relevant_stops(lat, lon, 3) 

#
