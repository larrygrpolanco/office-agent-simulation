# Frontend Server

This Django-based web application serves as the visualization and interaction layer for the generative agents human behavior simulation system.

## Purpose

The frontend server provides a web interface for:
- Visualizing agent behaviors in a virtual environment ("The Ville")
- Running simulations and viewing replays
- Examining agent memory, conversations, and cognitive states
- Testing agent navigation paths

## Directory Structure

- `frontend_server/` - Django core configuration (settings, urls, wsgi)
- `translator/` - Django app containing views and data processing logic
- `templates/` - HTML templates for the visualization interfaces
- `static_dirs/` - Static assets (images, CSS, character data)
- `storage/` - Complete simulation data in JSON format
- `compressed_storage/` - Optimized simulation data for replays
- `temp_storage/` - Temporary data for active simulations

## Key Files

- `manage.py` - Django management script
- `global_methods.py` - Utility functions for the simulation
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment configuration

## How It Works

The frontend server loads simulation data from JSON files and renders agent positions, movements, and interactions in a game-like interface. It communicates with the backend simulation system to:

1. Initialize environments and agents
2. Process agent movements and interactions
3. Visualize agent conversations and behaviors
4. Record and replay simulations
5. Provide detailed views of agent cognitive states

## Dependencies

- Django web framework
- Phaser.js for the 2D game visualization
- SQLite for data persistence