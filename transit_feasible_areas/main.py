# Imports --------------------------------------------------
from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


# # EOF. ----------------------------------------------------
