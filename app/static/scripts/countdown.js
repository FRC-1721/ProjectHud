document.addEventListener("DOMContentLoaded", () => {
    const countdownElement = document.getElementById("countdown");
    const targetTime = parseInt(countdownElement.dataset.targetTime) * 1000; // Convert to milliseconds

    function updateCountdown() {
        const now = Date.now();
        let timeLeft = targetTime - now;

        if (timeLeft < 0) {
            countdownElement.innerText = "000:00:00:00.00";
            return;
        }

        let days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        let hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        let tenths = Math.floor((timeLeft % 1000) / 10); // Extract tenths & hundredths

        let countdownString = `${days.toString().padStart(3, '0')}:` +
            `${hours.toString().padStart(2, '0')}:` +
            `${minutes.toString().padStart(2, '0')}:` +
            `${seconds.toString().padStart(2, '0')}.` +
            `${tenths.toString().padStart(2, '0')}`; // Show two-digit tenths & hundredths

        countdownElement.innerText = countdownString;
    }

    setInterval(updateCountdown, 10); // Update every 10ms
    updateCountdown();
});
