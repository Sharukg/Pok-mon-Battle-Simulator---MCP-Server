from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from battle_logic import simulate_battle

# Create a FastAPI instance
app = FastAPI()

# A global variable to store the Pokémon data
pokemon_data = {}

# Configure CORS to allow requests from your local file
origins = [
    "null", # Allows requests from a local file opened in a browser
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use FastAPI's startup event to load the data once
@app.on_event("startup")
async def load_pokemon_data():
    global pokemon_data
    file_path = os.path.join(os.path.dirname(__file__), "pokemon_data.json")
    try:
        with open(file_path, "r") as f:
            pokemon_data = json.load(f)
        print("Pokémon data loaded successfully.")
    except FileNotFoundError:
        print("Error: pokemon_data.json not found.")
        raise RuntimeError("Required data file not found. Please ensure pokemon_data.json is in the project directory.")

# The MCP manifest endpoint
@app.get("/.well-known/mcp/manifest.json")
def get_mcp_manifest():
    return FileResponse("manifest.json")

# A basic welcome message for the root URL
@app.get("/")
def read_root():
    return {"Hello": "Trainer!"}

# Endpoint for the Pokémon Data Resource
@app.get("/v1/resources/pokemon_data_resource/get")
def get_pokemon_data(pokemon_name: str):
    # Normalize the name to handle case variations
    normalized_name = pokemon_name.lower().replace(" ", "-")

    # Look up the Pokémon in your loaded data
    if normalized_name in pokemon_data:
        return pokemon_data[normalized_name]
    else:
        # If the Pokémon is not found, return a 404 error
        raise HTTPException(status_code=404, detail="Pokémon not found")

# Pydantic model for the Battle Simulation Tool's request body
class BattleRequest(BaseModel):
    pokemon1: str
    pokemon2: str

# Endpoint for the Battle Simulation Tool
@app.post("/v1/tools/battle_simulation_tool/run")
def run_battle_simulation(request: BattleRequest):
    # Check if both Pokémon exist in the data before running the simulation
    p1_name = request.pokemon1.lower().replace(" ", "-")
    p2_name = request.pokemon2.lower().replace(" ", "-")

    if p1_name not in pokemon_data:
        raise HTTPException(status_code=404, detail=f"Pokémon '{request.pokemon1}' not found.")
    if p2_name not in pokemon_data:
        raise HTTPException(status_code=404, detail=f"Pokémon '{request.pokemon2}' not found.")

    # Call the battle logic function from the separate module
    result = simulate_battle(p1_name, p2_name, pokemon_data)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)