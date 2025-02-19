// Load current preferences from storage
chrome.storage.local.get(['toxicityThreshold', 'enableBlur', 'blurIntensity'], (result) => {
    const sensitivitySelect = document.getElementById('sensitivity');
    const blurToggle = document.getElementById('enableBlur');
    const blurIntensitySlider = document.getElementById('blurIntensity');

    // Set saved values or defaults
    sensitivitySelect.value = result.toxicityThreshold || 'medium';
    blurToggle.checked = result.enableBlur !== undefined ? result.enableBlur : true;
    blurIntensitySlider.value = result.blurIntensity || 10; // Default to medium blur
});

// Save the selected preferences when the user changes them
document.getElementById('savePreferences').addEventListener('click', () => {
    const selectedThreshold = document.getElementById('sensitivity').value;
    const enableBlur = document.getElementById('enableBlur').checked;
    const blurIntensity = document.getElementById('blurIntensity').value;

    // Save preferences to chrome storage
    chrome.storage.local.set({ 
        toxicityThreshold: selectedThreshold,
        enableBlur: enableBlur,
        blurIntensity: blurIntensity 
    }, () => {
        console.log('Preferences saved!');

        // Reload the active tab
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs.length > 0) {
                chrome.tabs.reload(tabs[0].id);
            }
        });

        // Close the popup after saving
        window.close();
    });
});
