let downloadedUrls = [];

// Load previously downloaded URLs from storage
chrome.storage.local.get(["downloadedUrls"], function (result) {
  if (result.downloadedUrls) {
    downloadedUrls = result.downloadedUrls;
  }
});

function openPopup(downloadId) {
  chrome.windows.create({
    url: "popup.html",
    type: "popup",
    width: 400,
    height: 300
  }, (newWindow) => {
    const tabId = newWindow.tabs[0].id;
    
    // Instead of immediately sending the message, we wait for the popup to request it
    chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
      if (message.action === 'requestDownloadId') {
        chrome.tabs.sendMessage(tabId, { downloadId: downloadId });
      }
    });
  });
}



// Listen for new downloads
chrome.downloads.onCreated.addListener(function (downloadItem) {
  const downloadUrl = downloadItem.url;

  // Check if the URL has already been downloaded
  if (downloadedUrls.includes(downloadUrl)) {
    console.log("Duplicate download detected for URL:", downloadUrl); // Debugging

    // Pause the download
    chrome.downloads.pause(downloadItem.id);

    // Open the pop-up window
    openPopup(downloadItem.id);
  } else {
    // If it's a new download, store the URL
    downloadedUrls.push(downloadUrl);

    // Update the local storage with the newly downloaded URL
    chrome.storage.local.set({ "downloadedUrls": downloadedUrls });
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  const { action, downloadId } = message;

  if (action === 'resume') {
    chrome.downloads.resume(downloadId, () => {
      if (chrome.runtime.lastError) {
        console.error("Error resuming download:", chrome.runtime.lastError.message);
      } else {
        console.log("Download resumed:", downloadId);
      }
    });
  } else if (action === 'cancel') {
    // Ensure the cancel action is handled correctly
    chrome.downloads.cancel(downloadId, () => {
      if (chrome.runtime.lastError) {
        console.error("Error cancelling download:", chrome.runtime.lastError.message);
      } else {
        console.log("Download cancelled:", downloadId);
      }
    });
  }
});


