chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed!");
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "getToxicityThreshold") {
        chrome.storage.local.get(["toxicityThreshold"], (data) => {
            if (chrome.runtime.lastError) {
                console.error("Storage error:", chrome.runtime.lastError);
                sendResponse({ threshold: 0.7 }); // Default to medium
            } else {
                sendResponse({ threshold: data.toxicityThreshold || 0.7 });
            }
        });

        return true; // Indicates async response
    }
});
