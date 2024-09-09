// Function to update the displayed user name
function setTheme() {
    const themeStyle = document.getElementById('theme-style');
    const themeIcon = document.getElementById('theme-icon');
    const toggleButton = document.getElementById('theme-toggle');

    // Get the paths from data attributes
    const lightTheme = toggleButton.getAttribute('data-light-theme');
    const darkTheme = toggleButton.getAttribute('data-dark-theme');

    const theme = localStorage.getItem('theme') //|| window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    if (theme === 'dark') {
        themeStyle.setAttribute('href', darkTheme);
        themeIcon.textContent = '🌞'; // Change to sun icon
        localStorage.setItem('theme', 'dark');
    } else {
        themeStyle.setAttribute('href', lightTheme);
        themeIcon.textContent = '🌙'; // Change to moon icon
        localStorage.setItem('theme', 'light');
    }
    console.log("Theme set to:", theme);
}

// JavaScript to toggle the theme
function toggleTheme() {
    // Get the saved theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    // Check current theme and toggle
    const newTheme = savedTheme === 'light' ? 'dark' : 'light';
    console.log("Toggling theme to:", newTheme, "from:", savedTheme);
    localStorage.setItem('theme', newTheme);
    setTheme();
}

function updateUserName(name) {
    console.log("Updating user name:", name);
    if (!name) name = 'Guest';
    const userNameElement = document.getElementById('user-name');
    if (name && userNameElement) {
        userNameElement.textContent = `Welcome ${name}!`;
    } else {
        if (name) console.error("userNameElement not found.")
    }

//    userNameElement.textContent = `Welcome ${name}!`;
}

function updateUserScore(score) {
    console.log("Updating user score:", score);
    if (!score) score = 0;
    const userScoreElement = document.getElementById('user-score');
    if (userScoreElement) {
        userScoreElement.textContent = `Score: ${score} points`;
    } else {
        if (score) console.error("userScoreElement not found.")
    }
}

if (!localStorage.getItem('theme')) {
    localStorage.setItem('theme', window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
}

// Apply the saved theme on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    if (!savedTheme) {
        localStorage.setItem('theme', systemTheme);
    }
    console.log("Saved theme:", savedTheme, "System theme:", systemTheme);
    setTheme();

    // Update the user name and score on the page
    const userNameElement = document.getElementById('user-name');
    const userName = userNameElement ? userNameElement.getAttribute('data-name') : 'Guest';
    updateUserName(userName);
    
    const userScoreElement = document.getElementById('user-score');
    const userScore = userScoreElement ? userScoreElement.getAttribute('data-score') : '0';
    updateUserScore(userScore);
    
    // Attach the function to the button's click event
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
});
