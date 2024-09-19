document.addEventListener('DOMContentLoaded', function () {
  // Request download ID from the background script
  chrome.runtime.sendMessage({ action: 'requestDownloadId' });

  // Listen for the download ID from the background script
  chrome.runtime.onMessage.addListener(function (message) {
    const downloadId = message.downloadId;
    if (downloadId) {
      // Attach event listener for the "Download Again" button
      document.getElementById('resume-btn').addEventListener('click', () => {
        chrome.runtime.sendMessage({ action: 'resume', downloadId: downloadId });
        window.close();
      });

      // Attach event listener for the "Cancel Download" button
      document.getElementById('cancel-btn').addEventListener('click', () => {
        chrome.runtime.sendMessage({ action: 'cancel', downloadId: downloadId });
        window.close();
      });
    }
  });
});
