const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs'); // Require fs for file operations
const axios = require('axios'); // Assuming you're using axios for network requests

function createWindow() {
    const win = new BrowserWindow({
        webPreferences: {
            nodeIntegration: true, // Allows you to use Node.js in your renderer process
            contextIsolation: false, // Disable context isolation
        },
    });

    win.maximize();
    win.loadFile('pages/revenue.html'); // Load your HTML file

    // Handle folder selection dialog
    ipcMain.handle('dialog:openFolder', async () => {
        const result = await dialog.showOpenDialog(win, {
            properties: ['openDirectory'], // Enable directory selection
        });
        return result.filePaths[0]; // Return the first selected folder path
    });

    // Handle file deletion
    ipcMain.handle('deleteLocalFile', async (event, filePath) => {
        console.log(`Attempting to delete file at: ${filePath}`); // Log the file path
        try {
            fs.unlinkSync(filePath); // Synchronously delete the file
            console.log(`File deleted successfully: ${filePath}`);
            return { status: 'success' };
        } catch (error) {
            console.error('Error deleting file:', error);
            return { status: 'error', message: error.message };
        }
    });

    // Handle fetching duplicates (placeholder for your actual logic)
    ipcMain.handle('getDuplicates', async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/folder/duplicates');
            return response.data; // Return duplicates data
        } catch (error) {
            console.error('Error fetching duplicates:', error);
            return []; // Return an empty array on error
        }
    });
}

app.whenReady().then(createWindow);

// Handle window close
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
