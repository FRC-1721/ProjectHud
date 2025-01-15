const iframe = document.getElementById("board-iframe");
let screens = [];
let currentScreenIndex = 0;
let initialVersion = null;

async function fetchScreens() {
    try {
        const response = await fetch("/api/screens");
        const data = await response.json();

        // Check for server version change
        if (initialVersion === null) {
            initialVersion = data.version;
        } else if (initialVersion !== data.version) {
            console.log("Server version changed, reloading...");
            window.location.reload();
        }

        screens = data.screens;
    } catch (error) {
        console.error("Failed to fetch screens:", error);
    }
}

function cycleScreens() {
    if (screens.length > 0) {
        currentScreenIndex = (currentScreenIndex + 1) % screens.length;
        iframe.src = screens[currentScreenIndex];
    }
}

// Initial fetch and start cycling
fetchScreens().then(() => {
    setInterval(() => {
        fetchScreens(); // Periodically check for updates
        cycleScreens();
    }, 10000); // Cycle every 10 seconds
});
