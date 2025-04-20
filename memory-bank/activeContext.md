# Office Agent Simulation: Active Context

## Current Work Focus

We are currently in the **initial implementation phase** of the Office Agent Simulation project. The focus is on:

1. **Porting the core agent architecture**: Taking the cognitive loop and memory systems from the original Generative Agents codebase and adapting them to our new architecture.

2. **Developing the environment representation**: Implementing the maze.py equivalent for our office environment.

3. **Creating a proper office map**: Designing a detailed office map using Tiled Map Editor.

4. **Connecting frontend and backend**: Replacing placeholder data with real agent decisions and movements.

## Recent Changes

- Created project repository and initial documentation
- Established comprehensive Memory Bank structure
- Set up basic project structure with backend and frontend directories
- Implemented skeleton FastAPI backend with WebSocket endpoint
- Created basic Phaser.js frontend with placeholder visualization
- Set up Electron configuration for desktop packaging
- Added placeholder assets and basic movement visualization

## Next Steps

### Immediate Tasks (Beta Phase 1)

1. **Port core agent architecture**:

   - Port `persona.py` and cognitive modules
   - Port memory systems (associative, spatial, scratch)
   - Adapt to use LLM API for agent cognition

2. **Implement environment representation**:

   - Port `maze.py` for office environment
   - Implement tile-based world representation
   - Add collision detection and event handling

3. **Create proper office map**:

   - Design detailed office layout in Tiled
   - Export map data for frontend (JSON) and backend (CSV)
   - Implement map loading in both systems

4. **Connect frontend and backend**:
   - Replace mock data with real agent decisions
   - Create agent sprites and animations
   - Implement basic movement visualization

### Medium-Term Tasks (Beta Phase 2)

1. **Refine agent behaviors**:

   - Implement office-specific behaviors
   - Create agent roles and personalities
   - Improve agent decision-making

2. **Enhance visualization**:

   - Add pronunciatio system (emojis/status indicators)
   - Improve animations and visual feedback
   - Add basic UI elements for simulation control

3. **Testing and debugging**:
   - Test with multiple agents
   - Debug pathfinding and collision issues
   - Optimize performance

### Long-Term Tasks (Future Phases)

1. **Add React UI components**
2. **Implement agent customization**
3. **Create multiple maps and scenarios**
4. **Add advanced environment interactions**
5. **Package with Electron for distribution**

## Active Decisions & Considerations

### Architecture Decisions

1. **Single-Server Approach**: We've decided to use a single-server architecture with FastAPI and WebSockets instead of the original dual-server, file-based approach. This simplifies deployment and enables real-time communication.

2. **Original Agent Architecture**: We're keeping the original agent cognitive loop and memory systems intact initially, rather than experimenting with alternatives. This allows us to focus on getting the basic simulation working before exploring variations.

3. **WebSocket Communication**: Using WebSockets for real-time communication between frontend and backend, maintaining the same JSON structure as the original for compatibility.

4. **Phaser.js for Visualization**: Using Phaser.js for the frontend visualization due to its powerful 2D game engine capabilities and ease of use.

### Open Questions

1. **LLM Integration Strategy**:

   - How to efficiently use LLM API calls for agent cognition?
   - Should we batch process agent decisions or process them individually?
   - How to handle API rate limits and costs?

2. **Map Complexity**:

   - How detailed should the office map be for the beta version?
   - What office areas and objects are essential for basic functionality?

3. **Agent Behavior Scope**:

   - What office behaviors should be implemented first?
   - How to balance realism with performance?

4. **UI Requirements**:
   - What minimal UI elements are needed for the beta version?
   - When should we integrate React for more advanced UI?

## Important Patterns & Preferences

### Code Organization

- **Backend**: Modular structure following the original architecture's organization
- **Frontend**: Clear separation between Phaser game logic and UI components
- **Communication**: Consistent JSON structure for WebSocket messages

### Development Approach

- **Incremental Implementation**: Focus on getting basic functionality working before adding features
- **Testing First**: Test components individually before integration
- **Documentation Driven**: Keep Memory Bank updated as development progresses

### Naming Conventions

- **Backend (Python)**:

  - snake_case for variables and functions
  - CamelCase for classes
  - Descriptive names that reflect purpose

- **Frontend (JavaScript)**:
  - camelCase for variables and functions
  - PascalCase for classes and components
  - Clear, descriptive naming

## Learnings & Project Insights

### From Original Architecture

- The agent cognitive loop (perceive → retrieve → plan → execute → reflect) is the heart of the system and should be preserved.
- Memory systems (associative, spatial, scratch) are crucial for agent believability.
- The dual representation of the map (visual for frontend, logical for backend) is an effective approach.

### Technical Insights

- WebSockets provide a more efficient communication method than file-based approaches.
- FastAPI's async support is well-suited for handling multiple agent processes.
- Phaser.js offers powerful capabilities for 2D visualization and animation.

### Challenges Anticipated

- Balancing agent complexity with performance
- Efficient use of LLM API calls
- Coordinating frontend animation with backend decision-making
- Creating believable office behaviors and interactions

## Current Status Summary

We are in the **planning and setup phase** of the project. The Memory Bank has been established, and we have a clear understanding of the original architecture and our porting approach. The next step is to begin implementing the core components, starting with the backend agent architecture and basic frontend visualization.

The project is on track for a phased implementation, with the initial focus on getting a basic simulation working before adding more advanced features. The Memory Bank will be updated regularly as development progresses to maintain clear documentation of the project's evolution.
