# Memory Structures

## Overview
This directory contains the memory systems that enable agents to store, organize, and retrieve information about their experiences. The three memory structures work together to create a comprehensive representation of an agent's knowledge and experiences.

## Components

### associative_memory.py
Long-term memory system that stores events, thoughts, and conversations in a structured format.

**Key Classes:**
- `ConceptNode`: Represents a single memory element (event, thought, or chat)
- `AssociativeMemory`: Main class that manages storage and retrieval of nodes

**Key Features:**
- Memory is organized as nodes with subject-predicate-object (SPO) triples
- Stores event details, creation time, poignancy (importance), and keywords
- Uses embeddings for semantic similarity comparison
- Maintains sequences of events, thoughts, and chats by recency
- Supports keyword-based retrieval for fast access
- Tracks relationships between thoughts and evidence

**How It Works:**
1. Creates `ConceptNode` objects for each memory with metadata
2. Organizes nodes in sequences and by keywords for easy retrieval
3. Assigns importance scores (poignancy) to memories
4. Provides methods to save/load memory state
5. Enables retrieval of related memories based on content

### spatial_memory.py
Represents the agent's knowledge of the physical environment through a hierarchical structure.

**Key Class:**
- `MemoryTree`: Maintains a tree representation of spatial knowledge

**Key Features:**
- Organized hierarchically by world, sector, arena, and objects
- Provides methods to query known locations and objects
- Enables spatial navigation and contextual awareness
- Supports saving and loading of spatial knowledge

**How It Works:**
1. Stores spatial knowledge in a nested dictionary (tree) structure
2. Provides methods to access elements at different levels of the hierarchy
3. Helps the agent understand what objects exist in which locations
4. Supports decision-making about where to perform actions

### scratch.py
Short-term working memory that maintains the current state of the agent.

**Key Class:**
- `Scratch`: Stores transient information about the agent's current state

**Key Features:**
- Maintains agent parameters like attention bandwidth and vision range
- Stores identity information (name, traits, current status)
- Tracks current action, location, and conversation state
- Manages planning variables (daily schedule, current task)
- Handles reflection triggers and importance thresholds

**How It Works:**
1. Initializes with default parameters or loads from saved state
2. Provides methods to update and access current state information
3. Maintains action-related variables (description, duration, location)
4. Tracks planning information like daily schedules
5. Manages conversation state when interacting with other agents

## How They Work Together

1. **Perceiving Events**:
   - Events from the environment are processed and stored in `associative_memory.py`
   - Spatial information is updated in `spatial_memory.py`
   - Current state is tracked in `scratch.py`

2. **Planning Actions**:
   - `associative_memory.py` provides relevant past experiences
   - `spatial_memory.py` helps locate appropriate places for actions
   - `scratch.py` maintains the current plan and schedule

3. **Executing Actions**:
   - `scratch.py` tracks the current action being performed
   - `spatial_memory.py` provides navigational information
   - After execution, new events are stored in `associative_memory.py`

4. **Reflecting on Experiences**:
   - `associative_memory.py` provides material for reflection
   - New insights are stored back in `associative_memory.py`
   - Reflection triggers are managed by `scratch.py`

This multi-layered memory system allows agents to maintain a rich internal representation of their experiences, knowledge, and current state, enabling complex, human-like behavior.