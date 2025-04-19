# Office Agent Simulation

A port of the "Interactive Simulacra of Human Behavior" simulation system, focused on an office-themed environment. This project implements a single-server architecture using FastAPI for the backend, Phaser.js for the frontend, and WebSockets for real-time communication.

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

## Setup Instructions

### Prerequisites

- Node.js (v14+)
- Python (v3.9+)
- npm or yarn

### Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/office-agent-simulation.git
   cd office-agent-simulation
   ```

2. **Install dependencies**:
   ```
   # Install all dependencies (Node.js and Python)
   npm run install:all
   
   # Or install separately:
   npm install              # Root dependencies (Electron)
   npm run install:frontend # Frontend dependencies
   npm run install:backend  # Backend dependencies
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the Application

#### Development Mode

1. **Start the backend server**:
   ```
   npm run dev:backend
   ```

2. **Start the frontend server** (in a separate terminal):
   ```
   npm run dev:frontend
   ```

3. **Access the application** at `http://localhost:3000`

#### Electron App

Run the complete application as an Electron desktop app:
```
npm start
```

### Building for Distribution

Build the Electron app for distribution:
```
npm run build
```

This will create distributable packages in the `dist` directory.

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
