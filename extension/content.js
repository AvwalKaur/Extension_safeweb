async function analyzeText(text) {
    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text }),
        });

        const data = await response.json();
        return data.toxicity_score;
    } catch (error) {
        console.error("Error analyzing text:", error);
        return 0; // Assume non-toxic if API fails
    }
}

async function getPreferences() {
    return new Promise((resolve) => {
        chrome.storage.local.get(['toxicityThreshold', 'enableBlur', 'blurIntensity'], (result) => {
            resolve({
                toxicityThreshold: result.toxicityThreshold || 'medium',
                enableBlur: result.enableBlur !== undefined ? result.enableBlur : true,
                blurIntensity: result.blurIntensity || 10
            });
        });
    });
}

const sensitivityLevels = {
    low: 0.9,
    medium: 0.7,
    high: 0.5
};

(async function () {
    const preferences = await getPreferences();
    const toxicityThreshold = sensitivityLevels[preferences.toxicityThreshold] || 0.7;
    const enableBlur = preferences.enableBlur;
    const blurIntensity = preferences.blurIntensity;

    // Scan and blur toxic content
    document.querySelectorAll("p").forEach(async (element) => {
        const text = element.innerText;
        const toxicity = await analyzeText(text);

        if (toxicity >= toxicityThreshold) {
            if (enableBlur) {
                element.style.filter = `blur(${blurIntensity}px)`;
            }
            element.title = "⚠️ Warning: Content hidden due to toxicity!";
        }
    });
})();
