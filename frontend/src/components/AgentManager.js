/**
 * Agent Manager
 * Handles agent creation, movement, and visual updates
 */

import { CONSTANTS } from './GameConfig.js';

export class AgentManager {
  constructor(scene) {
    this.scene = scene;
    this.personas = {};
    this.pronunciatios = {};
    this.movementTargets = {};
  }

  createAgent(personaName, x, y) {
    console.log(`Creating new agent: ${personaName}`);
    
    // Create agent sprite
    const pixelX = x * CONSTANTS.TILE_WIDTH;
    const pixelY = y * CONSTANTS.TILE_WIDTH;
    
    this.personas[personaName] = this.scene.add.sprite(pixelX, pixelY, 'agent');
    
    // Add text for speech bubble/pronunciatio
    const textStyle = { 
      font: '14px Arial', 
      fill: '#ffffff',
      backgroundColor: '#333333',
      padding: { x: 8, y: 4 },
      borderRadius: 4
    };
    
    this.pronunciatios[personaName] = this.scene.add.text(
      pixelX, 
      pixelY - 40, 
      '', 
      textStyle
    );
    
    // Set initial target position
    this.movementTargets[personaName] = [pixelX, pixelY];
  }

  updateAgent(personaName, movementData) {
    // Create agent if it doesn't exist
    if (!(personaName in this.personas)) {
      this.createAgent(
        personaName, 
        movementData.movement[0], 
        movementData.movement[1]
      );
    }
    
    // Set target position
    this.movementTargets[personaName] = [
      movementData.movement[0] * CONSTANTS.TILE_WIDTH,
      movementData.movement[1] * CONSTANTS.TILE_WIDTH,
    ];

    // Update speech bubble
    if (movementData.pronunciatio) {
      this.pronunciatios[personaName].setText(movementData.pronunciatio);
    }

    // Update agent info in UI
    this.updateAgentInfo(personaName, movementData.description);
  }

  updateAgentInfo(personaName, description) {
    const agentElement = document.getElementById(
      `agent-${personaName.split(' ')[0]}`
    );
    
    if (agentElement && description) {
      const taskElement = agentElement.querySelector('.agent-task');
      const locationElement = agentElement.querySelector('.agent-location');

      // Extract task and location from description
      // Format: "task @ location"
      const parts = description.split(' @ ');
      if (parts.length === 2) {
        if (taskElement) taskElement.textContent = parts[0];
        if (locationElement) locationElement.textContent = parts[1];
      }
    }
  }

  updateMovement() {
    // Move agents towards their targets
    for (const personaName in this.personas) {
      const persona = this.personas[personaName];
      const pronunciatio = this.pronunciatios[personaName];

      if (this.movementTargets[personaName]) {
        // Calculate direction
        const targetX = this.movementTargets[personaName][0];
        const targetY = this.movementTargets[personaName][1];

        // Move towards target
        if (Math.abs(persona.x - targetX) > CONSTANTS.AGENT_SPEED) {
          if (persona.x < targetX) {
            persona.x += CONSTANTS.AGENT_SPEED;
          } else {
            persona.x -= CONSTANTS.AGENT_SPEED;
          }
        }

        if (Math.abs(persona.y - targetY) > CONSTANTS.AGENT_SPEED) {
          if (persona.y < targetY) {
            persona.y += CONSTANTS.AGENT_SPEED;
          } else {
            persona.y -= CONSTANTS.AGENT_SPEED;
          }
        }

        // Update speech bubble position
        pronunciatio.x = persona.x;
        pronunciatio.y = persona.y - 40;
      }
    }
  }

  getCurrentEnvironmentState() {
    const envData = {};

    // Add each agent's position
    for (const personaName in this.personas) {
      const persona = this.personas[personaName];
      envData[personaName] = {
        x: Math.ceil(persona.x / CONSTANTS.TILE_WIDTH),
        y: Math.ceil(persona.y / CONSTANTS.TILE_WIDTH),
      };
    }

    return envData;
  }

  resetAgents() {
    // Destroy all existing agents
    Object.values(this.personas).forEach((agent) => agent.destroy());
    Object.values(this.pronunciatios).forEach((text) => text.destroy());
    
    // Clear references
    this.personas = {};
    this.pronunciatios = {};
    this.movementTargets = {};
  }

  getAgentCount() {
    return Object.keys(this.personas).length;
  }
}
