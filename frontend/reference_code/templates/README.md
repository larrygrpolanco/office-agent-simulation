# Templates

This directory contains the HTML templates that form the web interface for the simulation visualization system.

## Purpose

The templates directory provides the frontend views that allow users to interact with and visualize the generative agents simulation.

## Directory Structure

- `base.html` - The master template that defines common page structure
- `demo/` - Templates for the demonstration replay mode
  - `demo.html` - Demo interface
  - `main_script.html` - JavaScript for the demo visualization
- `home/` - Templates for the main simulation interface
  - `home.html` - Main simulation view
  - `main_script.html` - Core JavaScript for the simulation visualization
  - `error_start_backend.html` - Error handling view
- `landing/` - Entry point templates
  - `landing.html` - Initial landing page
- `path_tester/` - Templates for the agent path testing tool
  - `path_tester.html` - Path testing interface
  - `main_script.html` - JavaScript for path visualization
- `persona_state/` - Templates for examining agent cognitive states
  - `persona_state.html` - Agent memory and state visualization

## Key Components

- **Phaser.js Game Engine** - The main_script.html files contain JavaScript that uses Phaser.js to render the 2D game-like visualization
- **Agent Visualization** - Characters are rendered on a tile-based map with movements and interactions
- **Conversation Display** - Speech bubbles show agent conversations
- **Memory Interface** - Persona state view shows agent memory structures
- **Simulation Controls** - Play, pause, speed control for simulations

## How Templates Work Together

1. base.html provides the common structure and loads CSS/JS dependencies
2. Specific view templates extend base.html with content for different functionality
3. main_script.html files contain most of the visualization logic
4. The Django view (in translator app) renders these templates with simulation data