document.addEventListener('DOMContentLoaded', function () {
    const gameOptions = document.querySelectorAll('.game-option');
    const gameChoiceInput = document.getElementById('game_choice');
    const difficultyInput = document.getElementById('difficulty');
    const playButton = document.getElementById('play-button');

    function updatePlayButtonState(game, difficulty) {
        // Check if both game choice and difficulty are set
        if (game && difficulty) {
            playButton.disabled = false;
        } else {
            playButton.disabled = true;
        }
    }

    gameOptions.forEach(option => {
        option.addEventListener('click', function () {
            // Remove selection from other images
            gameOptions.forEach(opt => opt.classList.remove('selected-game'));

            // Add the selected class to the clicked image
            option.classList.add('selected-game');

            // Set the hidden input value to the selected game's data attribute
            gameChoiceInput.value = option.getAttribute('data-game');

            // Update the button state
            updatePlayButtonState(gameChoiceInput.value, difficultyInput.value);
            console.log('Selected game:', gameChoiceInput.value, 'difficulty:', difficultyInput.value);
        });
    });
    
    
    document.querySelectorAll('.difficulty-option').forEach(option => {
        option.addEventListener('click', () => {
            document.querySelectorAll('.difficulty-option').forEach(opt => opt.classList.remove('selected'));
            option.classList.add('selected');
            
            // Set the value in a hidden input or use another method to handle the selection
            document.querySelector('input[name="difficulty"]').value = option.getAttribute('data-difficulty');
            // Update the button state
            updatePlayButtonState(gameChoiceInput.value, difficultyInput.value);
            console.log('Selected difficulty:', document.querySelector('input[name="difficulty"]').value);
        });
    });
});
