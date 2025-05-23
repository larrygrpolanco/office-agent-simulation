/**
 * Office Agent Simulation - Frontend Game Logic (Step-Based Architecture)
 *
 * This file implements the Phaser.js game logic and WebSocket communication
 * for the Office Agent Simulation using a step-based approach suitable for AI agents.
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

// Step-based simulation state
let currentStep = 0;
let isProcessing = false;
let autoMode = false;
let autoModeTimeout = null;

let gameLayers = {};

// Initialize game when the window loads
window.onload = function () {
  game = new Phaser.Game(config);

  // Get UI elements
  statusMessage = document.getElementById('status-message');
  fpsCounter = document.getElementById('fps-counter');

  // Set up simulation button listeners
  document
    .getElementById('next-step-btn')
    .addEventListener('click', nextStep);
  document
    .getElementById('reset-btn')
    .addEventListener('click', resetSimulation);
    
  // Set up auto mode listeners
  document
    .getElementById('auto-mode-checkbox')
    .addEventListener('change', toggleAutoMode);
  document
    .getElementById('auto-delay')
    .addEventListener('change', updateAutoDelay);
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
  this.load.image(
    'int_Basement_32x32',
    'assets/the_office/visuals/map_assets/int_Basement_32x32.png'
  );
  this.load.image(
    'int_Bathroom_32x32',
    'assets/the_office/visuals/map_assets/int_Bathroom_32x32.png'
  );
  this.load.image(
    'int_Classroom_and_library_32x32',
    'assets/the_office/visuals/map_assets/int_Classroom_and_library_32x32.png'
  );
  this.load.image(
    'int_Generic_32x32',
    'assets/the_office/visuals/map_assets/int_Generic_32x32.png'
  );
  this.load.image(
    'int_Grocery_store_32x32',
    'assets/the_office/visuals/map_assets/int_Grocery_store_32x32.png'
  );
  this.load.image(
    'int_Hospital_32x32',
    'assets/the_office/visuals/map_assets/int_Hospital_32x32.png'
  );
  this.load.image(
    'int_Kitchen_32x32',
    'assets/the_office/visuals/map_assets/int_Kitchen_32x32.png'
  );

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
    const modern = tryAddTileset(
      map,
      'Modern_Office_32x32',
      'Modern_Office_32x32'
    );
    const roomBuilder = tryAddTileset(
      map,
      'Room_Builder_Office_32x32',
      'Room_Builder_Office_32x32'
    );
    const int_Basement = tryAddTileset(
      map,
      'int_Basement_32x32',
      'int_Basement_32x32'
    );
    const int_Bathroom = tryAddTileset(
      map,
      'int_Bathroom_32x32',
      'int_Bathroom_32x32'
    );
    const int_Classroom = tryAddTileset(
      map,
      'int_Classroom_and_library_32x32',
      'int_Classroom_and_library_32x32'
    );
    const int_Generic = tryAddTileset(
      map,
      'int_Generic_32x32',
      'int_Generic_32x32'
    );
    const int_Grocery = tryAddTileset(
      map,
      'int_Grocery_store_32x32',
      'int_Grocery_store_32x32'
    );
    const int_Hospital = tryAddTileset(
      map,
      'int_Hospital_32x32',
      'int_Hospital_32x32'
    );
    const int_Kitchen = tryAddTileset(
      map,
      'int_Kitchen_32x32',
      'int_Kitchen_32x32'
    );

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
    gameLayers.furnitureLayer1 = map.createLayer(
      'Furniture Visuals L1',
      allTilesets,
      0,
      0
    );
    gameLayers.furnitureLayer2 = map.createLayer(
      'Furniture Visuals L2',
      allTilesets,
      0,
      0
    );
    gameLayers.furnitureLayer3 = map.createLayer(
      'Furniture Visuals L3',
      allTilesets,
      0,
      0
    );
    gameLayers.furnitureLayer4 = map.createLayer(
      'Furniture Visuals L4',
      allTilesets,
      0,
      0
    );

    // Create collision layer (hidden by default)
    gameLayers.collisionLayer = map.createLayer(
      'Collision Layer',
      allTilesets,
      0,
      0
    );
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

  // Connect to WebSocket server
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

  // For local development, hardcode the URL
  const wsUrl = 'ws://localhost:8000/ws';
  
  // Create new WebSocket connection
  socket = new WebSocket(wsUrl);

  // Connection opened
  socket.onopen = function (event) {
    connected = true;
    updateStatus('Connected to server - Ready for simulation');
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
    // Handle plain text connection confirmation
    if (event.data === 'connected') {
      console.log('WebSocket connection established');
      return;
    }

    // Handle JSON messages
    try {
      const data = JSON.parse(event.data);

      // Validate JSON structure
      if (data.persona && typeof data.persona === 'object' && data.meta) {
        handleStepResponse(data);
      } else {
        console.warn('Received unexpected JSON format:', data);
      }
    } catch (e) {
      console.error('Failed to parse server message:', e);
      console.log('Raw server response:', event.data);
      console.log('Full error stack:', e.stack);
    }
  };
}

// Handle step response from backend
function handleStepResponse(data) {
  // Stop processing indicator
  setProcessingState(false);
  
  // Update agents
  updateAgents(data);
  
  // Update step counter
  currentStep++;
  document.getElementById('step-counter').textContent = currentStep;
  
  // Show processing time if available
  if (data.meta && data.meta.processing_time) {
    document.getElementById('processing-time').textContent = 
      `Last step: ${data.meta.processing_time}`;
  }
  
  // Update game time
  const timeElement = document.getElementById('game-time-content');
  if (timeElement && data.meta && data.meta.curr_time) {
    timeElement.innerHTML = data.meta.curr_time;
  }
  
  // Update status
  updateStatus(`Step ${currentStep} completed`);
  
  // If auto mode is enabled, schedule next step
  if (autoMode) {
    const delay = parseInt(document.getElementById('auto-delay').value);
    autoModeTimeout = setTimeout(() => {
      if (autoMode && !isProcessing) {
        nextStep();
      }
    }, delay);
  }
}

// Execute next simulation step
function nextStep() {
  if (!connected || isProcessing) {
    if (!connected) {
      updateStatus('Error: Not connected to server');
    }
    return;
  }

  // Set processing state
  setProcessingState(true);
  
  // Send step request to backend
  const stepRequest = {
    action: 'next_step',
    step_id: currentStep + 1,
    environment: getCurrentEnvironmentState()
  };
  
  socket.send(JSON.stringify(stepRequest));
  updateStatus(`Processing step ${currentStep + 1}...`);
}

// Get current environment state
function getCurrentEnvironmentState() {
  const envData = {};

  // Add each agent's position
  for (const personaName in personas) {
    const persona = personas[personaName];
    envData[personaName] = {
      x: Math.ceil(persona.x / tile_width),
      y: Math.ceil(persona.y / tile_width),
    };
  }

  return envData;
}

// Set processing state (show/hide spinner, disable buttons)
function setProcessingState(processing) {
  isProcessing = processing;
  
  const nextStepBtn = document.getElementById('next-step-btn');
  const processingIndicator = document.getElementById('processing-indicator');
  
  if (processing) {
    nextStepBtn.disabled = true;
    processingIndicator.classList.add('active');
  } else {
    nextStepBtn.disabled = false;
    processingIndicator.classList.remove('active');
  }
}

// Update agent positions and animations based on backend data
function updateAgents(movements) {
  // Create scene reference for adding new agents
  const scene = game.scene.scenes[0];
  
  for (const personaName in movements.persona) {
    const movement = movements.persona[personaName];
    
    // Create new agent if it doesn't exist
    if (!(personaName in personas)) {
      console.log(`Creating new agent: ${personaName}`);
      
      // Create agent sprite
      const x = movement.movement[0] * tile_width;
      const y = movement.movement[1] * tile_width;
      personas[personaName] = scene.add.sprite(x, y, 'agent');
      
      // Add text for speech bubble/pronunciatio
      const textStyle = { 
        font: '14px Arial', 
        fill: '#ffffff',
        backgroundColor: '#333333',
        padding: { x: 8, y: 4 },
        borderRadius: 4
      };
      pronunciatios[personaName] = scene.add.text(x, y - 40, '', textStyle);
      
      // Set initial target position
      movement_target[personaName] = [x, y];
    }
    
    // Update existing agent
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

// Toggle auto mode
function toggleAutoMode() {
  const checkbox = document.getElementById('auto-mode-checkbox');
  const delaySelect = document.getElementById('auto-delay');
  
  autoMode = checkbox.checked;
  delaySelect.disabled = !autoMode;
  
  if (autoMode) {
    updateStatus('Auto mode enabled');
    // Start auto mode if not currently processing
    if (!isProcessing && connected) {
      const delay = parseInt(delaySelect.value);
      autoModeTimeout = setTimeout(() => {
        if (autoMode && !isProcessing) {
          nextStep();
        }
      }, delay);
    }
  } else {
    updateStatus('Auto mode disabled');
    // Clear any pending auto step
    if (autoModeTimeout) {
      clearTimeout(autoModeTimeout);
      autoModeTimeout = null;
    }
  }
}

// Update auto mode delay
function updateAutoDelay() {
  // If auto mode is active and we have a pending timeout, restart it with new delay
  if (autoMode && autoModeTimeout) {
    clearTimeout(autoModeTimeout);
    const delay = parseInt(document.getElementById('auto-delay').value);
    autoModeTimeout = setTimeout(() => {
      if (autoMode && !isProcessing) {
        nextStep();
      }
    }, delay);
  }
}

// Reset simulation
function resetSimulation() {
  if (connected && socket.readyState === WebSocket.OPEN) {
    // Stop auto mode
    autoMode = false;
    document.getElementById('auto-mode-checkbox').checked = false;
    document.getElementById('auto-delay').disabled = true;
    if (autoModeTimeout) {
      clearTimeout(autoModeTimeout);
      autoModeTimeout = null;
    }
    
    // Reset processing state
    setProcessingState(false);
    
    // Reset step counter
    currentStep = 0;
    document.getElementById('step-counter').textContent = currentStep;
    
    // Clear processing time
    document.getElementById('processing-time').textContent = '';
    
    updateStatus('Resetting simulation...');
    
    socket.send(JSON.stringify({
      action: 'reset'
    }));
    
    // Reset local agent positions
    Object.values(personas).forEach((agent) => agent.destroy());
    Object.values(pronunciatios).forEach((text) => text.destroy());
    personas = {};
    pronunciatios = {};
    movement_target = {};
    
    updateStatus('Simulation reset - Ready for next step');
  } else {
    updateStatus('Error: Not connected to server');
  }
}
