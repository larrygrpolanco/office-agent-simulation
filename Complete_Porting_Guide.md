# Complete Porting Guide: Generative Agents for Office Simulation

This comprehensive guide provides a complete roadmap for porting the Generative Agents system from "The Ville" to your custom office simulation environment. It covers all aspects of the system, from map creation to agent cognition, and provides step-by-step instructions for each component.

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Project Roadmap](#2-project-roadmap)
3. [Map Creation & Representation](#3-map-creation--representation)
4. [Backend Setup](#4-backend-setup)
5. [Frontend Setup](#5-frontend-setup)
6. [Agent Cognition & Behavior](#6-agent-cognition--behavior)
7. [Testing & Debugging](#7-testing--debugging)
8. [Advanced Customization](#8-advanced-customization)
9. [Deployment Considerations](#9-deployment-considerations)

## 1. System Architecture Overview

The Generative Agents system consists of two main components:

### Backend (Python)

- **Core Agent Logic**: Implements the agent cognitive loop (perceive → retrieve → plan → execute → reflect)
- **Memory Systems**: Manages spatial memory, associative memory, and scratch (working memory)
- **World Representation**: Maintains the state of the environment and handles pathfinding
- **LLM Integration**: Uses language models for agent decision-making and dialogue generation

### Frontend (Django + Phaser.js)

- **Visualization**: Renders the map and agents using Phaser.js
- **User Interface**: Provides controls and information displays
- **Communication**: Exchanges data with the backend through JSON files

### Communication Flow

1. **Backend → Frontend**: Movement files (`{sim_folder}/movement/{step}.json`) containing agent positions and actions
2. **Frontend → Backend**: Environment state files (`{sim_folder}/environment/{step}.json`) containing current agent positions

This dual-server architecture allows the backend to run headless for experiments while providing a visual interface when needed.

## 2. Project Roadmap

Here's a recommended sequence for porting the system:

1. **Map Creation**: Design your office layout in Tiled Map Editor
2. **Backend Data Generation**: Create the necessary CSV files and legend files
3. **Backend Integration**: Configure the backend to use your custom map
4. **Frontend Integration**: Update the frontend to visualize your office environment
5. **Agent Customization**: Adapt agent behaviors and dialogue for an office context
6. **Testing & Refinement**: Test the system and refine as needed
7. **Deployment**: Package the system for your target environment

## 3. Map Creation & Representation

### Step 1: Design Your Office Map in Tiled

1. **Download and install [Tiled Map Editor](https://www.mapeditor.org/)**
2. **Create a new map** with your desired dimensions (e.g., 50x40 tiles) and tile size (e.g., 32x32 pixels)
3. **Import visual tilesets** for your office environment (floors, walls, furniture, etc.)
4. **Create visual layers** for different elements:
   - `Floor_Visuals`
   - `Wall_Visuals`
   - `Furniture_Visuals`
   - `Foreground_Visuals`

### Step 2: Create Backend Data Layers

1. **Create a "Backend Blocks" tileset** with simple colored squares
2. **Assign specific Tile IDs (GIDs)** for:
   - **Collision Marker** (e.g., GID 1): For non-walkable tiles
   - **Sector Markers** (e.g., GIDs 101-199): One per area (Reception, Meeting Room, etc.)
   - **Arena Markers** (e.g., GIDs 201-299): One per sub-area (Coffee Area within Kitchen)
   - **GameObject Markers** (e.g., GIDs 301-399): One per object type (Coffee Machine, Desk)
   - **Spawning Location Markers** (e.g., GIDs 401-499): One per spawn point

3. **Create data layers** in Tiled:
   - `Collision_Layer`: Place Collision Marker tiles on non-walkable areas
   - `Sector_Layer`: Paint areas with appropriate Sector Markers
   - `Arena_Layer`: Paint sub-areas with Arena Markers
   - `GameObject_Layer`: Place GameObject Markers on object locations
   - `Spawning_Layer`: Place Spawning Location Markers on spawn points

### Step 3: Export Data for Backend

1. **Export each data layer** as a CSV file:
   - `collision_maze.csv`
   - `sector_maze.csv`
   - `arena_maze.csv`
   - `game_object_maze.csv`
   - `spawning_location_maze.csv`

2. **Create legend files** mapping GIDs to names:
   - `world_blocks.csv`: `1000, Office Floor 1`
   - `sector_blocks.csv`: `101, Office Floor 1, Reception`
   - `arena_blocks.csv`: `201, Office Floor 1, Kitchen, Coffee Area`
   - `game_object_blocks.csv`: `301, Office Floor 1, <all>, Coffee Machine`
   - `spawning_location_blocks.csv`: `401, Office Floor 1, <all>, Entrance Spawn`

3. **Create metadata JSON**:
   ```json
   {
     "world_name": "Office Floor 1",
     "maze_width": 50,
     "maze_height": 40,
     "sq_tile_size": 32,
     "special_constraint": ""
   }
   ```

### Step 4: Organize Files

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

## 4. Backend Setup

### Step 1: Configure Environment Variables

Locate where the `env_matrix` path is defined (likely in `utils.py` or set via environment variables) and update it to point to your `your_office_assets/matrix/` directory.

### Step 2: Understand Key Backend Files

- **`maze.py`**: Loads map data and builds the world representation
- **`path_finder.py`**: Handles agent pathfinding
- **`persona/persona.py`**: Implements the agent cognitive loop
- **`persona/memory_structures/`**: Contains memory systems
- **`persona/cognitive_modules/`**: Contains cognitive functions
- **`reverie.py`**: Main simulation server

### Step 3: Adapt Planning Prompts

The agent's planning module uses LLM prompts to determine appropriate locations for actions. Review and modify these prompts (in `persona/prompt_template/run_gpt_prompt.py`) to reflect office-appropriate actions and locations:

- `generate_action_sector`: Choosing which sector is appropriate for an action
- `generate_action_arena`: Choosing which arena within a sector is appropriate
- `generate_action_game_object`: Choosing which object to interact with
- `generate_action_pronunciatio`: Generating emojis for actions

### Step 4: Customize Agent Interaction

Decide how agents should interact with objects:

- **Option A (Simpler)**: Keep the default behavior where agents stand *on* the object's tile
- **Option B (More Realistic)**: Modify `execute.py` to have agents stand *adjacent* to objects

If choosing Option B, modify the `execute` function in `persona/cognitive_modules/execute.py` to calculate adjacent tiles.

### Step 5: Initialize Agent Personas

Create persona initialization files for your office agents:

1. **Identity**: Define roles, personalities, and backgrounds
2. **Spatial Memory**: Initialize knowledge of the office layout
3. **Daily Schedule**: Create appropriate work schedules

## 5. Frontend Setup

### Step 1: Update Asset Paths

In your frontend templates (based on `templates/demo/main_script.html`), update the asset paths:

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
```

### Step 3: Customize Agent Visualization

Update the agent sprites and pronunciatio display:

```javascript
// Create the pronunciatio text with office-appropriate styling
pronunciatios[persona_name] = this.add.text(
  new_sprite.body.x - 6, 
  new_sprite.body.y - 42, 
  "💼", {
  font: "24px monospace", 
  fill: "#000000", 
  padding: { x: 8, y: 8}, 
  backgroundColor: "#ffffff",
  border: "solid",
  borderRadius: "10px"
}).setDepth(3);
```

### Step 4: Customize UI Elements

Update the information panels and time display to be office-appropriate:

```html
<div class="media" id="on_screen_det_content-{{p.underscore}}">
  <div class="media-body">
    <h2 id="name__{{ p.underscore }}">{{p.original}}</h2>
    <p><strong>Role:</strong> <span id="role__{{ p.underscore }}">Software Engineer</span></p>
    <p><strong>Current Task:</strong> <span id="current_action__{{ p.underscore }}"></span></p>
    <p><strong>Location:</strong> <span id="target_address__{{ p.underscore }}"></span></p>
    <p><strong>Current Meeting:</strong> <span id="chat__{{ p.underscore }}"></span></p>
  </div>
</div>
```

## 6. Agent Cognition & Behavior

### Step 1: Understand the Agent Cognitive Loop

The agent cognitive loop consists of five steps:

1. **Perceive**: Observe the environment and other agents
2. **Retrieve**: Recall relevant memories
3. **Plan**: Decide on actions based on perceptions and memories
4. **Execute**: Translate plans into physical movements
5. **Reflect**: Form higher-level thoughts about experiences

### Step 2: Customize Agent Planning

The planning module (`plan.py`) determines what actions agents take. Customize it for office behaviors:

1. **Daily Planning**: Modify `generate_first_daily_plan()` to create office-appropriate schedules
2. **Hourly Planning**: Modify `generate_hourly_schedule()` to include office activities
3. **Task Decomposition**: Modify `generate_task_decomp()` to break down office tasks

### Step 3: Customize Agent Interactions

Agent interactions are handled by several functions:

1. **Conversation Initiation**: Modify `generate_decide_to_talk()` to determine when agents should talk
2. **Conversation Content**: Modify `generate_convo()` to generate office-appropriate dialogue
3. **Reaction Logic**: Modify `generate_decide_to_react()` to determine how agents react to events

### Step 4: Customize Agent Reflection

The reflection module (`reflect.py`) generates higher-level thoughts. Customize it for office contexts:

1. **Event Reflection**: Generate thoughts about work events
2. **Planning Reflection**: Generate thoughts about work plans
3. **Social Reflection**: Generate thoughts about colleagues

## 7. Testing & Debugging

### Path Tester

Use the path testing tool to verify your collision map and pathfinding logic:

1. Start the Django server
2. Navigate to the path tester URL
3. Click on the map to test paths between points

### Common Issues to Check

1. **Collision Map**: Ensure walls and obstacles are properly marked
2. **Address Resolution**: Verify `maze.address_tiles` contains the expected mappings
3. **Layer Names**: Ensure layer names in your TMX file match those in JavaScript
4. **Tile IDs**: Verify your GIDs in the legend files match those in your Tiled map

### Debugging Techniques

1. **Print Statements**: Add print statements to key functions to trace execution
2. **Logging**: Enable logging in the backend to track agent decisions
3. **Frontend Console**: Use browser developer tools to debug frontend issues
4. **Step-by-Step Testing**: Test each component individually before integration

## 8. Advanced Customization

### Custom Agent Behaviors

To create more realistic office behaviors:

1. **Meeting Scheduling**: Implement a system for agents to schedule and attend meetings
2. **Task Priorities**: Add priority levels to tasks and allow interruptions
3. **Team Dynamics**: Create team structures and collaborative behaviors

### Custom Environment Interactions

To enhance the office environment:

1. **Interactive Objects**: Add special interactions for office equipment
2. **Time-Based Events**: Schedule office-wide events (meetings, lunch, etc.)
3. **Environmental Conditions**: Add factors like noise levels or temperature

### Performance Optimization

For larger simulations:

1. **Tilemap Optimization**: Use culling and efficient layer organization
2. **Agent Animation Optimization**: Only animate visible agents
3. **Memory Management**: Limit history storage and use compressed formats

## 9. Deployment Considerations

### Single-Server Deployment

For simplicity, consider merging the frontend and backend:

1. **WebSocket Communication**: Replace file-based communication with WebSockets
2. **Integrated Server**: Use Django to serve both the frontend and run the backend
3. **Electron Packaging**: Package the application with Electron for desktop use

### Multi-Server Deployment

For more complex setups:

1. **Backend API**: Create a REST or WebSocket API for the backend
2. **Frontend Hosting**: Host the frontend on a separate server
3. **Database Integration**: Add a database for persistent storage

### Cloud Deployment

For scalable deployments:

1. **Containerization**: Package the application with Docker
2. **Orchestration**: Use Kubernetes for container orchestration
3. **Cloud Services**: Leverage cloud services for LLM integration and storage

---

This guide provides a comprehensive roadmap for porting the Generative Agents system to your office simulation. By following these steps and understanding the underlying architecture, you can create a realistic simulation of human behavior in an office environment.

For more detailed information on specific components, refer to the accompanying guides:
- [Map & Movement Porting Guide](Map_and_Movement_Porting_Guide.md)
- [Frontend & Phaser.js Setup Guide](Frontend_and_Phaser_Setup_Guide.md)
