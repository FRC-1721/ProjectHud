document.addEventListener('DOMContentLoaded', () => {
    // Refresh interval (in milliseconds)
    const REFRESH_INTERVAL = 10000; // 10 seconds
    let timeLeft = REFRESH_INTERVAL / 1000; // Countdown in seconds

    // Countdown Timer
    const refreshIndicator = document.getElementById('refresh-indicator');
    const countdownTimer = setInterval(() => {
        timeLeft -= 1;
        if (timeLeft >= 0) {
            refreshIndicator.innerText = `Refresh in ${timeLeft}s`;
        }
    }, 1000);

    // Auto-refresh every 10 seconds
    setInterval(() => {
        fetch(window.location.href, { method: 'HEAD' })
            .then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.warn('Server not responding, will retry in 10 seconds');
                    refreshIndicator.innerText = 'Server down. Retrying...';
                    timeLeft = REFRESH_INTERVAL / 1000; // Reset countdown
                }
            })
            .catch(error => {
                console.error('Fetch failed, server might be down:', error);
                refreshIndicator.innerText = 'Server down. Retrying...';
                timeLeft = REFRESH_INTERVAL / 1000; // Reset countdown
            });
    }, REFRESH_INTERVAL);

    // Retry logic for server downtime
    function checkServerStatus() {
        fetch(window.location.href, { method: 'HEAD' })
            .then(response => {
                if (response.ok) {
                    console.log('Server is back online, refreshing page...');
                    window.location.reload();
                } else {
                    console.warn('Server still down, retrying in 10 seconds');
                    refreshIndicator.innerText = 'Reconnecting...';
                    setTimeout(checkServerStatus, 10000);
                }
            })
            .catch(error => {
                console.error('Failed to reach server:', error);
                refreshIndicator.innerText = 'Reconnecting...';
                setTimeout(checkServerStatus, 10000);
            });
    }

    // Initial check if the page fails to load
    window.addEventListener('error', (event) => {
        console.error('Critical error detected:', event);
        console.warn('Starting server status checks...');
        refreshIndicator.innerText = 'Reconnecting...';
        checkServerStatus();
    });
});
