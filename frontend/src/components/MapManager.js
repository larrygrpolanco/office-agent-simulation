/**
 * Map Manager
 * Handles map loading, tileset management, and layer creation
 */

import { TILESET_CONFIG, LAYER_NAMES, CONSTANTS } from './GameConfig.js';

export class MapManager {
  constructor(scene) {
    this.scene = scene;
    this.map = null;
    this.layers = {};
    this.tilesets = [];
  }

  preloadAssets() {
    // Load the Tiled map (JSON export)
    this.scene.load.tilemapTiledJSON(
      'officeMap',
      'assets/the_office/visuals/the_office.json'
    );

    // Load all tileset images
    TILESET_CONFIG.forEach(tileset => {
      this.scene.load.image(tileset.name, tileset.path);
    });

    // Load placeholder agent sprite
    this.scene.load.image('agent', 'assets/the_office/visuals/placeholder-agent.png');
  }

  createMap() {
    try {
      // Create the tilemap
      this.map = this.scene.make.tilemap({ key: 'officeMap' });

      // Debug: Log the map object to inspect tileset and layer names
      console.log('Phaser Tilemap object:', this.map);
      console.log('Tilesets:', this.map.tilesets.map((ts) => ts.name));
      console.log('Layers:', this.map.layers.map((layer) => layer.name));

      // Add tilesets
      this.addTilesets();

      // Create layers
      this.createLayers();

      // Set up camera bounds
      this.setupCamera();

      return true;
    } catch (error) {
      console.error('Error loading map:', error);
      this.logMapDebugInfo();
      return false;
    }
  }

  addTilesets() {
    this.tilesets = [];

    TILESET_CONFIG.forEach(config => {
      try {
        const tileset = this.tryAddTileset(config.name, config.name);
        if (tileset) {
          this.tilesets.push(tileset);
        }
      } catch (error) {
        console.warn(`Failed to add tileset ${config.name}:`, error);
      }
    });

    console.log('Tilesets added successfully');
  }

  tryAddTileset(tilesetName, imageKey) {
    try {
      // First try the standard way
      return this.map.addTilesetImage(tilesetName, imageKey);
    } catch (e) {
      console.warn(
        `Failed to add tileset ${tilesetName} with key ${imageKey}. Trying alternatives...`
      );

      // Try with just the filename (no path)
      const tilesetData = this.map.tilesets.find((ts) => ts.name === tilesetName);
      if (tilesetData && tilesetData.image) {
        const imagePath = tilesetData.image;
        const filename = imagePath.split('/').pop().split('\\').pop();
        const filenameWithoutExt = filename.split('.')[0];

        console.log(`Trying with filename: ${filenameWithoutExt}`);
        try {
          return this.map.addTilesetImage(tilesetName, filenameWithoutExt);
        } catch (e2) {
          // Last resort: try with the tileset name itself
          console.log(`Trying with tileset name itself: ${tilesetName}`);
          return this.map.addTilesetImage(tilesetName);
        }
      }
      throw e; // Re-throw if we couldn't find alternatives
    }
  }

  createLayers() {
    // Create map layers (layer names must match those in Tiled)
    this.layers.floorLayer = this.map.createLayer('Floor Visuals', this.tilesets, 0, 0);
    this.layers.wallLayer = this.map.createLayer('Wall Visuals', this.tilesets, 0, 0);

    // Create furniture layers
    this.layers.furnitureLayer1 = this.map.createLayer('Furniture Visuals L1', this.tilesets, 0, 0);
    this.layers.furnitureLayer2 = this.map.createLayer('Furniture Visuals L2', this.tilesets, 0, 0);
    this.layers.furnitureLayer3 = this.map.createLayer('Furniture Visuals L3', this.tilesets, 0, 0);
    this.layers.furnitureLayer4 = this.map.createLayer('Furniture Visuals L4', this.tilesets, 0, 0);

    // Create collision layer (hidden by default)
    this.layers.collisionLayer = this.map.createLayer('Collision Layer', this.tilesets, 0, 0);
    this.layers.collisionLayer.setVisible(false);
  }

  setupCamera() {
    if (this.map) {
      this.scene.cameras.main.setBounds(0, 0, this.map.widthInPixels, this.map.heightInPixels);
      this.scene.cameras.main.setZoom(1);
    }
  }

  handleCameraMovement(cursors) {
    if (cursors.left.isDown) {
      this.scene.cameras.main.scrollX -= CONSTANTS.CAMERA_SCROLL_SPEED;
    } else if (cursors.right.isDown) {
      this.scene.cameras.main.scrollX += CONSTANTS.CAMERA_SCROLL_SPEED;
    }

    if (cursors.up.isDown) {
      this.scene.cameras.main.scrollY -= CONSTANTS.CAMERA_SCROLL_SPEED;
    } else if (cursors.down.isDown) {
      this.scene.cameras.main.scrollY += CONSTANTS.CAMERA_SCROLL_SPEED;
    }
  }

  logMapDebugInfo() {
    if (this.map) {
      console.log('Tileset names in map:', this.map.tilesets.map((ts) => ts.name));
      console.log('Image sources in map:', this.map.tilesets.map((ts) => ts.image));
      console.log('Layer names in map:', this.map.layers.map((layer) => layer.name));
    }
  }

  getMapDimensions() {
    if (this.map) {
      return {
        width: this.map.widthInPixels,
        height: this.map.heightInPixels,
        tileWidth: this.map.tileWidth,
        tileHeight: this.map.tileHeight
      };
    }
    return null;
  }

  toggleCollisionLayer() {
    if (this.layers.collisionLayer) {
      this.layers.collisionLayer.setVisible(!this.layers.collisionLayer.visible);
    }
  }
}
