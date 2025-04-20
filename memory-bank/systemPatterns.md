# Office Agent Simulation: System Patterns

## System Architecture Overview

The Office Agent Simulation uses a modern, single-server architecture that combines a Python backend with a JavaScript frontend, connected via WebSockets for real-time communication.

```
┌─────────────────────────────────────────────────────────────┐
│                      Electron Application                    │
│                                                             │
│  ┌─────────────────┐           ┌───────────────────────┐   │
│  │  FastAPI Backend │◄────────►│  Phaser.js Frontend   │   │
│  │  (Python)        │  WebSocket│  (JavaScript)         │   │
│  └─────────────────┘           └───────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **FastAPI Backend**
   - Manages agent cognition and simulation state
   - Exposes WebSocket endpoint for real-time communication
   - Processes environment updates and generates agent actions

2. **Phaser.js Frontend**
   - Renders the office environment and agents
   - Handles user interaction
   - Sends environment state to backend
   - Animates agent movements based on backend instructions

3. **WebSocket Communication**
   - Replaces the original file-based communication
   - Enables real-time updates between frontend and backend
   - Maintains the same JSON structure for compatibility

4. **Electron Wrapper** (future)
   - Packages the application for desktop use
   - Manages the Python subprocess
   - Provides native OS integration

## Core Design Patterns

### 1. Agent Cognitive Loop

The heart of the system is the agent cognitive loop, implemented in the `persona.py` class:

```
┌─────────┐     ┌──────────┐     ┌──────┐     ┌─────────┐     ┌─────────┐
│ Perceive │────►│ Retrieve │────►│ Plan │────►│ Execute │────►│ Reflect │
└─────────┘     └──────────┘     └──────┘     └─────────┘     └─────────┘
     ▲                                                              │
     └──────────────────────────────────────────────────────────────┘
```

Each agent follows this loop to:
1. **Perceive** the environment around them
2. **Retrieve** relevant memories based on what they perceive
3. **Plan** their next actions (both short and long-term)
4. **Execute** those plans as concrete movements and interactions
5. **Reflect** on their experiences to form higher-level thoughts

### 2. Memory System Architecture

Agents have three complementary memory structures:

```
┌───────────────────────┐
│      Agent Memory     │
│                       │
│  ┌─────────────────┐  │
│  │ Spatial Memory  │  │  Physical world knowledge
│  └─────────────────┘  │
│                       │
│  ┌─────────────────┐  │
│  │ Associative Mem │  │  Long-term episodic memory
│  └─────────────────┘  │
│                       │
│  ┌─────────────────┐  │
│  │     Scratch     │  │  Short-term working memory
│  └─────────────────┘  │
└───────────────────────┘
```

- **Spatial Memory** (`spatial_memory.py`): A tree representing the agent's knowledge of the world's physical layout
- **Associative Memory** (`associative_memory.py`): Long-term memory of events, thoughts, and interactions
- **Scratch** (`scratch.py`): Short-term working memory for current state and plans

### 3. Dual Map Representation

The environment is represented in two complementary ways:

```
┌───────────────────┐                  ┌───────────────────┐
│  Visual Map (TMX) │                  │ Logical Map (CSV) │
│                   │                  │                   │
│  - Tilesets       │                  │  - Collision      │
│  - Visual Layers  │                  │  - Sectors        │
│  - Decorations    │◄────────────────►│  - Arenas         │
│  - Animation      │    Coordinates   │  - Game Objects   │
│                   │    Mapping       │  - Spawn Points   │
│                   │                  │                   │
│  (Frontend)       │                  │  (Backend)        │
└───────────────────┘                  └───────────────────┘
```

- **Frontend Map**: JSON/TMX file created with Tiled Map Editor, loaded by Phaser.js
- **Backend Map**: Set of CSV matrices and legend files for agent cognition and pathfinding

### 4. Real-Time Communication Pattern

The WebSocket-based communication replaces the original file-based approach:

```
┌─────────────┐                         ┌─────────────┐
│  Frontend   │                         │  Backend    │
│             │                         │             │
│             │  1. Environment State   │             │
│             │────────────────────────►│             │
│             │  {"agent": {x:10, y:5}} │             │
│             │                         │             │
│             │                         │             │
│             │  2. Agent Movements     │             │
│             │◄────────────────────────│             │
│             │  {"movement":[11,5],    │             │
│             │   "pronunciatio":"💼"}  │             │
└─────────────┘                         └─────────────┘
```

- **Frontend → Backend**: Current positions of all agents
- **Backend → Frontend**: Next positions, actions, and descriptions for each agent

### 5. Agent Interface Pattern

For future experimentation with different agent architectures:

```
┌───────────────────┐
│  Agent Interface  │
│                   │
│  - perceive()     │
│  - decide()       │
│  - act()          │
└───────────────────┘
         ▲
         │
         │
┌────────┴─────────┐
│                  │
│                  │
┌──────────────┐   ┌──────────────┐
│ ReverieAgent │   │ Future Agent │
│              │   │ Architectures│
└──────────────┘   └──────────────┘
```

This pattern allows for:
- Maintaining the original architecture initially
- Adding experimental architectures later
- Comparing different approaches
- Keeping the frontend and communication system unchanged

---

## Environmental Matrix & Hierarchical Labeling Pattern

### Rationale

- **Hierarchical (tree) labeling** in special_blocks CSVs (world, sector, arena, object) enables agents to reason about, remember, and navigate the environment at multiple levels of detail.
- This structure supports address resolution, contextual memory, and extensibility for both small and large maps.

### Implementation

- All legend files (arena_blocks.csv, game_object_blocks.csv, etc.) use the format: GID, world, sector, arena, object (as needed).
- For small, detailed maps, always use specific context (avoid `<all>` unless you have many generic, repeated objects).
- Example:
  ```
  0,The Office, Kitchen, Kitchenette, Coffee Machine
  0,The Office, Open Workspace, Desk Cluster A, Assistant’s Desk
  0,The Office, Reception, , Reception Desk
  ```

### Impact on Agent Architecture

- **Spatial Memory**: Agents can form memories and plans at any level of the hierarchy.
- **Navigation**: The backend can resolve high-level goals (e.g., "go to the kitchen") to specific tiles.
- **Interaction**: Agents can interact with objects in context (e.g., "use the coffee machine in the kitchen").
- **Extensibility**: New areas and objects can be added by simply extending the CSVs with new hierarchical rows.

### Best Practices

- Always use the full hierarchy for labeling, even in small maps.
- Be consistent and clear in naming.
- Update documentation and legend files as the environment evolves.
- Use `<all>` only for truly generic objects in large, repetitive environments.

---

## Critical Implementation Paths

### 1. Agent Cognitive Loop Implementation

The most critical path is the agent cognitive loop in `persona.py`:

```python
def move(self, maze, personas, curr_tile, curr_time):
    # 1. Perceive
    perceived_info = self.perceive(maze, personas, curr_tile)
    
    # 2. Retrieve
    retrieved_memories = self.retrieve(perceived_info)
    
    # 3. Plan
    plan = self.plan(maze, personas, new_day, retrieved_memories)
    
    # 4. Execute
    next_tile, pronunciatio, description = self.execute(maze, personas, plan)
    
    # 5. Reflect
    self.reflect()
    
    return next_tile, pronunciatio, description
```

### 2. WebSocket Communication Path

The WebSocket endpoint in FastAPI:

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive environment state from frontend
        env_data = await websocket.receive_json()
        
        # Process agent decisions
        movements = process_agent_decisions(env_data)
        
        # Send movement data to frontend
        await websocket.send_json(movements)
```

### 3. Frontend Animation Path

The frontend animation loop in Phaser:

```javascript
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
    }
}
```

## Porting Priorities

When adapting the original codebase, focus on these components in order:

1. **Agent Cognitive Loop** (`persona.py` and cognitive modules)
2. **Memory Systems** (associative_memory.py, spatial_memory.py, scratch.py)
3. **Environment Representation** (maze.py)
4. **Communication System** (replace file I/O in reverie.py)
5. **Pathfinding** (path_finder.py)

This ensures maintaining the core agent believability while adapting the system to the new architecture.

## Key Technical Decisions

1. **Single-Server Architecture**: Simplifies deployment and development compared to the original dual-server approach.

2. **WebSocket Communication**: Enables real-time updates without the complexity of file-based communication.

3. **Modular Agent Interface**: Allows for future experimentation with different agent architectures.

4. **Electron Packaging**: Makes the application easily shareable and runnable on desktop.

5. **Phaser.js for Visualization**: Provides a powerful 2D game engine for rendering the office environment.

6. **FastAPI for Backend**: Offers modern async support and WebSocket capabilities.

7. **Tiled Map Editor**: Industry-standard tool for creating and editing game maps.

8. **Hierarchical Environmental Matrix**: Use a tree structure in all special_blocks CSVs for maximum agent context, memory, and extensibility.

## Future Architectural Considerations

1. **React Integration**: For more sophisticated UI components outside the simulation area.

2. **Multiple Agent Architectures**: Interface for swapping different cognitive models.

3. **LLM API Integration**: Configurable to work with different LLM providers.

4. **Persistence Layer**: For saving and loading simulation states.

5. **Event System**: For more complex interactions between agents and environment.
