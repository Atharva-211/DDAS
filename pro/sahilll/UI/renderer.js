const { ipcRenderer } = require('electron');

document.getElementById('selectFolder').addEventListener('click', async () => {
    const folderPath = await ipcRenderer.invoke('dialog:openFolder');
    
    if (folderPath) {
        document.getElementById('folderPath').innerText = `Selected Folder: ${folderPath}`;
        document.getElementById('uploadFiles').disabled = false;

        // Store the selected folder path
        window.selectedFolderPath = folderPath;
    }
});

document.getElementById('uploadFiles').addEventListener('click', async () => {
    const folderPath = window.selectedFolderPath;

    if (!folderPath) {
        document.getElementById('status').innerText = 'Please select a folder first!';
        return;
    }

    document.getElementById('status').innerText = 'Uploading files...';
    
    const response = await ipcRenderer.invoke('uploadFiles', folderPath);

    if (response.status === 'success') {
        document.getElementById('status').innerText = 'Files uploaded successfully!';
    } else {
        document.getElementById('status').innerText = 'Failed to upload files.';
    }
});
