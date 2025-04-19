# Office Agent Simulation

An adaptation of the "Generative Agents: Interactive Simulacra of Human Behavior" by Park et al. simulation system, focused on an office-themed environment. This project implements a single-server architecture using FastAPI for the backend, Phaser.js for the frontend, and WebSockets for real-time communication.

## Overview

The Office Agent Simulation creates a virtual office environment populated by AI agents that exhibit believable behaviors, interactions, and cognitive processes. Based on the research paper "Generative Agents: Interactive Simulacra of Human Behavior," this project ports the original architecture to a more accessible, real-time system.

### Key Features

- **AI Agents with Cognitive Architecture**: Agents follow a cognitive loop of perceive → retrieve → plan → execute → reflect
- **Office Environment**: A virtual office setting with different areas and objects
- **Real-Time Visualization**: Watch agents navigate and interact in real-time
- **Extensible Framework**: Add new agents, behaviors, and environments

## Project Structure

```
office-agent-simulation/
├── backend/                # Python FastAPI backend
│   ├── app.py              # Main server entry point
│   ├── maze.py             # Environment representation
│   ├── path_finder.py      # Pathfinding algorithms
│   └── persona/            # Agent architecture
├── frontend/               # JavaScript/Phaser.js frontend
│   ├── index.html          # Main HTML file
│   ├── assets/             # Images, tilesets, etc.
│   └── src/                # JavaScript source code
├── memory-bank/            # Project documentation
├── main.js                 # Electron entry point
└── package.json            # Project configuration
```


## Development Workflow

1. **Map Creation**:
   - Use Tiled Map Editor to create office layouts
   - Export as JSON for frontend and CSV for backend

2. **Agent Development**:
   - Modify agent behaviors in `backend/persona/`
   - Test with different personalities and goals

3. **Frontend Customization**:
   - Modify the UI in `frontend/index.html`
   - Update game logic in `frontend/src/game.js`

## Documentation

Comprehensive documentation is available in the `memory-bank/` directory:

- `projectbrief.md`: Project overview and goals
- `productContext.md`: Why this project exists and user experience goals
- `systemPatterns.md`: System architecture and design patterns
- `techContext.md`: Technologies used and development setup
- `activeContext.md`: Current work focus and next steps
- `progress.md`: Project status and what's left to build

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on the research paper "Generative Agents: Interactive Simulacra of Human Behavior" by Park et al.
- Inspired by "The Office" TV show for agent personalities and scenarios
