from fastapi import FastAPI
from pydantic import BaseModel
import googlemaps

app = FastAPI()

# Define the expected input structure
class FeasibilityInput(BaseModel):
    money_available: float
    transportation_mode: str

@app.post("/feasible_areas")
def calculate_feasible_areas(input_data: FeasibilityInput):
    return {
        "message": f"You have ${input_data.money_available} available for {input_data.transportation_mode}."
    }