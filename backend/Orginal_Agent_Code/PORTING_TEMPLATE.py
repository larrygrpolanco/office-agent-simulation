"""
PORTING_TEMPLATE.py

This file provides a template for porting the Generative Agents architecture
to a single-server setup using FastAPI and websockets. This is a starting point
that you can adapt for your Office simulation.

Key changes from the original architecture:
1. Replaces file-based communication with websockets
2. Runs both backend and frontend from a single server
3. Maintains the same JSON structure for compatibility

Usage:
1. Install dependencies: pip install fastapi uvicorn websockets
2. Adapt this template to your needs
3. Run with: uvicorn PORTING_TEMPLATE:app --reload
4. Connect your Phaser frontend to the websocket endpoint
"""

import json
import datetime
import asyncio
from typing import Dict, Any, List, Tuple

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Import your ported reverie components
# Adjust these imports based on your folder structure
from backend_server.maze import Maze
from backend_server.persona.persona import Persona

# Create FastAPI app
app = FastAPI(title="Office Simulation")

# Serve static files (your Phaser frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML page that loads your Phaser game
@app.get("/")
async def get():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Office Simulation</title>
            <script src="/static/phaser.min.js"></script>
            <script src="/static/game.js"></script>
        </head>
        <body>
            <div id="game-container"></div>
        </body>
    </html>
    """)

# Simulation state
class SimulationState:
    def __init__(self, maze_name: str = "office"):
        # Initialize simulation state
        self.maze = Maze(maze_name)
        self.personas = {}  # name -> Persona
        self.personas_tile = {}  # name -> (x, y)
        self.step = 0
        self.curr_time = datetime.datetime.now()
        self.sec_per_step = 60  # 1 minute per step
        
        # Initialize personas
        # In a real implementation, you would load these from a configuration
        self.init_personas()
    
    def init_personas(self):
        """Initialize personas with their starting positions"""
        # Example: Create a few personas
        persona_configs = [
            {"name": "Michael Scott", "position": (10, 15)},
            {"name": "Jim Halpert", "position": (12, 18)},
            {"name": "Pam Beesly", "position": (15, 18)},
            {"name": "Dwight Schrute", "position": (8, 12)}
        ]
        
        for config in persona_configs:
            name = config["name"]
            position = config["position"]
            
            # Create persona (in a real implementation, you would load from a file)
            self.personas[name] = Persona(name)
            self.personas_tile[name] = position
            
            # Add persona to the maze
            self.maze.add_event_from_tile(
                self.personas[name].scratch.get_curr_event_and_desc(), 
                position
            )
    
    def process_environment(self, env_data: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """
        Process the environment data from the frontend and generate movements
        
        This replaces the file-based communication in reverie.py's start_server method
        
        Args:
            env_data: Dictionary mapping persona names to their positions
                      e.g., {"Michael Scott": {"x": 10, "y": 15}}
        
        Returns:
            Dictionary with movement instructions for each persona
        """
        # Initialize movements dictionary
        movements = {"persona": {}, "meta": {}}
        
        # Update persona positions based on environment data
        for persona_name, persona in self.personas.items():
            if persona_name in env_data:
                # Get current and new positions
                curr_tile = self.personas_tile[persona_name]
                new_tile = (env_data[persona_name]["x"], env_data[persona_name]["y"])
                
                # Update position in our internal state
                self.personas_tile[persona_name] = new_tile
                
                # Update the maze (remove from old position, add to new)
                self.maze.remove_subject_events_from_tile(persona.name, curr_tile)
                self.maze.add_event_from_tile(
                    persona.scratch.get_curr_event_and_desc(), 
                    new_tile
                )
        
        # Generate next moves for each persona
        for persona_name, persona in self.personas.items():
            # Get the persona's current position
            curr_tile = self.personas_tile[persona_name]
            
            # Run the cognitive loop to get the next move
            next_tile, pronunciatio, description = persona.move(
                self.maze, 
                self.personas, 
                curr_tile, 
                self.curr_time
            )
            
            # Add to movements dictionary
            movements["persona"][persona_name] = {
                "movement": next_tile,
                "pronunciatio": pronunciatio,
                "description": description,
                "chat": persona.scratch.chat
            }
        
        # Add meta information
        movements["meta"]["curr_time"] = self.curr_time.strftime("%B %d, %Y, %H:%M:%S")
        
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

# Example of how to use this with Electron
"""
// main.js (Electron entry point)
const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let pythonProcess;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1500,
        height: 800,
        webPreferences: {
            nodeIntegration: true
        }
    });
    
    mainWindow.loadURL('http://localhost:8000');
    
    mainWindow.on('closed', function() {
        mainWindow = null;
        if (pythonProcess) {
            pythonProcess.kill();
        }
    });
}

app.on('ready', () => {
    // Start Python backend
    pythonProcess = spawn('python', ['-m', 'uvicorn', 'PORTING_TEMPLATE:app', '--host', '0.0.0.0', '--port', '8000']);
    
    // Log Python output
    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python: ${data}`);
    });
    
    // Create window after a short delay to ensure server is running
    setTimeout(createWindow, 1000);
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
"""

# Example of how to connect from Phaser
"""
// In your Phaser game code (game.js)

// Game configuration
const config = {
    type: Phaser.AUTO,
    width: 1500,
    height: 800,
    parent: "game-container",
    pixelArt: true,
    physics: {
        default: "arcade",
        arcade: {
            gravity: { y: 0 }
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

// Create game
const game = new Phaser.Game(config);

// Variables
let personas = {};
let pronunciatios = {};
let movement_target = {};
let tile_width = 32;
let socket;

function preload() {
    // Load assets
    this.load.image("tiles", "/static/assets/office_tileset.png");
    this.load.tilemapTiledJSON("map", "/static/assets/office_map.json");
    this.load.atlas("atlas", "/static/assets/atlas.png", "/static/assets/atlas.json");
}

function create() {
    // Create map
    const map = this.make.tilemap({ key: "map" });
    const tileset = map.addTilesetImage("office_tileset", "tiles");
    
    // Create layers
    const floorLayer = map.createLayer("Floor", tileset, 0, 0);
    const wallsLayer = map.createLayer("Walls", tileset, 0, 0);
    const furnitureLayer = map.createLayer("Furniture", tileset, 0, 0);
    
    // Set collision
    wallsLayer.setCollisionByProperty({ collides: true });
    furnitureLayer.setCollisionByProperty({ collides: true });
    
    // Create personas
    const personaConfigs = [
        { name: "Michael Scott", x: 10, y: 15 },
        { name: "Jim Halpert", x: 12, y: 18 },
        { name: "Pam Beesly", x: 15, y: 18 },
        { name: "Dwight Schrute", x: 8, y: 12 }
    ];
    
    for (const config of personaConfigs) {
        const x = config.x * tile_width + tile_width / 2;
        const y = config.y * tile_width + tile_width;
        
        // Create sprite
        const sprite = this.physics.add
            .sprite(x, y, "atlas", "misa-front")
            .setSize(30, 40)
            .setOffset(0, 24);
        
        // Add to personas dictionary
        personas[config.name] = sprite;
        
        // Create speech bubble
        pronunciatios[config.name] = this.add.text(
            sprite.body.x - 6,
            sprite.body.y - 42,
            "💼",
            {
                font: "28px monospace",
                fill: "#000000",
                padding: { x: 8, y: 8 },
                backgroundColor: "#ffffff",
                border: "solid",
                borderRadius: "10px"
            }
        ).setDepth(3);
    }
    
    // Create animations
    const anims = this.anims;
    anims.create({
        key: "misa-left-walk",
        frames: anims.generateFrameNames("atlas", { prefix: "misa-left-walk.", start: 0, end: 3, zeroPad: 3 }),
        frameRate: 4,
        repeat: -1
    });
    
    anims.create({
        key: "misa-right-walk",
        frames: anims.generateFrameNames("atlas", { prefix: "misa-right-walk.", start: 0, end: 3, zeroPad: 3 }),
        frameRate: 4,
        repeat: -1
    });
    
    anims.create({
        key: "misa-front-walk",
        frames: anims.generateFrameNames("atlas", { prefix: "misa-front-walk.", start: 0, end: 3, zeroPad: 3 }),
        frameRate: 4,
        repeat: -1
    });
    
    anims.create({
        key: "misa-back-walk",
        frames: anims.generateFrameNames("atlas", { prefix: "misa-back-walk.", start: 0, end: 3, zeroPad: 3 }),
        frameRate: 4,
        repeat: -1
    });
    
    // Connect to WebSocket
    socket = new WebSocket(`ws://${window.location.host}/ws`);
    
    socket.onopen = () => {
        console.log("WebSocket connection established");
        sendEnvironmentState();
    };
    
    socket.onmessage = (event) => {
        const movements = JSON.parse(event.data);
        updateAgents(movements);
    };
    
    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };
    
    socket.onclose = () => {
        console.log("WebSocket connection closed");
    };
}

function update() {
    // Move personas towards their targets
    for (const personaName in personas) {
        const persona = personas[personaName];
        const pronunciatio = pronunciatios[personaName];
        
        if (movement_target[personaName]) {
            // Calculate direction
            const targetX = movement_target[personaName][0];
            const targetY = movement_target[personaName][1];
            
            // Move towards target
            const speed = 2;
            let anims_direction = "";
            
            if (Math.abs(persona.body.x - targetX) > speed) {
                if (persona.body.x < targetX) {
                    persona.body.x += speed;
                    anims_direction = "r";
                } else {
                    persona.body.x -= speed;
                    anims_direction = "l";
                }
            }
            
            if (Math.abs(persona.body.y - targetY) > speed) {
                if (persona.body.y < targetY) {
                    persona.body.y += speed;
                    anims_direction = "d";
                } else {
                    persona.body.y -= speed;
                    anims_direction = "u";
                }
            }
            
            // Update speech bubble position
            pronunciatio.x = persona.body.x - 6;
            pronunciatio.y = persona.body.y - 42;
            
            // Play appropriate animation
            if (anims_direction === "l") {
                persona.anims.play("misa-left-walk", true);
            } else if (anims_direction === "r") {
                persona.anims.play("misa-right-walk", true);
            } else if (anims_direction === "u") {
                persona.anims.play("misa-back-walk", true);
            } else if (anims_direction === "d") {
                persona.anims.play("misa-front-walk", true);
            } else {
                persona.anims.stop();
                
                // Set idle frame based on last direction
                if (persona.anims.currentAnim) {
                    const key = persona.anims.currentAnim.key;
                    if (key === "misa-left-walk") persona.setTexture("atlas", "misa-left");
                    else if (key === "misa-right-walk") persona.setTexture("atlas", "misa-right");
                    else if (key === "misa-back-walk") persona.setTexture("atlas", "misa-back");
                    else if (key === "misa-front-walk") persona.setTexture("atlas", "misa-front");
                }
            }
        }
    }
}

// Send current environment state to backend
function sendEnvironmentState() {
    if (socket.readyState === WebSocket.OPEN) {
        const envData = {};
        
        // Add each persona's position
        for (const personaName in personas) {
            const persona = personas[personaName];
            
            envData[personaName] = {
                x: Math.ceil(persona.body.x / tile_width),
                y: Math.ceil(persona.body.y / tile_width)
            };
        }
        
        socket.send(JSON.stringify(envData));
    }
    
    // Schedule next update
    setTimeout(sendEnvironmentState, 1000);
}

// Update agent positions and animations based on backend data
function updateAgents(movements) {
    for (const personaName in movements.persona) {
        if (personaName in personas) {
            const movement = movements.persona[personaName];
            
            // Set target position
            movement_target[personaName] = [
                movement.movement[0] * tile_width,
                movement.movement[1] * tile_width
            ];
            
            // Update speech bubble
            if (movement.pronunciatio) {
                pronunciatios[personaName].setText(movement.pronunciatio);
            }
        }
    }
    
    // Update game time if there's an element for it
    const timeElement = document.getElementById("game-time-content");
    if (timeElement && movements.meta && movements.meta.curr_time) {
        timeElement.innerHTML = movements.meta.curr_time;
    }
}
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
