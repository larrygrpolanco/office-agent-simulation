/**
 * Simulation Controller
 * Handles step-based simulation logic, auto mode, and UI updates
 */

import { CONSTANTS } from './GameConfig.js';

export class SimulationController {
  constructor(webSocketManager, agentManager) {
    this.webSocketManager = webSocketManager;
    this.agentManager = agentManager;
    
    // Simulation state
    this.currentStep = 0;
    this.isProcessing = false;
    this.autoMode = false;
    this.autoModeTimeout = null;
    
    // UI elements
    this.statusMessage = null;
    this.fpsCounter = null;
    this.lastFpsUpdate = 0;
    
    this.setupEventListeners();
    this.setupWebSocketCallbacks();
  }

  setupEventListeners() {
    // Get UI elements
    this.statusMessage = document.getElementById('status-message');
    this.fpsCounter = document.getElementById('fps-counter');

    // Set up simulation button listeners
    document.getElementById('next-step-btn').addEventListener('click', () => this.nextStep());
    document.getElementById('reset-btn').addEventListener('click', () => this.resetSimulation());
    
    // Set up auto mode listeners
    document.getElementById('auto-mode-checkbox').addEventListener('change', () => this.toggleAutoMode());
    document.getElementById('auto-delay').addEventListener('change', () => this.updateAutoDelay());
  }

  setupWebSocketCallbacks() {
    // Handle messages from WebSocket
    this.webSocketManager.onMessage((data) => this.handleStepResponse(data));
    
    // Handle status updates from WebSocket
    this.webSocketManager.onStatusChange((message) => this.updateStatus(message));
  }

  nextStep() {
    if (!this.webSocketManager.isConnected() || this.isProcessing) {
      if (!this.webSocketManager.isConnected()) {
        this.updateStatus('Error: Not connected to server');
      }
      return;
    }

    // Set processing state
    this.setProcessingState(true);
    
    // Get current environment state from agent manager
    const environmentState = this.agentManager.getCurrentEnvironmentState();
    
    // Send step request to backend
    const success = this.webSocketManager.sendStepRequest(this.currentStep + 1, environmentState);
    
    if (success) {
      this.updateStatus(`Processing step ${this.currentStep + 1}...`);
    } else {
      this.setProcessingState(false);
      this.updateStatus('Error: Failed to send step request');
    }
  }

  handleStepResponse(data) {
    // Stop processing indicator
    this.setProcessingState(false);
    
    // Update agents through agent manager
    for (const personaName in data.persona) {
      this.agentManager.updateAgent(personaName, data.persona[personaName]);
    }
    
    // Update step counter
    this.currentStep++;
    document.getElementById('step-counter').textContent = this.currentStep;
    
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
    this.updateStatus(`Step ${this.currentStep} completed`);
    
    // If auto mode is enabled, schedule next step
    if (this.autoMode) {
      const delay = parseInt(document.getElementById('auto-delay').value);
      this.autoModeTimeout = setTimeout(() => {
        if (this.autoMode && !this.isProcessing) {
          this.nextStep();
        }
      }, delay);
    }
  }

  setProcessingState(processing) {
    this.isProcessing = processing;
    
    const nextStepBtn = document.getElementById('next-step-btn');
    const processingIndicator = document.getElementById('processing-indicator');
    
    if (processing) {
      nextStepBtn.disabled = true;
      if (processingIndicator) {
        processingIndicator.classList.add('active');
      }
    } else {
      nextStepBtn.disabled = false;
      if (processingIndicator) {
        processingIndicator.classList.remove('active');
      }
    }
  }

  toggleAutoMode() {
    const checkbox = document.getElementById('auto-mode-checkbox');
    const delaySelect = document.getElementById('auto-delay');
    
    this.autoMode = checkbox.checked;
    delaySelect.disabled = !this.autoMode;
    
    if (this.autoMode) {
      this.updateStatus('Auto mode enabled');
      // Start auto mode if not currently processing
      if (!this.isProcessing && this.webSocketManager.isConnected()) {
        const delay = parseInt(delaySelect.value);
        this.autoModeTimeout = setTimeout(() => {
          if (this.autoMode && !this.isProcessing) {
            this.nextStep();
          }
        }, delay);
      }
    } else {
      this.updateStatus('Auto mode disabled');
      // Clear any pending auto step
      if (this.autoModeTimeout) {
        clearTimeout(this.autoModeTimeout);
        this.autoModeTimeout = null;
      }
    }
  }

  updateAutoDelay() {
    // If auto mode is active and we have a pending timeout, restart it with new delay
    if (this.autoMode && this.autoModeTimeout) {
      clearTimeout(this.autoModeTimeout);
      const delay = parseInt(document.getElementById('auto-delay').value);
      this.autoModeTimeout = setTimeout(() => {
        if (this.autoMode && !this.isProcessing) {
          this.nextStep();
        }
      }, delay);
    }
  }

  resetSimulation() {
    if (this.webSocketManager.isConnected()) {
      // Stop auto mode
      this.autoMode = false;
      document.getElementById('auto-mode-checkbox').checked = false;
      document.getElementById('auto-delay').disabled = true;
      if (this.autoModeTimeout) {
        clearTimeout(this.autoModeTimeout);
        this.autoModeTimeout = null;
      }
      
      // Reset processing state
      this.setProcessingState(false);
      
      // Reset step counter
      this.currentStep = 0;
      document.getElementById('step-counter').textContent = this.currentStep;
      
      // Clear processing time
      document.getElementById('processing-time').textContent = '';
      
      this.updateStatus('Resetting simulation...');
      
      // Send reset request
      const success = this.webSocketManager.sendResetRequest();
      
      if (success) {
        // Reset agents through agent manager
        this.agentManager.resetAgents();
        this.updateStatus('Simulation reset - Ready for next step');
      } else {
        this.updateStatus('Error: Failed to send reset request');
      }
    } else {
      this.updateStatus('Error: Not connected to server');
    }
  }

  updateStatus(message) {
    if (this.statusMessage) {
      this.statusMessage.textContent = message;
    }
  }

  updateFPS(time, actualFps) {
    // Update FPS counter every 500ms
    if (time - this.lastFpsUpdate > CONSTANTS.FPS_UPDATE_INTERVAL) {
      if (this.fpsCounter) {
        this.fpsCounter.textContent = `FPS: ${Math.round(actualFps)}`;
      }
      this.lastFpsUpdate = time;
    }
  }

  getCurrentStep() {
    return this.currentStep;
  }

  isSimulationProcessing() {
    return this.isProcessing;
  }

  isAutoModeEnabled() {
    return this.autoMode;
  }
}
