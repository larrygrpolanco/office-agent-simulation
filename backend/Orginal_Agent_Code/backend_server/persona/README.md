# Persona System

## Overview
The Persona system implements generative agents with memory, planning capabilities, perception, and decision-making. This system powers the simulated agents in Reverie, enabling them to interact with their environment and other agents in a human-like manner.

## Main Components

### persona.py
The core class that ties together all cognitive modules and memory structures. Each Persona instance represents a single agent in the simulation with:
- Long-term and short-term memory systems
- Cognitive processes for perception, planning, reflection, and conversation
- State management through the lifecycle of the agent

Key methods:
- `perceive()`: Detects events in the environment
- `retrieve()`: Accesses relevant memories based on current perception
- `plan()`: Generates daily schedules and makes real-time decisions
- `execute()`: Translates plans into actions in the environment
- `reflect()`: Generates insights from experiences
- `move()`: Main cognitive function that orchestrates the agent's cognitive cycle

## Cognitive Modules

### perceive.py
Handles how agents observe and interpret the environment around them:
- Processes nearby events within the agent's vision range
- Updates spatial memory with new location information
- Assigns "poignancy" scores to events based on their significance
- Filters events based on attention bandwidth and retention

### retrieve.py
Manages memory retrieval based on relevance, recency, and importance:
- Calculates similarity between current events and memories
- Uses focal points to direct retrieval toward specific topics
- Balances between recent, important, and contextually relevant memories
- Returns memories that provide context for decision-making

### plan.py
Orchestrates both long-term and short-term planning:
- Generates wake-up times and daily schedules
- Decomposes high-level activities into specific tasks
- Selects appropriate locations and objects for actions
- Manages interactions with other agents
- Handles schedule revisions when interruptions occur

### reflect.py
Enables agents to process experiences and generate insights:
- Creates focal points from important memories
- Generates insights with supporting evidence
- Triggers reflections based on importance thresholds
- Processes conversations to extract relationship information
- Creates planning thoughts based on interactions

### execute.py
Translates plans into physical movements in the simulation:
- Converts action addresses to physical coordinates
- Implements pathfinding for agent movement
- Handles special cases (interactions, waiting, random locations)
- Returns movement descriptions and visualizations

### converse.py
Manages conversations between agents:
- Generates realistic multi-turn dialogues
- Creates summaries of conversations
- Generates inner thoughts during conversations
- Assigns poignancy to conversation events
- Provides relationship insights from dialogues

## Memory Structures

### associative_memory.py
Long-term memory system storing events, thoughts, and conversations:
- Uses `ConceptNode` objects to represent memory elements
- Stores embeddings for semantic similarity comparison
- Implements retrieval by keywords and relevance
- Manages memory organization by recency and importance
- Tracks relationships between memories (e.g., evidence for thoughts)

### spatial_memory.py
Represents the agent's knowledge of the physical environment:
- Uses a tree structure to represent spatial hierarchy
- Organizes spaces by world, sector, arena, and objects
- Enables navigation and interaction with environment
- Provides methods to access locations the agent knows about

### scratch.py
Short-term working memory that stores current agent state:
- Maintains parameters like attention bandwidth and vision range
- Stores identity information (name, traits, etc.)
- Tracks current action, location, and conversation state
- Manages planning variables and reflection triggers
- Functions as the "working memory" for the agent's operation

## How It Works

1. The agent perceives its environment through the `perceive()` function
2. Relevant memories are retrieved based on current perceptions
3. The agent plans its next actions using daily schedules and immediate context
4. Actions are executed in the environment
5. The agent periodically reflects on experiences to generate insights
6. This cycle repeats to create realistic, autonomous behavior

The system uses large language models to generate natural language descriptions, emotional responses, and decision-making, creating a simulation of human-like cognitive processes.