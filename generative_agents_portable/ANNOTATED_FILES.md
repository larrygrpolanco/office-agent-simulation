# Annotated File List: Key Components of the Generative Agents Architecture

This document provides a quick reference to the most important files in the backend server, explaining their purpose and key functions.

## Core Files

### `reverie.py`
- **Purpose**: Main simulation server that orchestrates the entire system
- **Key Components**:
  - `ReverieServer` class: Manages the simulation state, personas, and communication
  - `start_server()`: Main simulation loop that processes environment files and generates movement files
  - `open_server()`: Interactive terminal interface for controlling the simulation
- **Communication Pattern**: 
  - Reads environment files from `{sim_folder}/environment/{step}.json`
  - Writes movement files to `{sim_folder}/movement/{step}.json`
- **Porting Notes**: 
  - Replace file I/O with websockets or direct function calls
  - Keep the core simulation loop logic

### `maze.py`
- **Purpose**: Represents the world, handles collision and spatial events
- **Key Components**:
  - `Maze` class: Manages the tile-based world representation
  - `access_tile()`: Gets information about a specific tile
  - `get_nearby_tiles()`: Finds tiles within a certain radius
  - `add_event_from_tile()`: Adds an event to a tile (e.g., agent presence)
- **Porting Notes**: 
  - Adapt to your map structure but keep the interface
  - Ensure your office map is compatible with the tile-based system

### `path_finder.py`
- **Purpose**: Handles pathfinding for agent movement
- **Key Components**:
  - `path_finder()`: Main pathfinding algorithm
  - `closest_coordinate()`: Finds the closest accessible coordinate
- **Porting Notes**: 
  - Keep intact if using a similar tile-based system
  - Can be replaced with other pathfinding algorithms if needed

## Persona (Agent) Architecture

### `persona/persona.py`
- **Purpose**: Main agent class that implements the cognitive loop
- **Key Components**:
  - `perceive()`: Observes the environment
  - `retrieve()`: Recalls relevant memories
  - `plan()`: Makes decisions based on perceptions and memories
  - `execute()`: Converts plans to concrete actions
  - `reflect()`: Forms higher-level thoughts
  - `move()`: Main method that runs the cognitive loop
- **Porting Notes**: 
  - Keep the cognitive loop intact
  - Modify `move()` to work with your communication system

### `persona/memory_structures/`

#### `associative_memory.py`
- **Purpose**: Long-term memory system for agents
- **Key Components**:
  - `AssociativeMemory` class: Stores and retrieves memories
  - `add_memory()`: Adds a new memory
  - `get_relevant_memories()`: Retrieves memories based on relevance
- **Porting Notes**: 
  - Keep intact, this is a core part of agent believability

#### `spatial_memory.py`
- **Purpose**: Agent's knowledge of the world's physical layout
- **Key Components**:
  - `MemoryTree` class: Tree structure representing spatial knowledge
  - `add_node()`: Adds a new location to memory
  - `get_node()`: Retrieves information about a location
- **Porting Notes**: 
  - May need to adapt to your office map structure

#### `scratch.py`
- **Purpose**: Short-term working memory for current state and plans
- **Key Components**:
  - `Scratch` class: Stores temporary information
  - `get_daily_schedule()`: Gets the agent's current schedule
  - `get_curr_event_and_desc()`: Gets the current event description
- **Porting Notes**: 
  - Keep intact, handles important state information

### `persona/cognitive_modules/`

#### `perceive.py`
- **Purpose**: Implements how agents observe their environment
- **Key Components**:
  - `perceive()`: Main function that processes perceptions
  - `get_surroundings()`: Gets information about nearby tiles and events
- **Porting Notes**: 
  - May need to modify how agents perceive your office environment

#### `retrieve.py`
- **Purpose**: Implements how agents recall relevant memories
- **Key Components**:
  - `retrieve()`: Main function that retrieves memories
  - `get_relevant_memories()`: Finds memories related to current perceptions
- **Porting Notes**: 
  - Keep intact, core to agent believability

#### `plan.py`
- **Purpose**: Implements how agents make decisions
- **Key Components**:
  - `plan()`: Main planning function
  - `create_daily_plan()`: Creates a high-level plan for the day
  - `decompose_action()`: Breaks down high-level plans into specific actions
- **Porting Notes**: 
  - Keep intact, core to agent believability

#### `execute.py`
- **Purpose**: Implements how agents turn plans into actions
- **Key Components**:
  - `execute()`: Main execution function
  - `get_next_tile()`: Determines the next tile to move to
- **Porting Notes**: 
  - May need to adapt to your movement system

#### `reflect.py`
- **Purpose**: Implements how agents form higher-level thoughts
- **Key Components**:
  - `reflect()`: Main reflection function
  - `generate_questions()`: Creates questions for reflection
  - `answer_questions()`: Generates insights from memories
- **Porting Notes**: 
  - Keep intact, core to agent believability

#### `converse.py`
- **Purpose**: Implements agent conversation
- **Key Components**:
  - `generate_response()`: Creates dialogue responses
  - `open_convo_session()`: Starts a conversation
- **Porting Notes**: 
  - Keep intact, handles agent dialogue

## Utility Files

### `global_methods.py`
- **Purpose**: Utility functions used throughout the codebase
- **Key Components**:
  - File I/O functions
  - Data processing utilities
- **Porting Notes**: 
  - Keep the useful utilities, replace file I/O with your communication system

### `utils.py`
- **Purpose**: Additional utility functions
- **Porting Notes**: 
  - Keep as needed for your implementation

## Porting Priority

When adapting this codebase to your Office simulation, focus on these components in order:

1. **Agent Cognitive Loop** (`persona.py` and cognitive modules)
2. **Memory Systems** (associative_memory.py, spatial_memory.py, scratch.py)
3. **Environment Representation** (maze.py)
4. **Communication System** (replace file I/O in reverie.py)
5. **Pathfinding** (path_finder.py)

This will ensure you maintain the core agent believability while adapting the system to your needs.
