# Frontend & Phaser.js Setup Guide for Generative Agents (FastAPI + WebSocket)

This guide provides step-by-step instructions for setting up the frontend visualization system for your Generative Agents simulation using Phaser.js, with a focus on integration with a FastAPI backend via WebSocket. It is designed for the new, simplified architecture (see [Agents_Architecture.md](Agents_Architecture.md)) and omits Django or file-based communication.

---

## Table of Contents

1. [Frontend Architecture Overview](#1-frontend-architecture-overview)
2. [Setting Up Phaser.js](#2-setting-up-phaserjs)
3. [Loading and Configuring Tilesets & Maps](#3-loading-and-configuring-tilesets--maps)
4. [Agent Sprites & Pronunciatio System](#4-agent-sprites--pronunciatio-system)
5. [Frontend-Backend Communication (WebSocket)](#5-frontend-backend-communication-websocket)
6. [Customizing the UI](#6-customizing-the-ui)
7. [Performance Optimization](#7-performance-optimization)

---

## 1. Frontend Architecture Overview

- **Phaser.js**: 2D game framework for rendering the map and agents.
- **HTML/CSS/JavaScript**: For UI and integration.
- **WebSocket**: Real-time communication with the FastAPI backend.
- **Electron (optional)**: For desktop packaging.

**Modes:**
- **Simulation Mode**: Real-time updates from backend.
- **Replay Mode**: (Optional) Playback of recorded simulations.

---

## 2. Setting Up Phaser.js

### Step 1: Include Phaser.js

- Use CDN:
  ```html
  <script src="https://cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.js"></script>
  ```
- Or install via npm for Electron/React integration.

### Step 2: Phaser Game Configuration

```javascript
const config = {
  type: Phaser.AUTO,
  width: 1500,
  height: 800,
  parent: "game-container",
  pixelArt: true,
  physics: {
    default: "arcade",
    arcade: { gravity: { y: 0 } }
  },
  scene: { preload, create, update },
  scale: { zoom: 0.8 }
};
const game = new Phaser.Game(config);
```

---

## 3. Loading and Configuring Tilesets & Maps

### Step 1: Preload Assets

```javascript
function preload() {
  // Load tileset images
  this.load.image("walls", "assets/visuals/tilesets/walls.png");
  this.load.image("furniture", "assets/visuals/tilesets/furniture.png");
  // ... other tilesets

  // Load the Tiled map JSON
  this.load.tilemapTiledJSON("map", "assets/visuals/office.json");

  // Load character sprites (atlas or individual images)
  this.load.atlas("atlas", "assets/characters/character.png", "assets/characters/atlas.json");
}
```

### Step 2: Create Map and Layers

```javascript
function create() {
  const map = this.make.tilemap({ key: "map" });
  const walls = map.addTilesetImage("Walls_Tileset", "walls");
  const furniture = map.addTilesetImage("Furniture_Tileset", "furniture");
  let tileset_group = [walls, furniture];

  const floorLayer = map.createLayer("Floor", tileset_group, 0, 0);
  const wallsLayer = map.createLayer("Walls", tileset_group, 0, 0);
  const furnitureLayer = map.createLayer("Furniture", tileset_group, 0, 0);

  // Set up collision
  // If you have a collision layer:
  // const collisionsLayer = map.createLayer("Collisions", tileset_group, 0, 0);
  // collisionsLayer.setCollisionByProperty({ collide: true });

  // Set layer depths
  floorLayer.setDepth(0);
  wallsLayer.setDepth(1);
  furnitureLayer.setDepth(2);
}
```

### Step 3: Camera and Controls

```javascript
// Example: create a camera follow target (invisible player sprite)
player = this.physics.add.sprite(1200, 800, "atlas", "down").setSize(30, 40).setOffset(0, 0);
player.setDepth(-1);

const camera = this.cameras.main;
camera.startFollow(player);
camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

cursors = this.input.keyboard.createCursorKeys();
```

---

## 4. Agent Sprites & Pronunciatio System

### Step 1: Create Agent Sprites

```javascript
for (let personaName in spawn_tile_loc) {
  let start_pos = [
    spawn_tile_loc[personaName][0] * tile_width + tile_width / 2,
    spawn_tile_loc[personaName][1] * tile_width + tile_width
  ];
  let new_sprite = this.physics.add.sprite(start_pos[0], start_pos[1], "atlas", "down")
    .setSize(30, 40).setOffset(0, 0);
  new_sprite.displayWidth = 40;
  new_sprite.scaleY = new_sprite.scaleX;
  personas[personaName] = new_sprite;

  // Pronunciatio (emoji/status above agent)
  pronunciatios[personaName] = this.add.text(
    new_sprite.body.x - 6, new_sprite.body.y - 42, "💼", {
      font: "24px monospace",
      fill: "#000000",
      padding: { x: 8, y: 8 },
      backgroundColor: "#ffffff",
      border: "solid",
      borderRadius: "10px"
    }
  ).setDepth(3);
}
```

### Step 2: Update Pronunciatio

- The backend sends an emoji/status for each agent in the movement JSON.
- Update the pronunciatio text in the frontend when new data arrives.

---

## 5. Frontend-Backend Communication (WebSocket)

### Step 1: Connect to FastAPI WebSocket

```javascript
const socket = new WebSocket('ws://localhost:8000/ws');

socket.onopen = () => {
  sendEnvironmentState();
};

socket.onmessage = (event) => {
  const movements = JSON.parse(event.data);
  updateAgents(movements);
};
```

### Step 2: Send Environment State

```javascript
function sendEnvironmentState() {
  const envData = {};
  for (const personaName in personas) {
    envData[personaName] = {
      x: Math.ceil(personas[personaName].body.x / tile_width),
      y: Math.ceil(personas[personaName].body.y / tile_width)
    };
  }
  socket.send(JSON.stringify(envData));
}
```

### Step 3: Update Agents on Backend Response

```javascript
function updateAgents(movements) {
  for (const personaName in movements.persona) {
    const movement = movements.persona[personaName];
    // Move agent sprite to new position
    movement_target[personaName] = [
      movement.movement[0] * tile_width,
      movement.movement[1] * tile_width
    ];
    // Update pronunciatio
    pronunciatios[personaName].setText(movement.pronunciatio);
    // Optionally update description, chat, etc.
  }
  // Update simulation time
  document.getElementById("game-time-content").innerHTML = movements.meta.curr_time;
}
```

---

## 6. Customizing the UI

- **Agent Info Panel:**  
  Display agent name, role, current task, location, meeting, and schedule.
  ```html
  <div class="media" id="on_screen_det_content-AGENT_NAME">
    <div class="media-body">
      <h2 id="name__AGENT_NAME">Alice</h2>
      <p><strong>Role:</strong> <span id="role__AGENT_NAME">Software Engineer</span></p>
      <p><strong>Current Task:</strong> <span id="current_action__AGENT_NAME"></span></p>
      <p><strong>Location:</strong> <span id="target_address__AGENT_NAME"></span></p>
      <p><strong>Current Meeting:</strong> <span id="chat__AGENT_NAME"></span></p>
      <p><strong>Schedule:</strong> <span id="schedule__AGENT_NAME"></span></p>
    </div>
  </div>
  ```

- **Time Display:**  
  Show simulation time and working hours.
  ```javascript
  let workingHours = "9:00 AM - 5:00 PM";
  document.getElementById("working-hours").innerHTML = workingHours;
  ```

---

## 7. Performance Optimization

- **Tilemap Optimization:**  
  Use culling, group similar tiles, and hide unnecessary layers.
  ```javascript
  floorLayer.setCullPadding(2);
  wallsLayer.setCullPadding(2);
  ```

- **Agent Animation Optimization:**  
  Only animate agents that are moving. Use sprite pooling for efficiency.

- **Memory Management:**  
  Limit history storage and clear unused assets for long-running simulations.

---

## References

- [Agents_Architecture.md](Agents_Architecture.md): Core architecture and communication protocol
- [Complete_Porting_Guide.md](Complete_Porting_Guide.md): Full porting roadmap
- [Map_and_Movement_Porting_Guide.md](Map_and_Movement_Porting_Guide.md): Map and movement data details

---

This guide should help you set up the frontend for your Generative Agents simulation using Phaser.js and FastAPI. Focus on real-time WebSocket communication, modular agent visualization, and a UI that can be extended with React or Electron as needed.
