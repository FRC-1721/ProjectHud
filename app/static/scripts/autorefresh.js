// Auto-refresh every 80 seconds
setInterval(() => {
    fetch(window.location.href, { method: 'HEAD' })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.warn('Server not responding, will retry in 80 seconds');
            }
        })
        .catch(error => {
            console.error('Fetch failed, server might be down:', error);
        });
}, 80000);

// Retry logic for server downtime
function checkServerStatus() {
    fetch(window.location.href, { method: 'HEAD' })
        .then(response => {
            if (response.ok) {
                console.log('Server is back online, refreshing page...');
                window.location.reload();
            } else {
                console.warn('Server still down, retrying in 80 seconds');
                setTimeout(checkServerStatus, 80000);
            }
        })
        .catch(error => {
            console.error('Failed to reach server:', error);
            setTimeout(checkServerStatus, 80000);
        });
}

// Initial check if the page fails to load
window.addEventListener('error', (event) => {
    console.error('Critical error detected:', event);
    console.warn('Starting server status checks...');
    checkServerStatus();
});
