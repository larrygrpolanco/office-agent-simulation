# Static Directories

This folder contains the static assets used by the simulation visualization system.

## Purpose

The static_dirs directory stores all the frontend assets required to visualize the agents, environment, and user interface elements.

## Directory Structure

- `assets/` - Core game assets
  - `characters/` - Agent profile images and data
    - Character PNG files (e.g., `Isabella_Rodriguez.png`, `Klaus_Mueller.png`)
    - `atlas.json` - Character sprite mapping
  - `speech_bubble/` - Conversation visualization assets
  - `the_ville/` - Environment-specific assets and initial agent history
- `css/` - Stylesheet files
  - `style.css` - Main stylesheet for the web interface
- `img/` - Additional image assets
  - `atlas.png` - Spritesheet for visualization

## How These Assets Are Used

1. Character images are displayed in the UI when agents interact or speak
2. Speech bubbles visualize conversations between agents
3. The Ville environment assets define the simulation world
4. Initial agent history files provide the starting state for simulations
5. CSS stylesheets control the appearance of the web interface

## Key Files

- `atlas.json` - Defines the sprite mapping for character visualization
- `agent_history_init_n25.csv` - Initial history data for 25-agent simulations
- `agent_history_init_n3.csv` - Initial history data for 3-agent simulations