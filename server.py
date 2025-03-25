import asyncio
import json
import random
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = {
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "values": random.uniform(-1, 1),  # Simulating ECG signal
                "sdnn": random.uniform(30, 50),
                "rmssd": random.uniform(20, 40)
            }
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(1)  # Send data every second
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
