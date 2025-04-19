# Office Agent Simulation Project Brief

## Project Overview

The Office Agent Simulation is a port of the "Generative Agents" simulation system to a modern, single-server architecture focused on an office-themed environment. The project aims to create a fun, interactive simulation of office life with AI-powered agents that exhibit believable behaviors, interactions, and cognitive processes.

## Core Goals

1. **Create a working agent simulation** with the cognitive loop architecture (perceive → retrieve → plan → execute → reflect)
2. **Port the original architecture** to a modern, single-server setup using FastAPI and WebSockets
3. **Develop an engaging office environment** where agents interact realistically
4. **Build a foundation for extensibility** to add new maps, agents, and behaviors over time
5. **Package as a desktop application** using Electron for easy sharing

## Target Experience

Users will be able to:
- Watch AI agents navigate an office environment with realistic behaviors
- See agents interact with each other and the environment
- Eventually customize agents, edit their personalities and goals
- Add new office scenarios and behaviors as the project evolves

## Beta Requirements

### Must Have
- Single-server architecture (FastAPI backend + Phaser.js frontend)
- Working agent cognitive loop and memory systems
- Basic office map with walkable areas and objects
- Real-time WebSocket communication
- Simple agent behaviors appropriate for an office setting
- Basic visualization of agent status ("pronunciatio" system)

### Nice to Have
- Multiple agent personalities based on characters from "The Office"
- Simple UI for viewing agent thoughts and status
- Ability to interact with the simulation (e.g., clicking on agents)
- Basic environment interactions (e.g., using office equipment)

### Future Expansion
- React-based UI for more sophisticated interaction
- Agent customization interface
- Multiple maps and scenarios
- Advanced behaviors (e.g., agents can make messes, get fired, play games)
- Support for different LLM models

## Technical Approach

The project will follow a phased approach:
1. Port the core agent architecture to FastAPI
2. Implement the Phaser.js frontend
3. Connect frontend and backend via WebSockets
4. Add basic office behaviors and interactions
5. Package with Electron

## Out of Scope for Beta

- Multi-user functionality
- Cloud deployment
- Advanced UI features
- Complex agent interactions
- Multiple agent architecture variants (will be added later)

## Success Criteria

The beta version will be considered successful when:
1. Agents can navigate the office environment
2. Agents exhibit basic office behaviors
3. The simulation runs smoothly in real-time
4. The project is well-documented for future extension
