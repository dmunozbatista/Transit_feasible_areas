from fastapi import FastAPI
from pydantic import BaseModel
import googlemaps

# --- Setup ---
app = FastAPI()

def create_googlemaps_object():
    return googlemaps.Client(key="AIzaSyB0OuiuAIilorHNhFQ9AUXhc7Jo9Rx6QgQ")

googlemap = create_googlemaps_object()

class FeasibilityInput(BaseModel):
    money_available: float
    transportation_mode: str

class AddressInput(BaseModel):
    address: str


# POST for feasible areas
@app.post("/feasible_areas")
def calculate_feasible_areas(input_data: FeasibilityInput):
    return {
        "message": f"You have ${input_data.money_available} available for {input_data.transportation_mode}."
    }

# POST for address geocoding
@app.post("/geocode_address")
def geocode_address(address_input: AddressInput):
    geocode_result = googlemap.geocode(address_input.address)

    if not geocode_result:
        return {"error": "Address not found"}

    # Extract coordinates (lat, lng)
    location = geocode_result[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']

    # Here just returning them for now
    return {
        "address": address_input.address,
        "latitude": lat,
        "longitude": lng
    }

