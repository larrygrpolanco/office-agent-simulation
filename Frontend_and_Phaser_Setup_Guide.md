# Frontend & Phaser.js Setup Guide for Generative Agents

This guide provides detailed instructions for setting up the frontend visualization system for your Generative Agents simulation, with a focus on Phaser.js integration, tileset loading, and the "pronunciatio" system.

## Table of Contents

1. [Understanding the Frontend Architecture](#1-understanding-the-frontend-architecture)
2. [Setting Up Phaser.js](#2-setting-up-phaserjs)
3. [Loading and Configuring Tilesets](#3-loading-and-configuring-tilesets)
4. [The Pronunciatio System](#4-the-pronunciatio-system)
5. [Frontend-Backend Communication](#5-frontend-backend-communication)
6. [Customizing the UI](#6-customizing-the-ui)
7. [Performance Optimization](#7-performance-optimization)

## 1. Understanding the Frontend Architecture

The frontend of the Generative Agents system is built on:

- **Django**: Serves the web application and handles communication with the backend
- **Phaser.js**: A 2D game framework that renders the map and agents
- **HTML/CSS/JavaScript**: Standard web technologies for the UI

The frontend has two main modes:
- **Simulation Mode**: Real-time interaction with the backend
- **Replay Mode**: Playback of pre-recorded simulations

Key files:
- `templates/demo/demo.html`: Main template for the simulation view
- `templates/demo/main_script.html`: Contains the Phaser.js setup and game logic
- `templates/path_tester/path_tester.html`: Tool for testing pathfinding
- `translator/views.py`: Django views that handle communication with the backend

## 2. Setting Up Phaser.js

### Step 1: Include Phaser.js

Phaser.js is loaded from a CDN in the template:

```html
<script src='https://cdn.jsdelivr.net/npm/phaser@3.55.2/dist/phaser.js'></script>
```

You can either continue using the CDN or download and host Phaser locally.

### Step 2: Configure Phaser

The Phaser configuration is defined in `main_script.html`:

```javascript
const config = {
  type: Phaser.AUTO,
  width: 1500,
  height: 800,
  parent: "game-container",
  pixelArt: true,
  physics: {
    default: "arcade",
    arcade: {
      gravity: { y: 0 }
    }
  },
  scene: {
    preload: preload,
    create: create,
    update: update
  },
  scale: {zoom: 0.8}
};

const game = new Phaser.Game(config);
```

Key configuration options:
- `width` and `height`: Canvas dimensions
- `parent`: HTML element ID where the game will be rendered
- `pixelArt`: Enable pixel art mode for crisp rendering
- `physics`: Physics engine configuration
- `scene`: Functions for the game lifecycle
- `scale.zoom`: Overall zoom level

### Step 3: Implement Game Lifecycle Functions

Phaser uses three main lifecycle functions:

1. **`preload()`**: Loads all assets (images, tilemaps, etc.)
2. **`create()`**: Sets up the game world after assets are loaded
3. **`update()`**: Runs on every frame to handle game logic

## 3. Loading and Configuring Tilesets

### Step 1: Preload Assets

In the `preload()` function, load your map and tilesets:

```javascript
function preload() {
  // Load tileset images
  this.load.image("walls", "{% static 'assets/your_office/visuals/tilesets/walls.png' %}");
  this.load.image("furniture", "{% static 'assets/your_office/visuals/tilesets/furniture.png' %}");
  // ... other tilesets
  
  // Load the Tiled map JSON
  this.load.tilemapTiledJSON("map", "{% static 'assets/your_office/visuals/office.json' %}");
  
  // Load character sprites
  this.load.atlas("atlas", "{% static 'assets/characters/character.png' %}", 
                         "{% static 'assets/characters/atlas.json' %}");
}
```

**Important Notes:**
- The first parameter in `load.image()` is a key you'll use to reference the asset
- The second parameter is the file path (using Django's `static` template tag)
- For the map, use `tilemapTiledJSON` to load the JSON export from Tiled
- Character sprites use an atlas for animations

### Step 2: Create the Map in the `create()` Function

```javascript
function create() {
  // Create the tilemap from the loaded JSON
  const map = this.make.tilemap({ key: "map" });
  
  // Add the tilesets to the map
  // First parameter: name in Tiled, second parameter: key from preload
  const walls = map.addTilesetImage("Walls_Tileset", "walls");
  const furniture = map.addTilesetImage("Furniture_Tileset", "furniture");
  
  // Group tilesets for convenience
  let tileset_group = [walls, furniture];
  
  // Create layers from the map
  const floorLayer = map.createLayer("Floor", tileset_group, 0, 0);
  const wallsLayer = map.createLayer("Walls", tileset_group, 0, 0);
  const furnitureLayer = map.createLayer("Furniture", tileset_group, 0, 0);
  const collisionsLayer = map.createLayer("Collisions", collisions, 0, 0);
  
  // Set up collision
  collisionsLayer.setCollisionByProperty({ collide: true });
  
  // Set layer depths (higher numbers appear on top)
  floorLayer.setDepth(0);
  wallsLayer.setDepth(1);
  furnitureLayer.setDepth(2);
  collisionsLayer.setDepth(-1); // Hidden
}
```

**Important Notes:**
- The first parameter in `addTilesetImage()` must match the name in your Tiled project
- The second parameter must match the key used in `preload()`
- Layer names must match those in your Tiled project
- Set appropriate depths to ensure correct rendering order

### Step 3: Set Up Camera and Controls

```javascript
// Create a camera follow target
player = this.physics.add.sprite(1200, 800, "atlas", "down")
                 .setSize(30, 40)
                 .setOffset(0, 0);
player.setDepth(-1); // Make invisible but keep for camera

// Set up camera
const camera = this.cameras.main;
camera.startFollow(player);
camera.setBounds(0, 0, map.widthInPixels, map.heightInPixels);

// Set up keyboard controls
cursors = this.input.keyboard.createCursorKeys();
```

### Step 4: Create Agent Sprites

```javascript
// For each agent in your simulation
for (let i=0; i<Object.keys(spawn_tile_loc).length; i++) { 
  let persona_name = Object.keys(spawn_tile_loc)[i];
  let start_pos = [spawn_tile_loc[persona_name][0] * tile_width + tile_width / 2, 
                   spawn_tile_loc[persona_name][1] * tile_width + tile_width];
  
  // Create the sprite
  let new_sprite = this.physics.add
                       .sprite(start_pos[0], start_pos[1], persona_name, "down")
                       .setSize(30, 40)
                       .setOffset(0, 0);
  
  // Scale the sprite if needed
  new_sprite.displayWidth = 40;
  new_sprite.scaleY = new_sprite.scaleX;
  
  // Store the sprite for later reference
  personas[persona_name] = new_sprite;
  
  // Create the pronunciatio text
  pronunciatios[persona_name] = this.add.text(
                                 new_sprite.body.x - 6, 
                                 new_sprite.body.y - 42, 
                                 "🦁", {
                                 font: "24px monospace", 
                                 fill: "#000000", 
                                 padding: { x: 8, y: 8}, 
                                 border:"solid",
                                 borderRadius:"10px"}).setDepth(3);
}
```

## 4. The Pronunciatio System

### What is "Pronunciatio"?

"Pronunciatio" is a term borrowed from classical rhetoric, referring to the delivery or pronunciation of a speech, including gestures and expressions. In the Generative Agents system, it serves as a visual shorthand (using emojis) to indicate what an agent is currently doing.

The term choice is somewhat unusual and may be a reference to the rhetorical concept of "delivery" or "expression" - how an agent expresses their current state visually. It's essentially the "emote" or "status icon" for each agent.

### How Pronunciatio Works

1. **Backend Generation**: When an agent decides on an action, the backend generates an appropriate emoji in `generate_action_pronunciatio()` (in `persona/cognitive_modules/execute.py`)

2. **JSON Communication**: The emoji is included in the movement JSON sent to the frontend:
   ```json
   {
     "persona": {
       "Isabella Rodriguez": {
         "movement": [58, 9],
         "pronunciatio": "📝",
         "description": "writing her next novel @ double studio:common room:sofa",
         "chat": null
       }
     }
   }
   ```

3. **Frontend Display**: The frontend displays this emoji above the agent:
   ```javascript
   pronunciatios[persona_name].setText(initials + ": " + pronunciatio_content);
   ```

### Customizing Pronunciatio

To customize the pronunciatio system for your office simulation:

1. **Modify the Prompt**: The backend uses an LLM prompt to generate appropriate emojis. Find and modify this prompt in `persona/prompt_template/run_gpt_prompt.py` to include office-appropriate actions:

   ```python
   def run_gpt_prompt_pronunciatio(act_desp, persona):
       """
       Given an action description, returns an emoji that represents it.
       """
       prompt = f"Given the action '{act_desp}', provide a single emoji that best represents this action in an office environment.\n\n"
       prompt += "Examples:\n"
       prompt += "typing on computer → 💻\n"
       prompt += "in a meeting → 🗣️\n"
       prompt += "having coffee → ☕\n"
       prompt += "reading documents → 📄\n"
       prompt += "on a phone call → 📱\n"
       # Add more office-specific examples
       
       # Call LLM with prompt
       # ...
   ```

2. **Frontend Styling**: Adjust the styling of the pronunciatio text in the frontend:

   ```javascript
   pronunciatios[persona_name] = this.add.text(
     new_sprite.body.x - 6, 
     new_sprite.body.y - 42, 
     "💼", {
     font: "24px monospace", 
     fill: "#000000", 
     padding: { x: 8, y: 8}, 
     backgroundColor: "#ffffff",
     border: "solid",
     borderRadius: "10px"
   }).setDepth(3);
   ```

## 5. Frontend-Backend Communication

### Simulation Mode Communication

In simulation mode, the frontend and backend communicate through JSON files:

1. **Frontend → Backend**: The frontend sends the current state of all agents to the backend:
   ```javascript
   // Create environment state
   let environment = {};
   for (let i=0; i<Object.keys(personas).length; i++) {
     let persona_name = Object.keys(personas)[i];
     environment[persona_name] = {
       "x": Math.ceil(personas[persona_name].body.x / tile_width),
       "y": Math.ceil(personas[persona_name].body.y / tile_width)
     };
   }
   
   // Send to backend via AJAX
   $.ajax({
     url: "{% url 'process_environment' %}",
     type: "POST",
     data: JSON.stringify({
       "step": step,
       "sim_code": sim_code,
       "environment": environment
     }),
     contentType: "application/json",
     success: function(response) {
       // Handle success
     }
   });
   ```

2. **Backend → Frontend**: The frontend polls for movement updates:
   ```javascript
   $.ajax({
     url: "{% url 'update_environment' %}",
     type: "POST",
     data: JSON.stringify({
       "step": step,
       "sim_code": sim_code
     }),
     contentType: "application/json",
     success: function(response) {
       if (response["<step>"] == step) {
         // Process movement data
         for (let persona_name in response["persona"]) {
           let movement = response["persona"][persona_name]["movement"];
           let pronunciatio = response["persona"][persona_name]["pronunciatio"];
           // Update agent position and state
         }
       }
     }
   });
   ```

### Replay Mode Communication

In replay mode, all movement data is loaded at once:

```javascript
// In Django view
all_movement = dict()
for int_key in range(step+1, len(raw_all_movement.keys())): 
  all_movement[int_key] = raw_all_movement[str(int_key)]

context = {
  "all_movement": json.dumps(all_movement)
}

// In JavaScript
let all_movement = {{ all_movement|safe }};
```

## 6. Customizing the UI

### Agent Information Panel

The demo includes an information panel for each agent:

```html
<div class="media" id="on_screen_det_content-{{p.underscore}}">
  <div class="media-left media-middle">
    <a href="#">
      <img src="{% static image_static %}" style="width:5em"> 
    </a>
  </div>
  <div class="media-body">
    <h2 id="name__{{ p.underscore }}">{{p.original}}</h2>
    <p><strong>Current Action:</strong> <span id="current_action__{{ p.underscore }}"></span></p>
    <p><strong>Location:</strong> <span id="target_address__{{ p.underscore }}"></span></p>
    <p><strong>Current Conversation:</strong> <span id="chat__{{ p.underscore }}"></span></p>
  </div>
</div>
```

Update this to include office-appropriate information:

```html
<div class="media" id="on_screen_det_content-{{p.underscore}}">
  <div class="media-left media-middle">
    <a href="#">
      <img src="{% static image_static %}" style="width:5em"> 
    </a>
  </div>
  <div class="media-body">
    <h2 id="name__{{ p.underscore }}">{{p.original}}</h2>
    <p><strong>Role:</strong> <span id="role__{{ p.underscore }}">Software Engineer</span></p>
    <p><strong>Current Task:</strong> <span id="current_action__{{ p.underscore }}"></span></p>
    <p><strong>Location:</strong> <span id="target_address__{{ p.underscore }}"></span></p>
    <p><strong>Current Meeting:</strong> <span id="chat__{{ p.underscore }}"></span></p>
    <p><strong>Schedule:</strong> <span id="schedule__{{ p.underscore }}"></span></p>
  </div>
</div>
```

### Time Display

The simulation includes a time display that updates as the simulation progresses:

```javascript
let start_datetime = new Date(Date.parse("{{start_datetime}}"));
var datetime_options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
document.getElementById("game-time-content").innerHTML = start_datetime.toLocaleTimeString("en-US", datetime_options);

// Update time in update() function
start_datetime = new Date(start_datetime.getTime() + step_size);
document.getElementById("game-time-content").innerHTML = start_datetime.toLocaleTimeString("en-US", datetime_options);
```

Customize this for your office simulation:

```javascript
// Add working hours display
let workingHours = "9:00 AM - 5:00 PM";
document.getElementById("working-hours").innerHTML = workingHours;

// Add day progress indicator
let dayProgress = Math.min(100, (start_datetime.getHours() - 9) * 100 / 8);
document.getElementById("day-progress").style.width = dayProgress + "%";
```

## 7. Performance Optimization

### Tilemap Optimization

For large office maps:

1. **Use Tile Layers Efficiently**: Group similar tiles on the same layer
2. **Limit Visible Layers**: Hide layers that aren't necessary for gameplay
3. **Use Culling**: Enable culling to only render visible tiles

```javascript
// Enable culling
floorLayer.setCullPadding(2);
wallsLayer.setCullPadding(2);
```

### Agent Animation Optimization

For simulations with many agents:

1. **Limit Animation Updates**: Only animate agents that are moving
2. **Use Sprite Pooling**: Reuse sprite objects for efficiency
3. **Disable Physics for Distant Agents**: Only enable physics for nearby agents

```javascript
// Only animate if moving
if (curr_persona.body.x !== movement_target[curr_persona_name][0] || 
    curr_persona.body.y !== movement_target[curr_persona_name][1]) {
  // Play animation
} else {
  // Stop animation
  curr_persona.anims.stop();
}
```

### Memory Management

For long-running simulations:

1. **Clear Unused Assets**: Unload assets that are no longer needed
2. **Limit History**: Don't store unlimited history in memory
3. **Use Compressed Storage**: For replay data, use compressed formats

```javascript
// Limit history storage
if (Object.keys(all_movement).length > 1000) {
  // Remove oldest entries
  const oldest_key = Math.min(...Object.keys(all_movement).map(Number));
  delete all_movement[oldest_key];
}
```

---

This guide should help you set up the frontend visualization system for your Generative Agents office simulation. The key is understanding how Phaser.js integrates with the backend data and how to customize the visualization for your specific needs.
