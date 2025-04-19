# Generative Agents: Map & Movement Porting Guide

This guide provides detailed instructions for porting the map representation and agent movement system from "The Ville" to your own custom environment (such as an office simulation). It covers both the backend data structures and frontend visualization components.

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Map Representation](#2-map-representation)
3. [Creating Your Custom Map](#3-creating-your-custom-map)
4. [Backend Integration](#4-backend-integration)
5. [Frontend Integration](#5-frontend-integration)
6. [Agent Movement & Pathfinding](#6-agent-movement--pathfinding)
7. [Testing & Debugging](#7-testing--debugging)
8. [Common Issues & Solutions](#8-common-issues--solutions)

## 1. System Architecture Overview

The Generative Agents system uses a dual-representation approach for maps:

- **Frontend Representation**: A visual Tiled Map Editor (TMX) file loaded by Phaser.js for rendering
- **Backend Representation**: A set of CSV matrices and legend files used by the Python backend for agent cognition and pathfinding

Communication between frontend and backend happens through JSON files:
- Backend → Frontend: Movement files (`{sim_folder}/movement/{step}.json`) containing agent positions and actions
- Frontend → Backend: Environment state files (`{sim_folder}/environment/{step}.json`) containing current agent positions

This separation allows the backend to run headless for experiments while providing a visual interface when needed.

## 2. Map Representation

### Frontend (TMX) Representation

The frontend uses a TMX file created with Tiled Map Editor. In "The Ville" example:

- **Visual Layers**: Multiple layers using graphical tilesets for visual appearance (floors, walls, furniture)
- **Data Layers**: Special layers using "block" tilesets (simple colored squares) to encode information for the backend:
  - `Collisions`: Marks walkable vs. non-walkable tiles
  - Hidden layers for Sectors, Arenas, Game Objects, and Spawning Locations

### Backend (CSV) Representation

The backend uses several CSV files and legend files:

- **Matrix Files** (in `matrix/maze/`):
  - `collision_maze.csv`: Grid of values where non-zero indicates non-walkable tiles
  - `sector_maze.csv`: Grid mapping tiles to sector IDs
  - `arena_maze.csv`: Grid mapping tiles to arena IDs
  - `game_object_maze.csv`: Grid mapping tiles to object IDs
  - `spawning_location_maze.csv`: Grid mapping tiles to spawn point IDs

- **Legend Files** (in `matrix/special_blocks/`):
  - `world_blocks.csv`: Maps world ID to name
  - `sector_blocks.csv`: Maps sector IDs to names (e.g., "32136, the Ville, Hobbs Cafe")
  - `arena_blocks.csv`: Maps arena IDs to names
  - `game_object_blocks.csv`: Maps object IDs to names (e.g., "32227, the Ville, <all>, bed")
  - `spawning_location_blocks.csv`: Maps spawn point IDs to names

- **Metadata** (in `matrix/`):
  - `maze_meta_info.json`: Contains map dimensions, tile size, and world name

### Memory Structures

The backend builds two key data structures from these files:

1. **`maze.tiles[y][x]`**: A 2D grid where each cell contains a dictionary with:
   - `world`, `sector`, `arena`, `game_object`, `spawning_location` names
   - `collision` status (boolean)
   - `events` set (current activities at this location)

2. **`maze.address_tiles`**: A dictionary mapping string addresses (e.g., "the Ville:Hobbs Cafe:cafe customer seating") to sets of `(x, y)` coordinates

These structures enable the agent's cognitive modules to reason about locations and find paths.

## 3. Creating Your Custom Map

### Step 1: Set Up Tiled Map Editor

1. Download and install [Tiled Map Editor](https://www.mapeditor.org/)
2. Create a new map with your desired dimensions (e.g., 50x40 tiles) and tile size (e.g., 32x32 pixels)

### Step 2: Create Visual Tilesets

1. Import visual tilesets for your office environment (floors, walls, furniture, etc.)
2. Create visual layers for different elements:
   - `Floor_Visuals`
   - `Wall_Visuals`
   - `Furniture_Visuals`
   - `Foreground_Visuals`
   - etc.

### Step 3: Create Backend Data Tileset

1. Create a new tileset image file (e.g., `backend_blocks.png`) with simple colored squares
2. Import this as a tileset in Tiled (e.g., named "Backend Blocks")
3. Assign specific, documented Tile IDs (GIDs) for:
   - **Collision Marker** (e.g., GID 1): For non-walkable tiles
   - **Sector Markers** (e.g., GIDs 101-199): One unique ID per named area (101=Reception, 102=Meeting Room, etc.)
   - **Arena Markers** (e.g., GIDs 201-299): One unique ID per sub-area (201=Coffee Area within Kitchen)
   - **GameObject Markers** (e.g., GIDs 301-399): One unique ID per object type (301=Coffee Machine, 302=Desk)
   - **Spawning Location Markers** (e.g., GIDs 401-499): One unique ID per spawn point

4. **Important**: Keep a clear record mapping these GIDs to their meanings

### Step 4: Create Data Layers in Tiled

Create the following Tile Layers in Tiled, using only tiles from your "Backend Blocks" tileset:

1. **`Collision_Layer`**: Place Collision Marker tiles (GID 1) on all non-walkable tiles (walls, large furniture)
2. **`Sector_Layer`**: "Paint" all tiles belonging to each sector with the appropriate Sector Marker
3. **`Arena_Layer`**: Paint tiles within sub-areas using their Arena Marker GIDs
4. **`GameObject_Layer`**: Place the appropriate GameObject Marker tile on the *single, primary tile* representing each object instance
5. **`Spawning_Layer`**: Place Spawning Location Marker tiles on specific spawn points

### Step 5: Export Data Layers to CSV

1. In Tiled, go to `File -> Export As...`
2. Select only the `Collision_Layer`
3. Choose format "CSV (*.csv)"
4. Ensure options are set to export Tile Layer Format as "CSV"
5. Save as `collision_maze.csv`
6. Repeat for each data layer, saving as `sector_maze.csv`, `arena_maze.csv`, `game_object_maze.csv`, and `spawning_location_maze.csv`

### Step 6: Create Legend Files

Manually create the following CSV files, mapping the GIDs you chose to their names:

1. **`world_blocks.csv`**:
   ```
   1000, Office Floor 1
   ```

2. **`sector_blocks.csv`**:
   ```
   101, Office Floor 1, Reception
   102, Office Floor 1, Meeting Room
   103, Office Floor 1, Open Office
   ```

3. **`arena_blocks.csv`**:
   ```
   201, Office Floor 1, Kitchen, Coffee Area
   202, Office Floor 1, Open Office, Alice's Desk Area
   ```

4. **`game_object_blocks.csv`** (use `<all>` for generic objects):
   ```
   301, Office Floor 1, <all>, Coffee Machine
   302, Office Floor 1, <all>, Desk
   303, Office Floor 1, <all>, Chair
   ```

5. **`spawning_location_blocks.csv`**:
   ```
   401, Office Floor 1, <all>, Entrance Spawn
   ```

### Step 7: Create Metadata JSON

Create `maze_meta_info.json`:

```json
{
  "world_name": "Office Floor 1",
  "maze_width": 50,
  "maze_height": 40,
  "sq_tile_size": 32,
  "special_constraint": ""
}
```

## 4. Backend Integration

### Step 1: Organize Backend Files

Create the following directory structure:

```
your_office_assets/
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

### Step 2: Update Environment Variables

Locate where the `env_matrix` path is defined (likely in `utils.py` or set via environment variables) and update it to point to your `your_office_assets/matrix/` directory.

### Step 3: Adapt Planning Prompts

The agent's planning module (`plan.py`) uses LLM prompts to determine appropriate locations for actions. Review and modify these prompts (likely in `persona/prompt_template/run_gpt_prompt.py`) to reflect office-appropriate actions and locations.

For example, update prompts for:
- `generate_action_sector`: Choosing which sector (e.g., "Kitchen", "Meeting Room") is appropriate for an action
- `generate_action_arena`: Choosing which arena within a sector is appropriate
- `generate_action_game_object`: Choosing which object to interact with

### Step 4: Interaction Points Decision

Decide how agents should interact with objects:

- **Option A (Simpler)**: Keep the default behavior where agents stand *on* the object's tile. Ensure object marker tiles in `GameObject_Layer` are placed on *walkable* tiles in Tiled.

- **Option B (More Realistic)**: Modify `execute.py` to have agents stand *adjacent* to objects. This requires changing the target tile selection logic to find walkable neighbors of the object tile.

If choosing Option B, modify the `execute` function in `persona/cognitive_modules/execute.py` to calculate adjacent tiles:

```python
# Example modification (pseudocode)
if plan in maze.address_tiles:
    object_tiles = maze.address_tiles[plan]
    target_tiles = []
    
    # For each object tile, find adjacent walkable tiles
    for obj_tile in object_tiles:
        adjacent_tiles = [
            (obj_tile[0]+1, obj_tile[1]),
            (obj_tile[0]-1, obj_tile[1]),
            (obj_tile[0], obj_tile[1]+1),
            (obj_tile[0], obj_tile[1]-1)
        ]
        
        # Filter to only walkable adjacent tiles
        for adj_tile in adjacent_tiles:
            if (0 <= adj_tile[0] < maze.maze_width and 
                0 <= adj_tile[1] < maze.maze_height and
                not maze.tiles[adj_tile[1]][adj_tile[0]]["collision"]):
                target_tiles.append(adj_tile)
```

## 5. Frontend Integration

### Step 1: Update Asset Paths

In your frontend templates (based on `templates/demo/main_script.html`), update the asset paths to point to your new map and tilesets:

```javascript
// Update TMX path
this.load.tilemapTiledJSON("map", "{% static 'assets/your_office/visuals/office.json' %}");

// Update tileset paths
this.load.image("walls", "{% static 'assets/your_office/visuals/tilesets/walls.png' %}");
// ... other tilesets
```

### Step 2: Update Layer Names

In the `create()` function, update the layer names to match those in your TMX file:

```javascript
const floorLayer = map.createLayer("Floor", tileset_group_1, 0, 0);
const wallsLayer = map.createLayer("Walls", tileset_group_1, 0, 0);
// ... other layers

// Make sure to set collision layer
const collisionsLayer = map.createLayer("Collisions", collisions, 0, 0);
collisionsLayer.setCollisionByProperty({ collide: true });
```

### Step 3: Update Camera and Player Settings

Adjust the camera and player settings based on your map size:

```javascript
// Set initial camera position to a meaningful location in your office
player = this.physics.add.sprite(1200, 800, "atlas", "down")
                   .setSize(30, 40)
                   .setOffset(0, 0);
```

### Step 4: Update Pronunciatio (Action Emojis)

The system uses `pronunciatio` (emoji strings) to visually represent agent actions. You may want to update these to be more office-appropriate.

In `persona/cognitive_modules/execute.py`, you can modify the `generate_action_pronunciatio` function or its prompt to return office-relevant emojis:

```
"typing on computer" → "💻"
"in a meeting" → "🗣️"
"having coffee" → "☕"
```

## 6. Agent Movement & Pathfinding

### Understanding the Movement Flow

1. **Planning (`plan.py`)**: 
   - Agent decides on a high-level action (e.g., "have coffee")
   - LLM prompts determine the appropriate location (e.g., "Office:Kitchen:Coffee Area:Coffee Machine")
   - This location string is stored as `persona.scratch.act_address`

2. **Execution (`execute.py`)**:
   - Takes `act_address` and looks up corresponding tile coordinates using `maze.address_tiles`
   - Calls `path_finder` to calculate the path from current position to target
   - Returns the *next tile* in that path

3. **Pathfinding (`path_finder.py`)**:
   - Uses `collision_maze.csv` to find the shortest walkable path
   - For agent-agent interactions, finds a midpoint or adjacent tile

4. **Frontend Animation**:
   - Receives the next tile coordinate
   - Animates the agent sprite moving toward that coordinate

### Customizing Pathfinding

The default pathfinding should work with your custom map as long as your `collision_maze.csv` correctly marks walkable vs. non-walkable tiles.

If you need to customize agent-agent interactions (how agents position themselves when talking), look at the `path_finder_2` and `path_finder_3` functions in `path_finder.py`.

## 7. Testing & Debugging

### Path Tester

The original system includes a path testing tool (`path_tester.html`) that lets you visualize pathfinding. Use this to verify your collision map and pathfinding logic:

1. Start the Django server
2. Navigate to the path tester URL
3. Click on the map to test paths between points

### Common Issues to Check

1. **Collision Map**: Ensure walls and obstacles are properly marked in `collision_maze.csv`
2. **Address Resolution**: Verify `maze.address_tiles` contains the expected mappings
3. **Layer Names**: Ensure layer names in your TMX file match those referenced in the JavaScript
4. **Tile IDs**: Verify your GIDs in the legend files match those used in your Tiled map

## 8. Common Issues & Solutions

### Agents Walking Through Walls

**Cause**: Incorrect collision mapping
**Solution**: Check `collision_maze.csv` and ensure all walls/obstacles have the collision marker

### Agents Not Finding Paths

**Cause**: Target location not in `maze.address_tiles` or no valid path exists
**Solution**: Verify your legend files and ensure there's a walkable path to all objects

### Agents Standing in Wrong Positions

**Cause**: Object tiles placed on non-walkable tiles or interaction point logic issue
**Solution**: Either place object markers on walkable tiles or implement the adjacent tile logic in `execute.py`

### Frontend Not Displaying Map Correctly

**Cause**: Mismatched layer names or tileset references
**Solution**: Compare your TMX file structure with the JavaScript in `main_script.html`

---

This guide should help you port the map representation and agent movement system to your custom office environment. The key is understanding the dual representation (visual TMX vs. backend CSVs) and ensuring they remain in sync.
