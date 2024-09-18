const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');

// FastAPI endpoint
const UPLOAD_URL = 'http://127.0.0.1:8000/upload';

function createWindow() {
    const win = new BrowserWindow({
        // width: 1000,
        // height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'renderer.js'),
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    win.maximize();
    win.loadFile('pages/index.html');
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// Handle folder selection from renderer process
ipcMain.handle('dialog:openFolder', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({ properties: ['openDirectory'] });
    if (!canceled && filePaths.length > 0) {
        return filePaths[0];
    }
    return null;
});

// Handle file upload
ipcMain.handle('uploadFiles', async (event, folderPath) => {
    try {
        const files = fs.readdirSync(folderPath);

        for (const file of files) {
            const filePath = path.join(folderPath, file);
            
            // Read the file into a Buffer
            const fileBuffer = fs.readFileSync(filePath);

            // Create FormData and append the file
            const formData = new FormData();
            formData.append('file', fileBuffer, path.basename(filePath));

            // Send POST request to the FastAPI endpoint
            const response = await axios.post(UPLOAD_URL, formData, {
                headers: {
                    ...formData.getHeaders(),
                },
            });

            console.log(`Uploaded ${file}:`, response.data);
        }

        return { status: 'success', message: 'Files uploaded successfully' };
    } catch (error) {
        console.error('Error uploading files:', error);
        return { status: 'error', message: 'Failed to upload files' };
    }
});
