# main.py

from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

# Directory to store received data
DATA_DIR = "received_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Mock API key for authentication
MOCK_API_KEY = "test-api-key"

@app.post("/api/v1/agent/data")
async def receive_data(request: Request, authorization: str = Header(None)):
    if authorization != f"Bearer {MOCK_API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    # Save the received data to a file for inspection
    filename = os.path.join(DATA_DIR, "agent_data.json")
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print("Data received and saved.")
    return JSONResponse(content={"status": "success"}, status_code=200)