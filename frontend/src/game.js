/**
 * Office Agent Simulation - Main Game File (Refactored)
 * 
 * This is the main entry point that orchestrates all game components.
 * The original monolithic file has been broken down into modular components.
 */

import { GAME_CONFIG } from './components/GameConfig.js';
import { WebSocketManager } from './components/WebSocketManager.js';
import { AgentManager } from './components/AgentManager.js';
import { MapManager } from './components/MapManager.js';
import { SimulationController } from './components/SimulationController.js';

// Global game instance
let game;

// Component managers
let webSocketManager;
let agentManager;
let mapManager;
let simulationController;

// Input handling
let cursors;

/**
 * Initialize the game when window loads
 */
window.onload = function () {
  // Create Phaser game with our scene functions
  const gameConfig = {
    ...GAME_CONFIG,
    scene: {
      preload: preload,
      create: create,
      update: update,
    },
  };

  game = new Phaser.Game(gameConfig);
};

/**
 * Preload game assets
 */
function preload() {
  // Initialize map manager and preload assets
  mapManager = new MapManager(this);
  mapManager.preloadAssets();

  // Show loading message
  updateStatus('Loading assets...');
}

/**
 * Create game objects and initialize systems
 */
function create() {
  // Initialize agent manager
  agentManager = new AgentManager(this);

  // Initialize WebSocket manager
  webSocketManager = new WebSocketManager();

  // Initialize simulation controller
  simulationController = new SimulationController(webSocketManager, agentManager);

  // Create the map
  const mapLoaded = mapManager.createMap();
  
  if (mapLoaded) {
    updateStatus('Map loaded successfully');
  } else {
    updateStatus('Error loading map');
    return;
  }

  // Set up keyboard input
  cursors = this.input.keyboard.createCursorKeys();

  // Connect to WebSocket server
  webSocketManager.connect();

  // Show ready message
  updateStatus('Ready to start simulation');
}

/**
 * Update game state every frame
 */
function update(time, delta) {
  // Update FPS counter
  simulationController.updateFPS(time, game.loop.actualFps);

  // Update agent movement
  agentManager.updateMovement();

  // Handle camera movement with arrow keys
  mapManager.handleCameraMovement(cursors);
}

/**
 * Update status message (utility function for backwards compatibility)
 */
function updateStatus(message) {
  const statusElement = document.getElementById('status-message');
  if (statusElement) {
    statusElement.textContent = message;
  }
}

// Export for debugging purposes
window.gameDebug = {
  webSocketManager,
  agentManager,
  mapManager,
  simulationController,
  game
};
