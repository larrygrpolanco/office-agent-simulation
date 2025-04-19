# Office Agent Simulation: Technical Context

## Technology Stack

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Core backend language |
| FastAPI | Latest | API framework with WebSocket support |
| Uvicorn | Latest | ASGI server for FastAPI |
| OpenAI API | Latest | LLM integration for agent cognition |

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| JavaScript | ES6+ | Core frontend language |
| Phaser.js | 3.55+ | 2D game engine for visualization |
| HTML5/CSS3 | Latest | Basic UI structure and styling |
| React.js | Latest | (Future) Advanced UI components |

### Development & Deployment

| Technology | Version | Purpose |
|------------|---------|---------|
| Electron | Latest | Desktop application packaging |
| Tiled Map Editor | Latest | Creating and editing game maps |
| Git | Latest | Version control |
| npm/pip | Latest | Package management |

## Development Environment

### Local Setup

```
office-agent-simulation/
├── backend/
│   ├── app.py                # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── maze.py               # Environment representation
│   ├── path_finder.py        # Pathfinding algorithms
│   └── persona/              # Agent architecture
│       ├── persona.py        # Main agent class
│       ├── cognitive_modules/# Agent cognitive processes
│       └── memory_structures/# Agent memory systems
├── frontend/
│   ├── index.html            # Main HTML file
│   ├── package.json          # JavaScript dependencies
│   ├── assets/               # Images, tilesets, etc.
│   │   ├── visuals/          # Map files (TMX/JSON)
│   │   └── matrix/           # Backend map data (CSV)
│   └── src/                  # JavaScript source code
│       ├── game.js           # Phaser game configuration
│       └── components/       # (Future) React components
├── main.js                   # Electron entry point
├── .env                      # Environment variables (API keys)
└── memory-bank/              # Project documentation
```

### Required Tools

- **Code Editor**: VSCode or similar
- **Tiled Map Editor**: For creating and editing maps
- **Node.js & npm**: For JavaScript dependencies
- **Python 3.9+**: For backend development
- **Git**: For version control

## Technical Constraints

### Performance Considerations

1. **Agent Cognition**:
   - LLM API calls can be expensive and slow
   - Batch processing or caching may be needed for multiple agents
   - Consider local LLM options for development

2. **Real-time Simulation**:
   - WebSocket communication adds latency
   - Limit the number of agents for smooth performance
   - Optimize pathfinding for larger maps

3. **Rendering**:
   - Phaser.js has good performance but can struggle with many animated sprites
   - Use culling and optimization techniques for larger maps
   - Consider sprite batching for many agents

### API Limitations

1. **LLM API**:
   - Rate limits on API calls
   - Token limitations for context windows
   - Cost considerations for frequent calls
   - Dependency on external service availability

2. **Local Development**:
   - Environment variables for API keys (.env file)
   - Potential for offline development with local LLMs

## Dependencies & External Resources

### Core Dependencies

#### Backend (Python)

```
fastapi>=0.68.0
uvicorn>=0.15.0
websockets>=10.0
python-dotenv>=0.19.0
openai>=0.27.0
numpy>=1.20.0
```

#### Frontend (JavaScript)

```json
{
  "dependencies": {
    "phaser": "^3.55.2",
    "electron": "^13.0.0"
  },
  "devDependencies": {
    "electron-builder": "^22.11.7"
  }
}
```

### External Resources

1. **Tilesets**:
   - Office-themed tilesets for Tiled
   - Character sprites for agents

2. **LLM Integration**:
   - OpenAI API key (or alternative LLM provider)
   - Prompt templates for agent cognition

3. **Documentation**:
   - Original "Generative Agents" paper and code
   - Phaser.js documentation
   - FastAPI documentation
   - Tiled Map Editor documentation

## Tool Usage Patterns

### Tiled Map Editor

1. **Map Creation Workflow**:
   - Create a new map (e.g., 50x40 tiles, 32x32 pixels)
   - Import tilesets for office environment
   - Create visual layers (floors, walls, furniture)
   - Create data layers for backend (collision, sectors, objects)
   - Export as JSON for frontend and CSV for backend

2. **Layer Structure**:
   - Visual Layers:
     - Floor_Visuals
     - Wall_Visuals
     - Furniture_Visuals
     - Foreground_Visuals
   - Data Layers:
     - Collision_Layer
     - Sector_Layer
     - Arena_Layer
     - GameObject_Layer
     - Spawning_Layer

### FastAPI Development

1. **WebSocket Endpoint**:
   - Create a WebSocket endpoint for real-time communication
   - Process environment updates from frontend
   - Run agent cognitive loop
   - Send movement data back to frontend

2. **Agent Processing**:
   - Load agent configurations
   - Initialize memory systems
   - Process perceptions and generate actions
   - Update internal state

### Phaser.js Development

1. **Game Setup**:
   - Configure Phaser game instance
   - Load assets (map, tilesets, sprites)
   - Create map layers and sprites
   - Set up WebSocket connection

2. **Animation Loop**:
   - Send current environment state to backend
   - Receive movement data from backend
   - Animate agent sprites to new positions
   - Update UI elements (time, agent status)

### Electron Packaging

1. **Application Structure**:
   - Main process: Starts Python backend, creates window
   - Renderer process: Loads frontend, connects to backend
   - IPC communication for app-level events

2. **Distribution**:
   - Package Python backend with application
   - Include all assets and dependencies
   - Create installers for different platforms

## Development Workflow

1. **Map Creation**:
   - Design office layout in Tiled
   - Export map data for frontend and backend

2. **Backend Development**:
   - Port agent cognitive loop and memory systems
   - Implement WebSocket communication
   - Test with mock frontend data

3. **Frontend Development**:
   - Implement map rendering and agent sprites
   - Set up WebSocket communication
   - Test with mock backend data

4. **Integration**:
   - Connect frontend and backend
   - Test full simulation loop
   - Debug and optimize

5. **Packaging**:
   - Set up Electron configuration
   - Package application for distribution
   - Test on target platforms

## Future Technical Considerations

1. **React Integration**:
   - Add React for more sophisticated UI
   - Use React components for menus, settings, agent details
   - Integrate with Phaser.js canvas

2. **Multiple LLM Support**:
   - Abstract LLM API calls for provider flexibility
   - Support for different models and providers
   - Local LLM options for offline use

3. **Performance Optimization**:
   - Caching strategies for LLM calls
   - Optimized pathfinding for larger maps
   - Rendering optimizations for many agents

4. **Advanced Features**:
   - Save/load simulation state
   - Agent customization interface
   - Scenario editor
   - Analytics and visualization tools
