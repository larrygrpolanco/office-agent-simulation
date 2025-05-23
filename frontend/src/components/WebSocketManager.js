/**
 * WebSocket Manager
 * Handles all WebSocket communication with the backend
 */

import { CONSTANTS } from './GameConfig.js';

export class WebSocketManager {
  constructor() {
    this.socket = null;
    this.connected = false;
    this.onMessageCallback = null;
    this.onStatusChangeCallback = null;
  }

  connect() {
    // Close existing connection if any
    if (this.socket) {
      this.socket.close();
    }

    // Create new WebSocket connection
    this.socket = new WebSocket(CONSTANTS.WEBSOCKET_URL);

    // Connection opened
    this.socket.onopen = (event) => {
      this.connected = true;
      this.updateStatus('Connected to server - Ready for simulation');
    };

    // Connection closed
    this.socket.onclose = (event) => {
      this.connected = false;
      this.updateStatus('Disconnected from server');

      // Try to reconnect after delay
      setTimeout(() => this.connect(), CONSTANTS.RECONNECT_DELAY);
    };

    // Connection error
    this.socket.onerror = (error) => {
      this.connected = false;
      this.updateStatus('WebSocket error');
      console.error('WebSocket error:', error);
    };

    // Message received
    this.socket.onmessage = (event) => {
      this.handleMessage(event);
    };
  }

  handleMessage(event) {
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
        if (this.onMessageCallback) {
          this.onMessageCallback(data);
        }
      } else {
        console.warn('Received unexpected JSON format:', data);
      }
    } catch (e) {
      console.error('Failed to parse server message:', e);
      console.log('Raw server response:', event.data);
      console.log('Full error stack:', e.stack);
    }
  }

  sendMessage(message) {
    if (this.connected && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
      return true;
    }
    return false;
  }

  sendStepRequest(stepId, environmentState) {
    const stepRequest = {
      action: 'next_step',
      step_id: stepId,
      environment: environmentState
    };
    
    return this.sendMessage(stepRequest);
  }

  sendResetRequest() {
    return this.sendMessage({ action: 'reset' });
  }

  onMessage(callback) {
    this.onMessageCallback = callback;
  }

  onStatusChange(callback) {
    this.onStatusChangeCallback = callback;
  }

  updateStatus(message) {
    if (this.onStatusChangeCallback) {
      this.onStatusChangeCallback(message);
    }
  }

  isConnected() {
    return this.connected;
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
    this.connected = false;
  }
}
