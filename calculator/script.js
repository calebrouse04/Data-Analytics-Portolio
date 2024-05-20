document.addEventListener("DOMContentLoaded", () => {
    const display = document.getElementById('display');

    window.add = function(btn) {
        display.value += btn;
    }

    window.clearDisplay = function() {
        display.value = '';
    }

    window.evaluateDisplay = function() {
        try {
            display.value = eval(display.value);
        } catch (error) {
            console.error('Error:', error);
            display.value = 'Error';
        }
    }

    console.log("working");
});
