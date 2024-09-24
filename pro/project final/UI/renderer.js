const { ipcRenderer } = require('electron');

// Function to display duplicates in the table
function displayDuplicates(duplicates) {
    const tableBody = document.querySelector('#duplicatesTable tbody');
    tableBody.innerHTML = ''; // Clear previous entries

    duplicates.forEach(duplicate => {
        duplicate.locations.forEach(location => {
            const row = document.createElement('tr');
            
            // Hash cell
            const hashCell = document.createElement('td');
            hashCell.textContent = duplicate.hash;
            row.appendChild(hashCell);

            // Filenames cell
            const filenamesCell = document.createElement('td');
            filenamesCell.textContent = duplicate.filenames.join(', ');
            row.appendChild(filenamesCell);

            // Extension cell
            const extensionCell = document.createElement('td');
            extensionCell.textContent = duplicate.extension;
            row.appendChild(extensionCell);

            // Size cell
            const sizeCell = document.createElement('td');
            sizeCell.textContent = duplicate.size;
            row.appendChild(sizeCell);

            // Location cell
            const locationCell = document.createElement('td');
            locationCell.textContent = location;
            row.appendChild(locationCell);

            // Action cell with delete button
            const actionCell = document.createElement('td');
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', async () => {
                const response = await ipcRenderer.invoke('deleteLocalFile', location);
                if (response.status === 'success') {
                    row.remove(); // Remove the row from the table
                    document.getElementById('status').innerText = 'File deleted successfully!';
                } else {
                    document.getElementById('status').innerText = 'Failed to delete file.';
                }
            });
            actionCell.appendChild(deleteButton);
            row.appendChild(actionCell);

            tableBody.appendChild(row);
        });
    });
}

// Handle file selection
document.getElementById('selectFile').addEventListener('click', async () => {
    const filePath = await ipcRenderer.invoke('dialog:openFile');
    
    if (filePath) {
        document.getElementById('filePath').innerText = `Selected File: ${filePath}`;
        document.getElementById('uploadFile').disabled = false;

        // Store the selected file path
        window.selectedFilePath = filePath;
    }
});

// Handle file upload
document.getElementById('uploadFile').addEventListener('click', async () => {
    const filePath = window.selectedFilePath;

    if (!filePath) {
        document.getElementById('status').innerText = 'Please select a file first!';
        return;
    }

    document.getElementById('status').innerText = 'Uploading file...';
    
    const response = await ipcRenderer.invoke('uploadFile', filePath);

    if (response.status === 'success') {
        document.getElementById('status').innerText = 'File uploaded successfully!';
        // Fetch and display duplicates after upload
        const duplicates = await ipcRenderer.invoke('getDuplicates');
        displayDuplicates(duplicates);
    } else {
        document.getElementById('status').innerText = 'Failed to upload file.';
    }
});
