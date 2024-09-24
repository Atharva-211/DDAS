const { ipcRenderer } = require('electron');
const axios = require('axios'); // Ensure axios is imported

function displayDuplicates(duplicates) {
    const tableBody = document.querySelector('#duplicatesTable tbody');
    tableBody.innerHTML = ''; // Clear previous entries

    if (!Array.isArray(duplicates) || duplicates.length === 0) {
        const noDuplicatesRow = document.createElement('tr');
        noDuplicatesRow.innerHTML = '<td colspan="3">No duplicates found.</td>';
        tableBody.appendChild(noDuplicatesRow);
        return;
    }

    duplicates.forEach(duplicate => {
        // Only take the first filename and location for display
        const filename = duplicate.filenames[0]; // Only show the first file
        const location = duplicate.locations[0]; // Corresponding location for the first file

        const row = document.createElement('tr');

        // Filename cell
        const filenameCell = document.createElement('td');
        filenameCell.textContent = filename; // Display only the first filename
        row.appendChild(filenameCell);

        // Location cell
        const locationCell = document.createElement('td');
        locationCell.textContent = location; // Display its location
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
}

// Handle folder selection
document.getElementById('selectFolder').addEventListener('click', async () => {
    const folderPath = await ipcRenderer.invoke('dialog:openFolder');

    if (folderPath) {
        document.getElementById('folderPath').innerText = `Selected Folder: ${folderPath}`; // Corrected syntax for template literals
        document.getElementById('uploadFiles').disabled = false;

        // Store the selected folder path
        window.selectedFolderPath = folderPath;
    }
});

// Handle file upload
document.getElementById('uploadFiles').addEventListener('click', async () => {
    const folderPath = window.selectedFolderPath;

    if (!folderPath) {
        document.getElementById('status').innerText = 'Please select a folder first!';
        return;
    }

    document.getElementById('status').innerText = 'Uploading files...';

    try {
        // Send the request with the correct body structure
        const response = await axios.post('http://127.0.0.1:8000/upload-folder', {
            folder_path: folderPath // Send the folder path as a property of an object
        });

        console.log('Response from server:', response.data); // Log the response

        if (response.data.message === 'Folder processed successfully') {
            document.getElementById('status').innerText = 'Files uploaded successfully!';

            // Now call the getDuplicates handler
            const duplicatesResponse = await ipcRenderer.invoke('getDuplicates');
            console.log('Duplicates response:', duplicatesResponse); // Log duplicates response

            if (Array.isArray(duplicatesResponse) && duplicatesResponse.length > 0) {
                displayDuplicates(duplicatesResponse); // Display duplicates if it's an array
            } else {
                document.getElementById('status').innerText = 'No duplicates found.';
            }
        } else {
            document.getElementById('status').innerText = 'Failed to upload files.';
        }
    } catch (error) {
        console.error('Error uploading files:', error);
        document.getElementById('status').innerText = 'Failed to upload files.';
    }
});
