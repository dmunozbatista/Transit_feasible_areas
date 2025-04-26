from fastapi import FastAPI
from pydantic import BaseModel
import googlemaps

# --- Setup ---
app = FastAPI()

def geocode_address(address: str):
    geocode_result = googlemaps.geocode(address)

    if not geocode_result:
        return {"error": "Address not found"}

    # Extract coordinates (lat, lng)
    location = geocode_result[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']

    return {
        "address": address,
        "latitude": lat,
        "longitude": lng
    }

# class FeasibilityInput(BaseModel):
#     money_available: float
#     transportation_mode: str

# class AddressInput(BaseModel):
#     address: str


# # POST for feasible areas
# @app.post("/feasible_areas")
# def calculate_feasible_areas(input_data: FeasibilityInput):
#     return {
#         "message": f"You have ${input_data.money_available} available for {input_data.transportation_mode}."
#     }

# # POST for address geocoding
# @app.post("/geocode_address")
# def geocode_address(address_input: AddressInput):
#     geocode_result = googlemap.geocode(address_input.address)

#     if not geocode_result:
#         return {"error": "Address not found"}

#     # Extract coordinates (lat, lng)
#     location = geocode_result[0]['geometry']['location']
#     lat = location['lat']
#     lng = location['lng']

#     return {
#         "address": address_input.address,
#         "latitude": lat,
#         "longitude": lng
#     }

