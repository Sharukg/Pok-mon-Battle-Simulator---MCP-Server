Pokémon Battle Simulator - MCP Server
This project is a technical assessment for building a server that acts as a bridge between an AI (specifically, an LLM) and the world of Pokémon. It provides the AI with two main capabilities: a data resource for accessing comprehensive Pokémon information and a battle tool for simulating combat between any two Pokémon. The server is built in accordance with the Model Context Protocol (MCP) standards.

Technologies Used
Python: The core programming language.

FastAPI: A modern, fast web framework used for building the API endpoints.

Uvicorn: An ASGI server used to run the FastAPI application.

HTML, CSS, JavaScript: Used to create a simple, local user interface for manual interaction with the battle simulation tool.

Workflow
The project's workflow is centered around providing structured capabilities to an external AI.

Request from AI/User: An AI or a human user sends a request to one of the server's API endpoints.

Server Processing: The FastAPI server receives the request. For a battle simulation, it calls the core logic from battle_logic.py.

Simulation Engine: The battle_logic.py module processes the request, retrieves Pokémon data, runs the battle simulation (including turn order, damage calculation, and status effects), and generates a detailed log.

Response: The server returns the result of the operation as a structured JSON response, which the AI or user can then interpret and use.

Setup and Running the Code
Follow these steps to set up and run the project locally.

Prerequisites
Python 3.7+

pip (Python package installer)

Installation
Navigate to the project directory in your terminal.

python -m venv venv 
venv\Scripts\activate

Install the necessary Python dependencies:
 pip install "fastapi[all]" uvicorn

Running the Server
Start the server from your terminal using Uvicorn. Ensure your virtual environment is active.

uvicorn main:app --reload

The server will start at http://127.0.0.1:8000. 

How to Use the API
The server exposes its capabilities through the MCP manifest and dedicated API endpoints.

1. MCP Manifest
Method: GET

URL: http://127.0.0.1:8000/.well-known/mcp/manifest.json

Returns the manifest.json file that details the server's tools and resources.

2. Pokémon Data Resource
Method: GET

URL: http://127.0.0.1:8000/v1/resources/pokemon_data_resource/get?pokemon_name={name}

Retrieves detailed information for a specified Pokémon.

Example (Terminal):

curl "http://127.0.0.1:8000/v1/resources/pokemon_data_resource/get?pokemon_name=charizard"

3. Battle Simulation Tool
Method: POST

URL: http://127.0.0.1:8000/v1/tools/battle_simulation_tool/run

Description: Runs a battle simulation between two Pokémon and returns a detailed log.

Example (run this in Terminal):

irm http://localhost:8080/tools/battle_sim -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"pokemon1": "pikachu", "pokemon2": "charmander"}'

4. Local User Interface
The UI is a separate index.html file located in the project's root directory.

After running the main.py using "pip install "fastapi[all]" uvicorn" successfully then start running index.html locally

How to Run: Simply open index.html in your web browser after the server is running. The UI will automatically connect to your server to retrieve data and run simulations.