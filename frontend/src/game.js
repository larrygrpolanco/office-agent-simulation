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
    parent: "game-container",
    pixelArt: true,
    physics: {
        default: "arcade",
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    scale: {
        mode: Phaser.Scale.RESIZE,
        autoCenter: Phaser.Scale.CENTER_BOTH
    }
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

// Initialize game when the window loads
window.onload = function() {
    game = new Phaser.Game(config);
    
    // Get UI elements
    statusMessage = document.getElementById("status-message");
    fpsCounter = document.getElementById("fps-counter");
    
    // Set up button listeners
    document.getElementById("start-btn").addEventListener("click", startSimulation);
    document.getElementById("pause-btn").addEventListener("click", pauseSimulation);
    document.getElementById("reset-btn").addEventListener("click", resetSimulation);
};

// Preload game assets
function preload() {
    // Load tileset images (placeholder - will need actual assets)
    this.load.image("tiles", "assets/visuals/placeholder-tiles.png");
    
    // Load the map (placeholder - will need actual map)
    // this.load.tilemapTiledJSON("map", "assets/visuals/office-map.json");
    
    // Load character sprites (placeholder - will need actual sprites)
    this.load.image("agent", "assets/visuals/placeholder-agent.png");
    
    // Show loading message
    updateStatus("Loading assets...");
}

// Create game objects
function create() {
    // Create a placeholder map (until we have a real tilemap)
    createPlaceholderMap(this);
    
    // Create placeholder agents
    createPlaceholderAgents(this);
    
    // Set up camera
    this.cameras.main.setBounds(0, 0, 1600, 1200);
    this.cameras.main.setZoom(1);
    
    // Set up keyboard input
    cursors = this.input.keyboard.createCursorKeys();
    
    // Connect to WebSocket server
    connectWebSocket();
    
    // Show ready message
    updateStatus("Ready to start simulation");
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

// Create a placeholder map until we have a real tilemap
function createPlaceholderMap(scene) {
    // Create a grid of rectangles to represent the office
    const graphics = scene.add.graphics();
    
    // Floor
    graphics.fillStyle(0x555555);
    graphics.fillRect(0, 0, 1600, 1200);
    
    // Grid lines
    graphics.lineStyle(1, 0x666666);
    for (let x = 0; x < 1600; x += tile_width) {
        graphics.moveTo(x, 0);
        graphics.lineTo(x, 1200);
    }
    for (let y = 0; y < 1200; y += tile_width) {
        graphics.moveTo(0, y);
        graphics.lineTo(1600, y);
    }
    graphics.strokePath();
    
    // Walls
    graphics.fillStyle(0x333333);
    // Outer walls
    graphics.fillRect(0, 0, 1600, 32);
    graphics.fillRect(0, 0, 32, 1200);
    graphics.fillRect(0, 1168, 1600, 32);
    graphics.fillRect(1568, 0, 32, 1200);
    
    // Inner walls (just some examples)
    graphics.fillRect(400, 0, 32, 400);
    graphics.fillRect(400, 400, 400, 32);
    graphics.fillRect(1000, 400, 32, 400);
    
    // Add some text labels
    scene.add.text(200, 200, "Manager's Office", { color: '#ffffff' });
    scene.add.text(600, 200, "Sales Department", { color: '#ffffff' });
    scene.add.text(600, 600, "Break Room", { color: '#ffffff' });
    scene.add.text(200, 600, "Reception", { color: '#ffffff' });
}

// Create placeholder agents until we have real sprites and data
function createPlaceholderAgents(scene) {
    // Create some placeholder agents
    const agentConfigs = [
        { name: "Michael Scott", x: 200, y: 200, color: 0xff0000 },
        { name: "Jim Halpert", x: 600, y: 200, color: 0x00ff00 }
    ];
    
    for (const config of agentConfigs) {
        // Create agent sprite
        const agent = scene.add.circle(config.x, config.y, 16, config.color);
        agent.setDepth(10);
        personas[config.name] = agent;
        
        // Create pronunciatio (speech bubble)
        const pronunciatio = scene.add.text(
            config.x,
            config.y - 40,
            "💼",
            {
                font: "24px monospace",
                fill: "#000000",
                backgroundColor: "#ffffff",
                padding: { x: 8, y: 8 }
            }
        );
        pronunciatio.setDepth(11);
        pronunciatios[config.name] = pronunciatio;
        
        // Set initial target position
        movement_target[config.name] = [config.x, config.y];
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
    socket.onopen = function(event) {
        connected = true;
        updateStatus("Connected to server");
        sendEnvironmentState();
    };
    
    // Connection closed
    socket.onclose = function(event) {
        connected = false;
        updateStatus("Disconnected from server");
        
        // Try to reconnect after 5 seconds
        setTimeout(connectWebSocket, 5000);
    };
    
    // Connection error
    socket.onerror = function(error) {
        connected = false;
        updateStatus("WebSocket error");
        console.error("WebSocket error:", error);
    };
    
    // Message received
    socket.onmessage = function(event) {
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
                y: Math.ceil(persona.y / tile_width)
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
                movement.movement[1] * tile_width
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
    const timeElement = document.getElementById("game-time-content");
    if (timeElement && movements.meta && movements.meta.curr_time) {
        timeElement.innerHTML = movements.meta.curr_time;
    }
}

// Update agent information in the UI
function updateAgentInfo(personaName, description) {
    const agentElement = document.getElementById(`agent-${personaName.split(' ')[0]}`);
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
    updateStatus("Simulation running");
    // Additional logic to start/resume simulation
}

function pauseSimulation() {
    updateStatus("Simulation paused");
    // Additional logic to pause simulation
}

function resetSimulation() {
    updateStatus("Simulation reset");
    // Additional logic to reset simulation
}
