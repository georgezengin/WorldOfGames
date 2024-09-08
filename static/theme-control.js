// Function to update the displayed user name
function updateUserName(name) {
    console.log("Updating user name:", name);
    userNameElement.textContent = `Welcome ${name}!`;
}

// JavaScript to toggle the theme
function toggleTheme() {
    const themeStyle = document.getElementById('theme-style');
    const themeIcon = document.getElementById('theme-icon');
    const toggleButton = document.getElementById('theme-toggle');
    
    // Get the paths from data attributes
    const lightTheme = toggleButton.getAttribute('data-light-theme');
    const darkTheme = toggleButton.getAttribute('data-dark-theme');
    
    const currentTheme = themeStyle.getAttribute('href');
    // Get the saved theme from localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';

    // Check current theme and toggle
    if (savedTheme === 'light') {
        themeStyle.setAttribute('href', darkTheme);
        themeIcon.textContent = '🌞' // Change to sun icon
        localStorage.setItem('theme', 'dark');
    } else {
        themeStyle.setAttribute('href', lightTheme);
        themeIcon.textContent = '🌙'; // Change to moon icon
        localStorage.setItem('theme', 'light');
    }
    console.log("Theme applied to:", localStorage.getItem('theme'));
}

if (!localStorage.getItem('theme')) {
    localStorage.setItem('theme', 'dark');
}

// Apply the saved theme on page load
document.addEventListener('DOMContentLoaded', () => {
    const themeStyle = document.getElementById('theme-style');
    const themeIcon = document.getElementById('theme-icon');
    const toggleButton = document.getElementById('theme-toggle');

    const lightTheme = toggleButton.getAttribute('data-light-theme');
    const darkTheme = toggleButton.getAttribute('data-dark-theme');

    const savedTheme = localStorage.getItem('theme') || 'dark';
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

    // Apply saved theme or default to system theme
    if (savedTheme === 'light' || (savedTheme === null && systemTheme === 'light')) {
        themeStyle.setAttribute('href', lightTheme);
        themeIcon.textContent = '🌙'; // Change to moon icon
    } else {
        themeStyle.setAttribute('href', darkTheme);
        themeIcon.textContent = '🌞'; // Change to sun icon
    }
    console.log("Document loaded, theme applied to:", savedTheme);
});

const userNameElement = document.getElementById('user-name'); // Element for displaying the user's name
const userName = localStorage.getItem('username') || userNameElement.getAttribute('data-name') || 'Guest';
updateUserName(userName);

// Attach the function to the button's click event
document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
