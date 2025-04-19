# Map & Movement Porting Guide: Generative Agents (FastAPI + Phaser)

This guide details how to port the map representation and agent movement system for your Generative Agents simulation using a FastAPI backend and a Phaser.js frontend, with real-time WebSocket communication. It is designed for the new, simplified architecture (see [Agents_Architecture.md](Agents_Architecture.md)) and omits Django, file-based, or dual-server instructions.

---

## Table of Contents

1. [Overview: Map & Movement Architecture](#1-overview-map--movement-architecture)
2. [Map Creation in Tiled](#2-map-creation-in-tiled)
3. [Exporting Map Data for Backend & Frontend](#3-exporting-map-data-for-backend--frontend)
4. [Backend Integration (FastAPI)](#4-backend-integration-fastapi)
5. [Frontend Integration (Phaser.js)](#5-frontend-integration-phaserjs)
6. [Agent Movement & Pathfinding](#6-agent-movement--pathfinding)
7. [Testing & Debugging](#7-testing--debugging)
8. [Common Issues & Solutions](#8-common-issues--solutions)

---

## 1. Overview: Map & Movement Architecture

- **Frontend (Phaser.js):**  
  Loads a visual map (JSON from Tiled), renders agents, and animates movement.
- **Backend (FastAPI):**  
  Loads map data (CSV/JSON), maintains world state, and computes agent movement.
- **Communication:**  
  Real-time via WebSocket. The frontend sends environment state; the backend responds with agent actions/movements.

---

## 2. Map Creation in Tiled

### Step 1: Design Your Map

- Use [Tiled Map Editor](https://www.mapeditor.org/) to create your environment.
- Choose map size (e.g., 50x40 tiles, 32x32 pixels).
- Import visual tilesets for floors, walls, furniture, etc.
- Create visual layers:  
  - `Floor_Visuals`
  - `Wall_Visuals`
  - `Furniture_Visuals`
  - `Foreground_Visuals`

### Step 2: Add Data Layers for Backend

- Create a simple colored tileset for backend data (collision, sectors, arenas, objects, spawn points).
- Assign unique IDs (GIDs) for each type:
  - Collision: e.g., GID 1
  - Sectors: GID 101+
  - Arenas: GID 201+
  - Game Objects: GID 301+
  - Spawning Locations: GID 401+
- Add layers:
  - `Collision_Layer`
  - `Sector_Layer`
  - `Arena_Layer`
  - `Object_Interaction_Layer`
  - `Spawning_Layer`

---

## 3. Exporting Map Data for Backend & Frontend

### Step 1: Export Visual Map for Frontend

- Export the map as JSON (`office.json`) for Phaser.

### Step 2: Export Data Layers for Backend

- Export each data layer as CSV:
  - `collision_maze.csv`
  - `sector_maze.csv`
  - `arena_maze.csv`
  - `game_object_maze.csv`
  - `spawning_location_maze.csv`
- Create legend files mapping GIDs to names:
  - `world_blocks.csv`
  - `sector_blocks.csv`
  - `arena_blocks.csv`
  - `game_object_blocks.csv`
  - `spawning_location_blocks.csv`
- Create a metadata JSON:
  ```json
  {
    "world_name": "Office Floor 1",
    "maze_width": 50,
    "maze_height": 40,
    "sq_tile_size": 32,
    "special_constraint": ""
  }
  ```

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

## 4. Backend Integration (FastAPI)

### Step 1: Load Map Data

- On backend startup, load all CSV and JSON files.
- Build a 2D grid of tiles, each with:
  - Collision status
  - Sector/arena/object/spawn info
  - Address lookup tables for agent cognition

### Step 2: Pathfinding

- Use the collision map to determine walkable tiles.
- Implement or port a pathfinding algorithm (e.g., A*).
- For each agent, compute the next tile toward their target.

### Step 3: WebSocket Communication

- Expose a WebSocket endpoint (e.g., `/ws`).
- On each tick:
  - Receive environment state from frontend.
  - Run agent cognitive loop and movement logic.
  - Send updated agent positions and actions as JSON.

---

## 5. Frontend Integration (Phaser.js)

### Step 1: Load Map and Tilesets

- In `preload()`, load the map JSON and all tileset images.
- In `create()`, create map layers matching your Tiled project.

### Step 2: Agent Sprites

- For each agent, create a sprite at their spawn location.
- Store references for updating positions and pronunciatio (emoji/status).

### Step 3: Real-Time Updates

- On each backend response, animate agent sprites to new positions.
- Update pronunciatio/status above each agent.

---

## 6. Agent Movement & Pathfinding

### Movement Flow

1. **Planning:**  
   - Agent decides on a high-level action (e.g., "have coffee").
   - Backend determines the target location (address or tile).
2. **Pathfinding:**  
   - Backend computes the path from current to target tile.
   - Returns the next tile for the agent to move to.
3. **Frontend Animation:**  
   - Receives new tile coordinates and animates the agent sprite.

### Address Resolution

- The backend uses address lookup tables to map semantic locations (e.g., "Office:Kitchen:Coffee Area") to tile coordinates.

### Object Interaction

- Decide if agents stand *on* or *adjacent* to objects.
- If adjacent, backend should find walkable neighbor tiles for interaction.

---

## 7. Testing & Debugging

- **Backend:**  
  - Add logging to pathfinding and movement logic.
  - Print agent decisions and paths.
- **Frontend:**  
  - Use browser dev tools to inspect agent positions and animation.
  - Optionally, overlay walkability or path info for debugging.

---

## 8. Common Issues & Solutions

- **Agents Walking Through Walls:**  
  - Check `collision_maze.csv` and ensure all obstacles are marked.
- **Agents Not Finding Paths:**  
  - Verify address lookup tables and ensure all targets are reachable.
- **Agents Standing in Wrong Positions:**  
  - Ensure object markers are on walkable tiles, or implement adjacent-tile logic.
- **Map Not Displaying Correctly:**  
  - Check layer and tileset names in Tiled and Phaser.

---

## References

- [Agents_Architecture.md](Agents_Architecture.md): Core architecture and communication protocol
- [Complete_Porting_Guide.md](Complete_Porting_Guide.md): Full porting roadmap
- [Frontend_and_Phaser_Setup_Guide.md](Frontend_and_Phaser_Setup_Guide.md): Frontend setup details

---

This guide should help you port the map and movement system for your Generative Agents simulation using FastAPI and Phaser.js, with a focus on real-time, single-server architecture and maintainable data flow.
