# Storage

This directory contains the primary simulation data for the generative agents human behavior simulation system.

## Purpose

The storage directory saves complete simulation runs with all environment states, agent movements, and agent memories.

## Directory Structure

Each simulation run is stored in a separate folder with naming pattern:
- `[Date]_the_ville_[AgentNames]-step-[StepSize]-[RunNumber]/`
  - Example: `July1_the_ville_isabella_maria_klaus-step-3-10/`

Within each simulation folder:
- `environment/` - JSON files for each timestep showing agent positions and world state
  - Numbered sequentially (0.json, 1.json, etc.)
- `movement/` - JSON files tracking agent actions and movements
  - Numbered sequentially (0.json, 1.json, etc.)
- `personas/` - Agent identity and memory data
- `reverie/` - Additional simulation metadata
  - `meta.json` - Simulation parameters

## Base Simulations

- `base_the_ville_isabella_maria_klaus/` - Reference simulation with three agents
- `base_the_ville_n25/` - Reference simulation with 25 agents

## How This Data Is Used

1. The frontend loads these JSON files to visualize simulation replays
2. Each timestep JSON file contains the complete state needed to render that moment
3. Movement files track the decisions and actions of agents
4. Persona files maintain the cognitive state and memory of agents

## Data Format

Environment JSON files contain:
- Agent positions
- Current time in simulation
- Active interactions and conversations

Movement JSON files contain:
- Agent action decisions
- Path planning
- Conversation content
- Memory updates