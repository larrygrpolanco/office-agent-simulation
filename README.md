# Generative Agents Porting Guide

This repository contains comprehensive guides for porting the Generative Agents human behavior simulation system from "The Ville" to your custom office simulation environment.

## Overview

The Generative Agents system is a sophisticated simulation of human behavior that combines:

- **Cognitive Architecture**: Agents with memory, planning, and reflection capabilities
- **Spatial Reasoning**: Navigation and interaction with a virtual environment
- **Social Dynamics**: Conversations and relationships between agents
- **Visualization**: A frontend for observing and interacting with the simulation

Porting this system to an office environment involves understanding and adapting each of these components.

## Guide Structure

This repository contains three complementary guides:

### 1. [Map & Movement Porting Guide](Map_and_Movement_Porting_Guide.md)

Focuses on the spatial aspects of the simulation:

- Understanding the dual representation of maps (TMX for frontend, CSVs for backend)
- Creating a custom office map using Tiled Map Editor
- Generating the necessary backend data files
- Configuring the pathfinding system
- Handling agent-object and agent-agent interactions

This guide is essential for creating the physical environment of your office simulation.

### 2. [Frontend & Phaser.js Setup Guide](Frontend_and_Phaser_Setup_Guide.md)

Focuses on the visualization aspects:

- Setting up Phaser.js for rendering the office environment
- Loading and configuring tilesets
- Understanding the "pronunciatio" system (action emojis)
- Implementing frontend-backend communication
- Customizing the user interface
- Optimizing performance

This guide is crucial for creating an engaging visual representation of your simulation.

### 3. [Complete Porting Guide](Complete_Porting_Guide.md)

Provides a comprehensive roadmap that ties everything together:

- System architecture overview
- Step-by-step project roadmap
- Map creation and representation
- Backend and frontend setup
- Agent cognition and behavior customization
- Testing and debugging strategies
- Advanced customization options
- Deployment considerations

This guide serves as the main reference for the entire porting process.

## Key Concepts Explained

### The Dual-Representation Approach

The Generative Agents system uses two separate representations of the environment:

1. **Frontend (Visual) Representation**: A TMX file created with Tiled Map Editor, loaded by Phaser.js for rendering
2. **Backend (Logical) Representation**: A set of CSV matrices and legend files used by the Python backend for agent cognition and pathfinding

This separation allows the backend to run headless for experiments while providing a visual interface when needed.

### The Agent Cognitive Loop

Agents follow a five-step cognitive loop:

1. **Perceive**: Observe the environment and other agents
2. **Retrieve**: Recall relevant memories
3. **Plan**: Decide on actions based on perceptions and memories
4. **Execute**: Translate plans into physical movements
5. **Reflect**: Form higher-level thoughts about experiences

This loop is implemented in the backend and drives agent behavior.

### The Pronunciatio System

"Pronunciatio" is the term used for the visual representation of an agent's current action, displayed as an emoji above the agent. The term comes from classical rhetoric, referring to the delivery or expression of a speech.

## Getting Started

1. Begin with the [Complete Porting Guide](Complete_Porting_Guide.md) to understand the overall process
2. Refer to the [Map & Movement Porting Guide](Map_and_Movement_Porting_Guide.md) for detailed instructions on creating your office environment
3. Use the [Frontend & Phaser.js Setup Guide](Frontend_and_Phaser_Setup_Guide.md) for implementing the visualization

## Original System References

The original Generative Agents system is described in:

- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology.

The system consists of two main components:
- A backend server (in the `reverie/` directory) that implements the agent cognitive architecture
- A frontend server (in the `environment/frontend_server/` directory) that visualizes the simulation

## Customization Tips

When adapting the system to an office environment, consider:

1. **Office-Specific Behaviors**: Meetings, desk work, coffee breaks, etc.
2. **Professional Relationships**: Colleagues, managers, clients, etc.
3. **Work Schedules**: 9-5 workday, lunch breaks, meetings, etc.
4. **Office Layout**: Reception, meeting rooms, individual workspaces, break areas, etc.

These aspects should be reflected in both the physical environment and the agent cognition.

---

By following these guides, you can create a realistic simulation of human behavior in an office environment, enabling research, training, or entertainment applications.
