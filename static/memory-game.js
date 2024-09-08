// Function to handle hiding and showing elements in the memory game
window.addEventListener('DOMContentLoaded', (event) => {
    const sequenceElement = document.getElementById('sequence');
    const userInputElement = document.getElementById('user_input');

    if (sequenceElement && userInputElement) {
        setTimeout(() => {
            sequenceElement.style.display = 'none';
            userInputElement.style.display = 'block';
        }, 700);  // Hide the sequence after 0.7 seconds
    }
});
