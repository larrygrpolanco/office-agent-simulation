/**
 * Office Agent Simulation - Frontend Game Logic
 *
 * This file implements the Phaser.js game logic and WebSocket communication
 * for the Office Agent Simulation.
 */

// Game configuration
const config = {
  type: Phaser.AUTO,
  width: 1200,
  height: 800,
  parent: 'game-container',
  pixelArt: true,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 0 },
      debug: false,
    },
  },
  scene: {
    preload: preload,
    create: create,
    update: update,
  },
  scale: {
    mode: Phaser.Scale.RESIZE,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
};

// Global variables
let game;
let socket;
let connected = false;
let personas = {};
let pronunciatios = {};
let movement_target = {};
let tile_width = 32;
let cursors;
let statusMessage;
let fpsCounter;
let lastFpsUpdate = 0;

let gameLayers = {};

// Initialize game when the window loads
window.onload = function () {
  game = new Phaser.Game(config);

  // Get UI elements
  statusMessage = document.getElementById('status-message');
  fpsCounter = document.getElementById('fps-counter');

  // Set up simulation button listeners
  document
    .getElementById('start-btn')
    .addEventListener('click', startSimulation);
  document
    .getElementById('pause-btn')
    .addEventListener('click', pauseSimulation);
  document
    .getElementById('reset-btn')
    .addEventListener('click', resetSimulation);

};

/**
 * Preload game assets: Load the office map and all required tilesets.
 */
function preload() {
  // Load the Tiled map (JSON export)
  this.load.tilemapTiledJSON(
    'officeMap',
    'assets/the_office/visuals/the_office.json'
  );

  // Load all tileset images (names must match those used in Tiled)
  this.load.image(
    'blocks_1',
    'assets/the_office/visuals/map_assets/blocks_1.png'
  );

  // Load all new interiors tileset images (split from the original large tileset)
  this.load.image('int_Basement_32x32', 'assets/the_office/visuals/map_assets/int_Basement_32x32.png');
  this.load.image('int_Bathroom_32x32', 'assets/the_office/visuals/map_assets/int_Bathroom_32x32.png');
  this.load.image('int_Classroom_and_library_32x32', 'assets/the_office/visuals/map_assets/int_Classroom_and_library_32x32.png');
  this.load.image('int_Generic_32x32', 'assets/the_office/visuals/map_assets/int_Generic_32x32.png');
  this.load.image('int_Grocery_store_32x32', 'assets/the_office/visuals/map_assets/int_Grocery_store_32x32.png');
  this.load.image('int_Hospital_32x32', 'assets/the_office/visuals/map_assets/int_Hospital_32x32.png');
  this.load.image('int_Kitchen_32x32', 'assets/the_office/visuals/map_assets/int_Kitchen_32x32.png');

  this.load.image(
    'Modern_Office_32x32',
    'assets/the_office/visuals/map_assets/Modern_Office_32x32.png'
  );
  this.load.image(
    'Room_Builder_Office_32x32',
    'assets/the_office/visuals/map_assets/Room_Builder_Office_32x32.png'
  );

  // Load placeholder agent sprite
  this.load.image('agent', 'assets/the_office/visuals/placeholder-agent.png');

  // Show loading message
  updateStatus('Loading assets...');
}

/**
 * Create game objects: Display the office map and a placeholder agent.
 */
function create() {
  // Create the tilemap
  const map = this.make.tilemap({ key: 'officeMap' });

  // Debug: Log the map object to inspect tileset and layer names
  console.log('Phaser Tilemap object:', map);
  console.log(
    'Tilesets:',
    map.tilesets.map((ts) => ts.name)
  );
  console.log(
    'Layers:',
    map.layers.map((layer) => layer.name)
  );

  // Add tilesets and create layers
  try {
    // Helper function to try different ways of adding a tileset
    const tryAddTileset = (map, tilesetName, imageKey) => {
      try {
        // First try the standard way
        return map.addTilesetImage(tilesetName, imageKey);
      } catch (e) {
        console.warn(
          `Failed to add tileset ${tilesetName} with key ${imageKey}. Trying alternatives...`
        );

        // Try with just the filename (no path)
        const tilesetData = map.tilesets.find((ts) => ts.name === tilesetName);
        if (tilesetData && tilesetData.image) {
          const imagePath = tilesetData.image;
          const filename = imagePath.split('/').pop().split('\\').pop();
          const filenameWithoutExt = filename.split('.')[0];

          console.log(`Trying with filename: ${filenameWithoutExt}`);
          try {
            return map.addTilesetImage(tilesetName, filenameWithoutExt);
          } catch (e2) {
            // Last resort: try with the tileset name itself
            console.log(`Trying with tileset name itself: ${tilesetName}`);
            return map.addTilesetImage(tilesetName);
          }
        }
        throw e; // Re-throw if we couldn't find alternatives
      }
    };

    // Add all tilesets (names must match those in Tiled and as loaded above)
    const blocks = tryAddTileset(map, 'blocks_1', 'blocks_1');
    const modern = tryAddTileset(map, 'Modern_Office_32x32', 'Modern_Office_32x32');
    const roomBuilder = tryAddTileset(map, 'Room_Builder_Office_32x32', 'Room_Builder_Office_32x32');
    const int_Basement = tryAddTileset(map, 'int_Basement_32x32', 'int_Basement_32x32');
    const int_Bathroom = tryAddTileset(map, 'int_Bathroom_32x32', 'int_Bathroom_32x32');
    const int_Classroom = tryAddTileset(map, 'int_Classroom_and_library_32x32', 'int_Classroom_and_library_32x32');
    const int_Generic = tryAddTileset(map, 'int_Generic_32x32', 'int_Generic_32x32');
    const int_Grocery = tryAddTileset(map, 'int_Grocery_store_32x32', 'int_Grocery_store_32x32');
    const int_Hospital = tryAddTileset(map, 'int_Hospital_32x32', 'int_Hospital_32x32');
    const int_Kitchen = tryAddTileset(map, 'int_Kitchen_32x32', 'int_Kitchen_32x32');

    const allTilesets = [
      blocks,
      modern,
      roomBuilder,
      int_Basement,
      int_Bathroom,
      int_Classroom,
      int_Generic,
      int_Grocery,
      int_Hospital,
      int_Kitchen,
    ];

    console.log('Tilesets added successfully');

    // Create map layers (layer names must match those in Tiled)
    gameLayers.floorLayer = map.createLayer('Floor Visuals', allTilesets, 0, 0);
    gameLayers.wallLayer = map.createLayer('Wall Visuals', allTilesets, 0, 0);

    // Create furniture layers
    gameLayers.furnitureLayer1 = map.createLayer('Furniture Visuals L1', allTilesets, 0, 0);
    gameLayers.furnitureLayer2 = map.createLayer('Furniture Visuals L2', allTilesets, 0, 0);
    gameLayers.furnitureLayer3 = map.createLayer('Furniture Visuals L3', allTilesets, 0, 0);
    gameLayers.furnitureLayer4 = map.createLayer('Furniture Visuals L4', allTilesets, 0, 0);

    // Create collision layer (hidden by default)
    gameLayers.collisionLayer = map.createLayer('Collision Layer', allTilesets, 0, 0);
    gameLayers.collisionLayer.setVisible(false);

    updateStatus('Map loaded successfully');
  } catch (error) {
    console.error('Error loading map:', error);
    console.log(
      'Tileset names in map:',
      map.tilesets.map((ts) => ts.name)
    );
    console.log(
      'Image sources in map:',
      map.tilesets.map((ts) => ts.image)
    );
    console.log(
      'Layer names in map:',
      map.layers.map((layer) => layer.name)
    );

    updateStatus('Error loading map.');
  }

  // Set up camera bounds
  this.cameras.main.setBounds(0, 0, map.widthInPixels, map.heightInPixels);
  this.cameras.main.setZoom(1);

  // Set up keyboard input
  cursors = this.input.keyboard.createCursorKeys();

  // Connect to WebSocket server (can be left as is for now)
  connectWebSocket();

  // Show ready message
  updateStatus('Ready to start simulation');
}

// Update game state
function update(time, delta) {
  // Update FPS counter every 500ms
  if (time - lastFpsUpdate > 500) {
    fpsCounter.textContent = `FPS: ${Math.round(game.loop.actualFps)}`;
    lastFpsUpdate = time;
  }

  // Move agents towards their targets
  for (const personaName in personas) {
    const persona = personas[personaName];
    const pronunciatio = pronunciatios[personaName];

    if (movement_target[personaName]) {
      // Calculate direction
      const targetX = movement_target[personaName][0];
      const targetY = movement_target[personaName][1];

      // Move towards target
      const speed = 2;

      if (Math.abs(persona.x - targetX) > speed) {
        if (persona.x < targetX) {
          persona.x += speed;
        } else {
          persona.x -= speed;
        }
      }

      if (Math.abs(persona.y - targetY) > speed) {
        if (persona.y < targetY) {
          persona.y += speed;
        } else {
          persona.y -= speed;
        }
      }

      // Update speech bubble position
      pronunciatio.x = persona.x;
      pronunciatio.y = persona.y - 40;
    }
  }

  // Handle camera movement with arrow keys
  if (cursors.left.isDown) {
    this.cameras.main.scrollX -= 8;
  } else if (cursors.right.isDown) {
    this.cameras.main.scrollX += 8;
  }

  if (cursors.up.isDown) {
    this.cameras.main.scrollY -= 8;
  } else if (cursors.down.isDown) {
    this.cameras.main.scrollY += 8;
  }
}


// Connect to WebSocket server
function connectWebSocket() {
  // Close existing connection if any
  if (socket) {
    socket.close();
  }

  // Determine WebSocket URL (same host, different protocol)
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws`;

  // For local development, hardcode the URL
  // const wsUrl = 'ws://localhost:8000/ws';

  // Create new WebSocket connection
  socket = new WebSocket(wsUrl);

  // Connection opened
  socket.onopen = function (event) {
    connected = true;
    updateStatus('Connected to server');
    sendEnvironmentState();
  };

  // Connection closed
  socket.onclose = function (event) {
    connected = false;
    updateStatus('Disconnected from server');

    // Try to reconnect after 5 seconds
    setTimeout(connectWebSocket, 5000);
  };

  // Connection error
  socket.onerror = function (error) {
    connected = false;
    updateStatus('WebSocket error');
    console.error('WebSocket error:', error);
  };

  // Message received
  socket.onmessage = function (event) {
    const movements = JSON.parse(event.data);
    updateAgents(movements);
  };
}

// Send current environment state to backend
function sendEnvironmentState() {
  if (connected && socket.readyState === WebSocket.OPEN) {
    const envData = {};

    // Add each agent's position
    for (const personaName in personas) {
      const persona = personas[personaName];

      envData[personaName] = {
        x: Math.ceil(persona.x / tile_width),
        y: Math.ceil(persona.y / tile_width),
      };
    }

    socket.send(JSON.stringify(envData));
  }

  // Schedule next update
  setTimeout(sendEnvironmentState, 1000);
}

// Update agent positions and animations based on backend data
function updateAgents(movements) {
  for (const personaName in movements.persona) {
    if (personaName in personas) {
      const movement = movements.persona[personaName];

      // Set target position
      movement_target[personaName] = [
        movement.movement[0] * tile_width,
        movement.movement[1] * tile_width,
      ];

      // Update speech bubble
      if (movement.pronunciatio) {
        pronunciatios[personaName].setText(movement.pronunciatio);
      }

      // Update agent info in UI
      updateAgentInfo(personaName, movement.description);
    }
  }

  // Update game time
  const timeElement = document.getElementById('game-time-content');
  if (timeElement && movements.meta && movements.meta.curr_time) {
    timeElement.innerHTML = movements.meta.curr_time;
  }
}

// Update agent information in the UI
function updateAgentInfo(personaName, description) {
  const agentElement = document.getElementById(
    `agent-${personaName.split(' ')[0]}`
  );
  if (agentElement) {
    const taskElement = agentElement.querySelector('.agent-task');
    const locationElement = agentElement.querySelector('.agent-location');

    if (description) {
      // Extract task and location from description
      // Format: "task @ location"
      const parts = description.split(' @ ');
      if (parts.length === 2) {
        if (taskElement) taskElement.textContent = parts[0];
        if (locationElement) locationElement.textContent = parts[1];
      }
    }
  }
}

// Update status message
function updateStatus(message) {
  if (statusMessage) {
    statusMessage.textContent = message;
  }
}


// Button handlers
function startSimulation() {
  updateStatus('Simulation running');
  // Additional logic to start/resume simulation
}

function pauseSimulation() {
  updateStatus('Simulation paused');
  // Additional logic to pause simulation
}

function resetSimulation() {
  updateStatus('Simulation reset');
  // Additional logic to reset simulation
}
