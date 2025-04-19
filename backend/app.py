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

# Import simulation components (to be implemented)
# from maze import Maze
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
        # Initialize simulation state
        # self.maze = Maze(maze_name)  # Uncomment when implemented
        self.maze = None  # Placeholder
        self.personas = {}  # name -> Persona
        self.personas_tile = {}  # name -> (x, y)
        self.step = 0
        self.curr_time = datetime.datetime.now()
        self.sec_per_step = 60  # 1 minute per step
        
        # Initialize personas (placeholder)
        # self.init_personas()
    
    def init_personas(self):
        """Initialize personas with their starting positions"""
        # Example: Create a few personas
        persona_configs = [
            {"name": "Michael Scott", "position": (10, 15)},
            {"name": "Jim Halpert", "position": (12, 18)},
            {"name": "Pam Beesly", "position": (15, 18)},
            {"name": "Dwight Schrute", "position": (8, 12)}
        ]
        
        # Placeholder - will be implemented later
        pass
    
    def process_environment(self, env_data: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """
        Process the environment data from the frontend and generate movements
        
        Args:
            env_data: Dictionary mapping persona names to their positions
                      e.g., {"Michael Scott": {"x": 10, "y": 15}}
        
        Returns:
            Dictionary with movement instructions for each persona
        """
        # Placeholder implementation - returns mock data
        movements = {
            "persona": {
                "Michael Scott": {
                    "movement": [11, 15],
                    "pronunciatio": "📋",
                    "description": "reviewing quarterly reports @ office:manager_office:desk",
                    "chat": None
                },
                "Jim Halpert": {
                    "movement": [13, 18],
                    "pronunciatio": "💻",
                    "description": "working on sales report @ office:sales_area:desk",
                    "chat": None
                }
            },
            "meta": {
                "curr_time": self.curr_time.strftime("%B %d, %Y, %H:%M:%S")
            }
        }
        
        # Update simulation state
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
