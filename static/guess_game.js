// static/focus.js
document.addEventListener('DOMContentLoaded', function() {
    var guessInput = document.getElementById('guess');

    var target = document.getElementById('secret_number');
    console.log('Target:', target.value);
    var difficultyField = document.getElementById("difficulty");
    var difficulty = parseInt(difficultyField.value, 10);
    console.log('Difficulty:', difficulty);

    if (guessInput) {
        guessInput.focus();
    }
});
