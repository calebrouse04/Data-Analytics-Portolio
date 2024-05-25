let display;
let milliseconds = 0;
let seconds = 0;
let minutes = 0;
let hours = 0;
let interval = null;

document.addEventListener('DOMContentLoaded', () => {
    display = document.getElementById("display");
    display.textContent = "00:00:00:000";  // Initialize the display text
});

function updateTime() {
    milliseconds += 100;
    if (milliseconds >= 1000) {
        milliseconds = 0;
        seconds++;
    }
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
    }
    if (minutes >= 60) {
        minutes = 0;
        hours++;
    }
    display.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}:${milliseconds.toString().padStart(3, '0')}`;
}

function start() {
    if (!interval) {
        interval = setInterval(updateTime, 100);
    }
}

function stop() {
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
}

function resetStopwatch() {
    stop();
    milliseconds = 0;
    seconds = 0;
    minutes = 0;
    hours = 0;
    display.textContent = "00:00:00:000";  // Also reset display text
}
