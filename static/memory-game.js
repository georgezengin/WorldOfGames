// Function to handle hiding and showing elements in the memory game
// document.addEventListener("DOMContentLoaded", function() {
//     // Get the difficulty value from the page
//     const difficulty = parseInt(document.getElementById("difficulty").value, 10);
//     console.log('Difficulty:', difficulty);
//     // Calculate the wait time in milliseconds (e.g., 1000ms per difficulty level)
//     const waitTime = difficulty * 700;
//     console.log('Wait time:', waitTime);

//     // Set a timeout to hide the element after the wait time
//     setTimeout(function() {
//         document.getElementById("sequenceDiv").style.display = "none";
//         // Give focus to the input field with id 'user-sequence'
//         document.getElementById("user_sequence").focus();
//     }, waitTime);
// });


document.addEventListener("DOMContentLoaded", function() {
    const sequenceButton    = document.getElementById("sequenceButton");
    const sequenceField     = document.getElementById('sequence');
    const userSequenceField = document.getElementById("user-sequence");
    const difficultyField   = document.getElementById("difficulty");
    const difficulty = parseInt(difficultyField.value, 10);
    const baseTime = 700; // Base time in milliseconds
    
    // Calculate the wait time using natural logarithm scaling
    // Adding 1 to avoid log(0) and ensure that the result is scaled correctly
    const logScaleFactor = 1.5; // Factor to adjust the scaling, adjust as needed
    const factor = Math.log(difficulty + 1) * logScaleFactor;
    console.log('Factor:', factor);
    const waitTime = baseTime * difficulty * factor;
    
    // const logBase = 2; // Base for the logarithmic scaling, adjust as needed
    // const waitTime = baseTime * Math.log(difficulty + 1) / Math.log(logBase);
    const oldWaitTime = baseTime * difficulty;
    console.log('Difficulty:', difficulty, 'Old wait time:', oldWaitTime, 'New wait time:', waitTime);
    
    //sequenceButton.addEventListener("click", function() {
        // Set the button text to the sequence
        const sequence = sequenceField.value;
        console.log('Sequence:', sequence);
        sequenceButton.textContent = sequence;
        sequenceButton.disabled = true; 

        // Hide the button and enable the user sequence field after the wait time
        setTimeout(function() {
            sequenceButton.style.display = "none";
            userSequenceField.disabled = false;
            userSequenceField.focus(); // Focus on the user sequence field
        }, waitTime);
    //});
});
