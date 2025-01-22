document.addEventListener('DOMContentLoaded', () => {
    // HTML items
    const iframe = document.getElementById("board-iframe");
    const refreshIndicator = document.getElementById('refresh-indicator');

    let screens = [];
    let currentScreenIndex = 0;
    let initialVersion = null;
    let countdown = REFRESH_DURATION; // Use the dynamic variable

    async function fetchScreens() {
        try {
            const response = await fetch("/api/screens");
            const data = await response.json();

            // Check for server version change
            if (initialVersion === null) {
                initialVersion = data.version;
            } else if (initialVersion !== data.version) {
                console.log("Server version changed, reloading...");
                refreshIndicator.innerText = "Version change! Reloading...";
                window.location.reload();
            }

            screens = data.screens;
        } catch (error) {
            console.error("Failed to fetch screens:", error);
            refreshIndicator.innerText = "Error: Failed to fetch screens.";
        }
    }

    function cycleScreens() {
        if (screens.length > 0) {
            currentScreenIndex = (currentScreenIndex + 1) % screens.length;
            iframe.src = screens[currentScreenIndex];
        }
    }

    function updateCountdown() {
        refreshIndicator.innerText = `Changing in ${countdown}s`;
        if (countdown <= 0) {
            countdown = REFRESH_DURATION; // Reset countdown
            fetchScreens(); // Fetch screens and check for updates
            cycleScreens(); // Cycle to the next screen
        } else {
            countdown -= 1;
        }
    }

    // Initial fetch and start cycling
    fetchScreens().then(() => {
        setInterval(updateCountdown, 1000); // Update countdown every second
    });
});
