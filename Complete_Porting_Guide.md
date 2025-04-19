# Complete Porting Guide: Generative Agents Simulation (FastAPI + Phaser + Electron)

This guide provides a comprehensive roadmap for porting the Generative Agents system to a modern, simplified architecture using a FastAPI backend, a Phaser.js frontend, and Electron for desktop packaging. The focus is on replicating the core generative agent architecture and environment structure, then connecting them with real-time communication, and preparing for future UI improvements (e.g., React).

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Project Roadmap](#2-project-roadmap)
3. [Map Creation & Representation](#3-map-creation--representation)
4. [Backend Setup (FastAPI)](#4-backend-setup-fastapi)
5. [Frontend Setup (Phaser.js)](#5-frontend-setup-phaserjs)
6. [Agent Cognition & Behavior](#6-agent-cognition--behavior)
7. [Frontend-Backend Communication](#7-frontend-backend-communication)
8. [Testing & Debugging](#8-testing--debugging)
9. [Packaging with Electron](#9-packaging-with-electron)
10. [Advanced Customization & Next Steps](#10-advanced-customization--next-steps)

---

## 1. System Architecture Overview

The new architecture consists of:

- **Backend (Python, FastAPI):**
  - Implements the agent cognitive loop (perceive → retrieve → plan → execute → reflect)
  - Manages agent memory systems and world state
  - Exposes a WebSocket (or REST) API for real-time communication with the frontend

- **Frontend (Phaser.js):**
  - Renders the map and agents
  - Handles user interaction and visualization
  - Communicates with the backend via WebSocket

- **Electron (Optional):**
  - Packages the backend and frontend into a desktop application

**Key Change:**  
All communication is real-time (WebSocket), not file-based. The backend and frontend can be run as a single application, simplifying deployment and development.

---

## 2. Project Roadmap

**Recommended sequence for porting:**

1. **Replicate Core Agent Architecture:**  
   Port the cognitive loop and memory systems from the original project, keeping the logic modular and backend-agnostic.

2. **Design & Export Your Map:**  
   Use Tiled Map Editor to create your environment, export both visual (TMX/JSON) and backend (CSV/JSON) data.

3. **Implement FastAPI Backend:**  
   Set up FastAPI, integrate the agent logic, and expose a WebSocket endpoint for real-time simulation.

4. **Build Phaser Frontend:**  
   Set up Phaser to load your map, display agents, and handle real-time updates from the backend.

5. **Connect Frontend & Backend:**  
   Implement the WebSocket protocol for sending environment state and receiving agent actions/movements.

6. **Test & Refine:**  
   Run the simulation, debug, and iterate on both agent logic and visualization.

7. **Package with Electron:**  
   Bundle the backend and frontend for easy desktop deployment.

---

## 3. Map Creation & Representation

### Step 1: Design Your Map in Tiled

- Download [Tiled Map Editor](https://www.mapeditor.org/)
- Create a new map (e.g., 50x40 tiles, 32x32 pixels)
- Import tilesets for your environment (office, home, etc.)
- Create visual layers (floors, walls, furniture, etc.)

### Step 2: Create Data Layers for Backend

- Add layers for collision, sectors, arenas, objects, and spawn points using a simple colored tileset
- Assign unique IDs (GIDs) for each type (see [Map_and_Movement_Porting_Guide.md](Map_and_Movement_Porting_Guide.md) for details)
- Export each data layer as CSV for backend use
- Create legend files mapping IDs to names
- Create a metadata JSON with map info

### Step 3: Organize Files

```
assets/
├── matrix/
│   ├── maze/
│   │   ├── collision_maze.csv
│   │   ├── sector_maze.csv
│   │   ├── arena_maze.csv
│   │   ├── game_object_maze.csv
│   │   └── spawning_location_maze.csv
│   ├── special_blocks/
│   │   ├── world_blocks.csv
│   │   ├── sector_blocks.csv
│   │   ├── arena_blocks.csv
│   │   ├── game_object_blocks.csv
│   │   └── spawning_location_blocks.csv
│   └── maze_meta_info.json
└── visuals/
    └── office.tmx
```

---

## 4. Backend Setup (FastAPI)

### Step 1: Set Up FastAPI

- Install FastAPI and Uvicorn:
  ```
  pip install fastapi uvicorn
  ```

- Create `app.py` with a WebSocket endpoint:
  ```python
  from fastapi import FastAPI, WebSocket
  from fastapi.staticfiles import StaticFiles
  import uvicorn

  app = FastAPI()
  app.mount("/static", StaticFiles(directory="static"), name="static")

  @app.websocket("/ws")
  async def websocket_endpoint(websocket: WebSocket):
      await websocket.accept()
      while True:
          env_data = await websocket.receive_json()
          movements = process_agent_decisions(env_data)
          await websocket.send_json(movements)
  ```

- Implement `process_agent_decisions` to run the agent cognitive loop and return agent actions in the expected JSON format.

### Step 2: Integrate Agent Logic

- Port the core agent classes and memory systems (see `Agents_Architecture.md`)
- Keep the cognitive loop and memory logic modular
- Adapt environment perception and movement to your new map structure

### Step 3: Map Loading

- Load your exported CSV/JSON map data on backend startup
- Build the world representation and address lookup tables

---

## 5. Frontend Setup (Phaser.js)

### Step 1: Set Up Phaser

- Use Phaser 3 (CDN or npm)
- Load your map (JSON from Tiled) and tilesets in the `preload()` function
- Create map layers and agent sprites in `create()`
- Implement camera, controls, and UI as needed

### Step 2: WebSocket Communication

- Connect to the backend WebSocket:
  ```javascript
  const socket = new WebSocket('ws://localhost:8000/ws');
  socket.onopen = () => { sendEnvironmentState(); };
  socket.onmessage = (event) => { updateAgents(JSON.parse(event.data)); };
  ```

- Implement `sendEnvironmentState()` to send current agent positions
- Implement `updateAgents()` to animate agents based on backend response

### Step 3: Pronunciatio System

- Display agent status/emojis above each agent
- Customize the backend prompt for office-appropriate actions/emojis

---

## 6. Agent Cognition & Behavior

- The agent cognitive loop remains as in the original architecture:
  1. **Perceive**: Observe environment and other agents
  2. **Retrieve**: Recall relevant memories
  3. **Plan**: Decide next actions
  4. **Execute**: Move and interact
  5. **Reflect**: Form higher-level thoughts

- Customize planning, execution, and reflection modules for your environment and desired behaviors
- Use the same JSON structure for agent actions as in the original project, but transmit via WebSocket

---

## 7. Frontend-Backend Communication

- **WebSocket Protocol:**
  - Frontend sends environment state (agent positions, etc.) as JSON
  - Backend processes and returns agent actions/movements as JSON
  - Example movement JSON:
    ```json
    {
      "persona": {
        "Alice": {
          "movement": [10, 5],
          "pronunciatio": "💻",
          "description": "typing code at her desk",
          "chat": null
        }
      },
      "meta": {
        "curr_time": "April 19, 2025, 09:00:00"
      }
    }
    ```

- **No file-based communication is needed.**

---

## 8. Testing & Debugging

- Use print/logging in backend to trace agent decisions
- Use browser dev tools to debug frontend
- Test map loading, agent movement, and communication step by step
- Use a path tester or debug overlay in Phaser to visualize walkability and agent paths

---

## 9. Packaging with Electron

- Use Electron to bundle the backend and frontend into a desktop app
- Start the FastAPI backend as a subprocess from Electron’s main process
- Load the frontend in an Electron BrowserWindow
- Example Electron main process:
  ```javascript
  const { app, BrowserWindow } = require('electron');
  const { spawn } = require('child_process');
  let mainWindow, pythonProcess;
  function createWindow() {
      mainWindow = new BrowserWindow({ width: 1500, height: 800 });
      mainWindow.loadFile('static/index.html');
      mainWindow.on('closed', () => { if (pythonProcess) pythonProcess.kill(); });
  }
  app.on('ready', () => {
      pythonProcess = spawn('python', ['app.py']);
      createWindow();
  });
  ```

---

## 10. Advanced Customization & Next Steps

- **Experiment with Agent Architectures:**  
  Implement an agent interface and swap different agent logic modules for research or feature development.

- **Add React UI (Optional):**  
  After core simulation is stable, incrementally add React components for richer UI/UX.

- **Performance Optimization:**  
  Optimize map rendering, agent animation, and backend processing for larger simulations.

- **Cloud or Multi-User Deployment:**  
  Adapt the backend for cloud hosting or multi-user scenarios if needed.

---

## References

- [Agents_Architecture.md](Agents_Architecture.md): Deep dive into the cognitive loop and porting strategy
- [Map_and_Movement_Porting_Guide.md](Map_and_Movement_Porting_Guide.md): Details on map data and movement system
- [Frontend_and_Phaser_Setup_Guide.md](Frontend_and_Phaser_Setup_Guide.md): Phaser and frontend setup details

---

By following this guide, you can port the Generative Agents system to a modern, maintainable, and extensible architecture, ready for further research and development.
