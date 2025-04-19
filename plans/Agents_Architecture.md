# Generative Agents Architecture: Deep Dive & Porting Guide

This folder contains the core backend server code from the "Generative Agents" project, along with this detailed guide to help you understand and port the architecture to your own simulation projects (like your Office-themed simulation).

## 1. Core Architecture Overview

### Agent Cognitive Loop

The heart of the system is the agent cognitive loop in `persona.py`:

```
perceive → retrieve → plan → execute → reflect
```

Each agent (persona) follows this loop to:
1. **Perceive** the environment around them
2. **Retrieve** relevant memories based on what they perceive
3. **Plan** their next actions (both short and long-term)
4. **Execute** those plans as concrete movements and interactions
5. **Reflect** on their experiences to form higher-level thoughts

### Memory System

Agents have three memory structures:
- **Spatial Memory** (`spatial_memory.py`): A tree representing the agent's knowledge of the world's physical layout
- **Associative Memory** (`associative_memory.py`): Long-term memory of events, thoughts, and interactions
- **Scratch** (`scratch.py`): Short-term working memory for current state and plans

### Communication Between Frontend & Backend

The original architecture uses a two-server approach with file-based communication:

1. **Backend → Frontend Communication:**
   - Backend writes JSON movement files to `{sim_folder}/movement/{step}.json`
   - These files contain next positions, actions, and descriptions for each agent
   - Frontend reads these files to animate agents accordingly

2. **Frontend → Backend Communication:**
   - Frontend writes environment state to `{sim_folder}/environment/{step}.json`
   - These files contain current positions of all agents
   - Backend reads these files to update its internal state

3. **JSON Structure Examples:**
   - **Movement JSON** (Backend → Frontend):
     ```json
     {
       "persona": {
         "Isabella Rodriguez": {
           "movement": [58, 9],
           "pronunciatio": "📝",
           "description": "writing her next novel @ double studio:common room:sofa",
           "chat": [["Isabella", "I'm working on my novel"], ["Maria", "That sounds interesting"]]
         },
         "Klaus Mueller": {
           "movement": [38, 12],
           "pronunciatio": "🔬",
           "description": "researching gentrification @ school:library:desk",
           "chat": null
         }
       },
       "meta": {
         "curr_time": "February 13, 2023, 14:30:00"
       }
     }
     ```
   - **Environment JSON** (Frontend → Backend):
     ```json
     {
       "Isabella Rodriguez": {
         "x": 58,
         "y": 9
       },
       "Klaus Mueller": {
         "x": 38,
         "y": 12
       }
     }
     ```

## 2. Porting to a Single-Server Architecture

### Why the Original Uses Two Servers

The original architecture separates frontend and backend for several reasons:
- **Research Focus**: Allows running the simulation headless for experiments
- **Language Separation**: Backend in Python (for AI/ML), frontend in JS (for visualization)
- **Modularity**: Can swap frontends or run multiple simulations with one backend

### Single-Server Approach

For your Office simulation, a single-server approach makes more sense:
- **Simpler Setup**: One server handles both simulation logic and visualization
- **Real-Time Communication**: Direct function calls or websockets instead of files
- **Easier Deployment**: Package as a single application (e.g., with Electron)

### Implementation Strategy

1. **Keep the Agent Architecture Intact**:
   - The `persona.py` cognitive loop and memory systems can remain largely unchanged
   - The core agent logic is independent of the communication method

2. **Replace File-Based Communication**:
   - Instead of writing/reading JSON files, use direct function calls or websockets
   - For a Python backend with JS frontend, use websockets or REST APIs

3. **Simplify the Simulation Loop**:
   - Remove the file checking and waiting in `reverie.py`'s `start_server` method
   - Replace with a direct update cycle that pushes changes to the frontend

4. **JSON Structure**:
   - Keep the same JSON structure for consistency, but transmit via websockets
   - Example websocket implementation:

```python
# Backend (Python with FastAPI)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive environment state from frontend
        env_data = await websocket.receive_json()
        
        # Process agent decisions (similar to reverie.py's start_server)
        movements = process_agent_decisions(env_data)
        
        # Send movement data to frontend
        await websocket.send_json(movements)
```

```javascript
// Frontend (JavaScript with Phaser)
const socket = new WebSocket('ws://localhost:8000/ws');

socket.onopen = () => {
    // Send initial environment state
    sendEnvironmentState();
};

socket.onmessage = (event) => {
    const movements = JSON.parse(event.data);
    // Update agent positions and animations based on movements
    updateAgents(movements);
};

function sendEnvironmentState() {
    const envData = {
        "Isabella Rodriguez": {
            "x": currentX,
            "y": currentY
        },
        // Other agents...
    };
    socket.send(JSON.stringify(envData));
}
```

## 3. Key Files & Their Roles

### Core Agent Logic

- **`persona/persona.py`**: Main agent class with the cognitive loop
  - **How to Port**: Keep intact, modify the `move` method to work with your communication system
  - **Dependencies**: Imports from `cognitive_modules` and `memory_structures`

- **`persona/cognitive_modules/`**: Contains the implementation of each step in the cognitive loop
  - **perceive.py**: How agents observe their environment
  - **retrieve.py**: How agents recall relevant memories
  - **plan.py**: How agents make decisions
  - **execute.py**: How agents turn plans into actions
  - **reflect.py**: How agents form higher-level thoughts
  - **How to Port**: Keep intact, but you may need to modify environment perception

- **`persona/memory_structures/`**: Contains the agent's memory systems
  - **associative_memory.py**: Long-term memory
  - **spatial_memory.py**: Knowledge of the world
  - **scratch.py**: Short-term working memory
  - **How to Port**: Keep intact, but you may need to modify spatial memory for your map

### Environment & Simulation

- **`maze.py`**: Represents the world, handles collision and events
  - **How to Port**: Adapt to your office map, but keep the core interface
  - **Key Methods**: `access_tile`, `get_nearby_tiles`, `add_event_from_tile`

- **`path_finder.py`**: Handles agent movement and pathfinding
  - **How to Port**: Keep intact if using a similar tile-based system

- **`reverie.py`**: Main simulation server
  - **How to Port**: Heavily modify to use websockets/REST instead of files
  - **Key Method**: `start_server` - replace file I/O with direct communication

## 4. Specific Porting Steps for Your Office Simulation

1. **Set Up Your Server**:
   ```python
   # app.py
   from fastapi import FastAPI, WebSocket
   from fastapi.staticfiles import StaticFiles
   import uvicorn
   import json
   
   # Import your ported reverie components
   from backend_server.reverie import ReverieServer
   
   app = FastAPI()
   
   # Serve static files (your Phaser frontend)
   app.mount("/static", StaticFiles(directory="static"), name="static")
   
   # Create your simulation server
   reverie = ReverieServer("office_simulation", "current_session")
   
   @app.websocket("/ws")
   async def websocket_endpoint(websocket: WebSocket):
       await websocket.accept()
       while True:
           # Receive environment state
           env_data = await websocket.receive_json()
           
           # Process agent decisions (similar to reverie.py's start_server)
           movements = process_agent_decisions(env_data)
           
           # Send movement data
           await websocket.send_json(movements)
   
   def process_agent_decisions(env_data):
       # Similar logic to reverie.py's start_server method
       # but without file I/O
       movements = {"persona": {}, "meta": {}}
       
       # Update agent positions
       for persona_name, persona in reverie.personas.items():
           # Update position based on env_data
           # ...
           
           # Get next move
           next_tile, pronunciatio, description = persona.move(
               reverie.maze, reverie.personas, 
               (env_data[persona_name]["x"], env_data[persona_name]["y"]), 
               reverie.curr_time)
           
           # Add to movements
           movements["persona"][persona_name] = {
               "movement": next_tile,
               "pronunciatio": pronunciatio,
               "description": description,
               "chat": persona.scratch.chat
           }
       
       # Add meta information
       movements["meta"]["curr_time"] = reverie.curr_time.strftime("%B %d, %Y, %H:%M:%S")
       
       return movements
   
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

2. **Modify Your Phaser Frontend**:
   ```javascript
   // In your Phaser game code
   
   // Connect to backend
   const socket = new WebSocket('ws://localhost:8000/ws');
   
   // When connection opens
   socket.onopen = () => {
       // Send initial environment state
       sendEnvironmentState();
   };
   
   // When receiving updates from backend
   socket.onmessage = (event) => {
       const movements = JSON.parse(event.data);
       updateAgents(movements);
   };
   
   // Send current environment state
   function sendEnvironmentState() {
       const envData = {};
       
       // Add each agent's position
       for (const personaName in personas) {
           envData[personaName] = {
               x: Math.ceil(personas[personaName].body.x / tile_width),
               y: Math.ceil(personas[personaName].body.y / tile_width)
           };
       }
       
       socket.send(JSON.stringify(envData));
   }
   
   // Update agent positions and animations
   function updateAgents(movements) {
       for (const personaName in movements.persona) {
           const movement = movements.persona[personaName];
           
           // Set target position
           movement_target[personaName] = [
               movement.movement[0] * tile_width,
               movement.movement[1] * tile_width
           ];
           
           // Update speech bubble
           pronunciatios[personaName].setText(movement.pronunciatio);
           
           // Start animation sequence
           // (Similar to the original main_script.html)
       }
       
       // Update game time
       document.getElementById("game-time-content").innerHTML = movements.meta.curr_time;
   }
   ```

3. **Package with Electron**:
   ```javascript
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
       
       mainWindow.loadFile('static/index.html');
       
       mainWindow.on('closed', function() {
           mainWindow = null;
           if (pythonProcess) {
               pythonProcess.kill();
           }
       });
   }
   
   app.on('ready', () => {
       // Start Python backend
       pythonProcess = spawn('python', ['app.py']);
       
       // Log Python output
       pythonProcess.stdout.on('data', (data) => {
           console.log(`Python: ${data}`);
       });
       
       // Create window
       createWindow();
   });
   
   app.on('window-all-closed', () => {
       if (process.platform !== 'darwin') {
           app.quit();
       }
   });
   ```

## 5. Testing Different Agent Architectures

One of your goals is to test different agent architectures. Here's how to structure your code for easy swapping:

1. **Create an Agent Interface**:
   ```python
   # agent_interface.py
   class AgentInterface:
       def perceive(self, environment):
           """Process perceptions from the environment"""
           pass
           
       def decide(self, perceptions):
           """Make decisions based on perceptions"""
           pass
           
       def act(self, decision):
           """Convert decisions to concrete actions"""
           pass
   ```

2. **Implement Different Agent Types**:
   ```python
   # reverie_agent.py
   class ReverieAgent(AgentInterface):
       """Original Generative Agents architecture"""
       def __init__(self, name, folder_mem_saved=False):
           self.persona = Persona(name, folder_mem_saved)
           
       def perceive(self, environment):
           return self.persona.perceive(environment)
           
       def decide(self, perceptions):
           retrieved = self.persona.retrieve(perceptions)
           plan = self.persona.plan(environment, personas, new_day, retrieved)
           self.persona.reflect()
           return plan
           
       def act(self, decision):
           return self.persona.execute(environment, personas, decision)
   
   # new_architecture_agent.py
   class NewArchitectureAgent(AgentInterface):
       """Your new experimental architecture"""
       # Implement the interface with your new approach
   ```

3. **Swap Implementations in Your Server**:
   ```python
   # In your server code
   
   # Choose which agent architecture to use
   agent_type = "reverie"  # or "new_architecture"
   
   # Create agents based on type
   if agent_type == "reverie":
       agents = {name: ReverieAgent(name) for name in agent_names}
   elif agent_type == "new_architecture":
       agents = {name: NewArchitectureAgent(name) for name in agent_names}
   ```

This approach lets you experiment with different agent architectures while keeping the same frontend and communication system.

## Conclusion

The Generative Agents architecture is powerful but was designed with research in mind, not ease of use or deployment. By porting it to a single-server architecture with modern communication methods, you can maintain its strengths while making it more approachable and easier to extend.

The key is to preserve the cognitive loop and memory systems while replacing the file-based communication with direct function calls or websockets. This will give you a solid foundation for your Office simulation that you can easily extend with new agent architectures as you explore the field.
