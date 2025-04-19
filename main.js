/**
 * Office Agent Simulation - Electron Main Process
 * 
 * This is the entry point for the Electron application that packages
 * the Office Agent Simulation for desktop use.
 */

const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Global references
let mainWindow;
let pythonProcess;

// Create the main window
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1500,
        height: 900,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        title: 'Office Agent Simulation',
        icon: path.join(__dirname, 'frontend/assets/visuals/icon.png')
    });
    
    // Load the frontend
    mainWindow.loadURL('http://localhost:8000/static/');
    
    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }
    
    // Handle window close
    mainWindow.on('closed', function() {
        mainWindow = null;
        
        // Kill the Python backend process
        if (pythonProcess) {
            pythonProcess.kill();
            pythonProcess = null;
        }
    });
}

// Start the Python backend
function startBackend() {
    // Check if Python is installed
    const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
    
    // Path to the backend app.py
    const backendPath = path.join(__dirname, 'backend', 'app.py');
    
    // Ensure the backend file exists
    if (!fs.existsSync(backendPath)) {
        console.error(`Backend file not found: ${backendPath}`);
        app.quit();
        return;
    }
    
    // Start the Python process
    pythonProcess = spawn(pythonCommand, [backendPath]);
    
    // Log Python output
    pythonProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
    });
    
    // Log Python errors
    pythonProcess.stderr.on('data', (data) => {
        console.error(`Backend Error: ${data}`);
    });
    
    // Handle Python process exit
    pythonProcess.on('close', (code) => {
        console.log(`Backend process exited with code ${code}`);
        pythonProcess = null;
        
        // If the app is still running, quit it
        if (mainWindow) {
            app.quit();
        }
    });
}

// App ready event
app.on('ready', () => {
    // Start the backend
    startBackend();
    
    // Wait a moment for the backend to start
    setTimeout(() => {
        createWindow();
    }, 1000);
});

// Quit when all windows are closed
app.on('window-all-closed', () => {
    // On macOS, applications keep running until explicitly quit
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Activate event (macOS)
app.on('activate', () => {
    // Re-create window on dock icon click (macOS)
    if (mainWindow === null) {
        createWindow();
    }
});

// Handle app quit
app.on('quit', () => {
    // Kill the Python backend process
    if (pythonProcess) {
        pythonProcess.kill();
        pythonProcess = null;
    }
});
