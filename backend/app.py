"""
Office Agent Simulation - Backend Server

This is the main entry point for the FastAPI backend server that powers the
Office Agent Simulation. It implements a WebSocket endpoint for real-time
communication with the Phaser.js frontend.

The server manages the agent cognitive loop, environment state, and simulation logic.
"""

import json
import datetime
import asyncio
from typing import Dict, Any, List, Tuple

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from maze import Maze
# from path_finder import path_finder
# from persona.persona import Persona

# Create FastAPI app
app = FastAPI(
    title="Office Agent Simulation",
    description="Backend server for the Office Agent Simulation",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Simulation state
class SimulationState:
    def __init__(self, maze_name: str = "office"):
        # Set the path to the office map/matrix
        env_matrix = "frontend/assets/the_office/matrix"
        self.maze = Maze(maze_name, env_matrix)
        self.personas = {}  # name -> Persona (placeholder for now)
        self.personas_tile = {
            "Alice": (0, 3),
            "Bob": (1, 3)
        }
        self.step = 0
        self.curr_time = datetime.datetime.now()
        self.sec_per_step = 60  # 1 minute per step

    def process_environment(self, env_data: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """
        Process the environment data from the frontend and generate movements

        Args:
            env_data: Dictionary mapping persona names to their positions
                      e.g., {"Alice": {"x": 0, "y": 3}, "Bob": {"x": 1, "y": 3}}

        Returns:
            Dictionary with movement instructions for each persona
        """
        # For now, move Alice and Bob one tile to the right each step (demo logic)
        movements = {"persona": {}, "meta": {}}
        for name, pos in self.personas_tile.items():
            new_x = pos[0] + 1 if pos[0] + 1 < self.maze.maze_width else pos[0]
            new_y = pos[1]
            self.personas_tile[name] = (new_x, new_y)
            movements["persona"][name] = {
                "movement": [new_x, new_y],
                "pronunciatio": "💼" if name == "Alice" else "🗂️",
                "description": f"{name} is walking in the office.",
                "chat": None
            }
        movements["meta"]["curr_time"] = self.curr_time.strftime("%B %d, %Y, %H:%M:%S")
        self.step += 1
        self.curr_time += datetime.timedelta(seconds=self.sec_per_step)
        return movements

# Create simulation state
simulation = SimulationState()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Office Agent Simulation Backend Server"}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive environment data from frontend
            env_data = await websocket.receive_json()
            
            # Process agent decisions
            movements = simulation.process_environment(env_data)
            
            # Send movement data back to frontend
            await websocket.send_json(movements)
            
            # Small delay to prevent overwhelming the connection
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
