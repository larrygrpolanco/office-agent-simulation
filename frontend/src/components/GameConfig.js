/**
 * Game Configuration
 * Contains Phaser game configuration and constants
 */

export const GAME_CONFIG = {
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
  scale: {
    mode: Phaser.Scale.RESIZE,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
};

export const CONSTANTS = {
  TILE_WIDTH: 32,
  AGENT_SPEED: 2,
  FPS_UPDATE_INTERVAL: 500,
  CAMERA_SCROLL_SPEED: 8,
  WEBSOCKET_URL: 'ws://localhost:8000/ws',
  RECONNECT_DELAY: 5000,
};

export const TILESET_CONFIG = [
  { name: 'blocks_1', path: 'assets/the_office/visuals/map_assets/blocks_1.png' },
  { name: 'int_Basement_32x32', path: 'assets/the_office/visuals/map_assets/int_Basement_32x32.png' },
  { name: 'int_Bathroom_32x32', path: 'assets/the_office/visuals/map_assets/int_Bathroom_32x32.png' },
  { name: 'int_Classroom_and_library_32x32', path: 'assets/the_office/visuals/map_assets/int_Classroom_and_library_32x32.png' },
  { name: 'int_Generic_32x32', path: 'assets/the_office/visuals/map_assets/int_Generic_32x32.png' },
  { name: 'int_Grocery_store_32x32', path: 'assets/the_office/visuals/map_assets/int_Grocery_store_32x32.png' },
  { name: 'int_Hospital_32x32', path: 'assets/the_office/visuals/map_assets/int_Hospital_32x32.png' },
  { name: 'int_Kitchen_32x32', path: 'assets/the_office/visuals/map_assets/int_Kitchen_32x32.png' },
  { name: 'Modern_Office_32x32', path: 'assets/the_office/visuals/map_assets/Modern_Office_32x32.png' },
  { name: 'Room_Builder_Office_32x32', path: 'assets/the_office/visuals/map_assets/Room_Builder_Office_32x32.png' },
];

export const LAYER_NAMES = [
  'Floor Visuals',
  'Wall Visuals',
  'Furniture Visuals L1',
  'Furniture Visuals L2',
  'Furniture Visuals L3',
  'Furniture Visuals L4',
  'Collision Layer',
];
