document.addEventListener('DOMContentLoaded', () => {
    console.log("Document loaded");

    // Select the buttons and stylesheet link
    const lightButton = document.getElementById('light-theme');
    const darkButton = document.getElementById('dark-theme');
    const themeLink = document.getElementById('theme-style');
    const userNameElement = document.getElementById('user-name'); // Element for displaying the user's name
    
    // Ensure elements are present
    if (!lightButton || !darkButton || !themeLink || !userNameElement) {
        console.error("One or more elements are missing.");
        return;
    }

    // Function to apply the selected theme
    function applyTheme(theme) {
        console.log("Applying theme:", theme);

        if (theme === 'light') {
            themeLink.href = '/static/light-theme.css';
        } else if (theme === 'dark') {
            themeLink.href = '/static/dark-theme.css';
        } else {
            console.error("Unknown theme:", theme);
        }

        localStorage.setItem('theme', theme);
    }

    // Function to update the displayed user name
    function updateUserName(name) {
        console.log("Updating user name:", name);
        userNameElement.textContent = `Welcome ${name}!`;
    }

    // Set up theme switcher functionality
    function setupThemeSwitcher() {
        console.log("Setting up theme switcher");

        // Apply the saved theme or default to light
        const savedTheme = localStorage.getItem('theme') || 'light';
        applyTheme(savedTheme);

        // Event listeners for theme buttons
        lightButton.addEventListener('click', () => {
            console.log("Light theme button clicked");
            applyTheme('light');
        });

        darkButton.addEventListener('click', () => {
            console.log("Dark theme button clicked");
            applyTheme('dark');
        });
    }

    // Initialize theme switcher and user name display
    setupThemeSwitcher();

    // Get the user's name from local storage and update the display
    // Get the username from the data attribute and update the display
    const userName = localStorage.getItem('username') || userNameElement.getAttribute('data-name') || 'Guest';
    updateUserName(userName);
});


// document.addEventListener('DOMContentLoaded', () => {
//     console.log("Document loaded");

//     // Select the buttons and stylesheet link
//     const lightButton = document.getElementById('light-theme');
//     const darkButton = document.getElementById('dark-theme');
//     const themeLink = document.getElementById('theme-style');

//     // Ensure elements are present
//     if (!lightButton || !darkButton || !themeLink) {
//         console.error("One or more elements are missing.");
//         return;
//     }

//     // Function to apply the selected theme
//     function applyTheme(theme) {
//         console.log("Applying theme:", theme);

//         if (theme === 'light') {
//             themeLink.href = '/static/light-theme.css';
//         } else if (theme === 'dark') {
//             themeLink.href = '/static/dark-theme.css';
//         } else {
//             console.error("Unknown theme:", theme);
//         }

//         localStorage.setItem('theme', theme);
//     }

//     // Set up theme switcher functionality
//     function setupThemeSwitcher() {
//         console.log("Setting up theme switcher");

//         // Apply the saved theme or default to light
//         const savedTheme = localStorage.getItem('theme') || 'light';
//         applyTheme(savedTheme);

//         // Event listeners for theme buttons
//         lightButton.addEventListener('click', () => {
//             console.log("Light theme button clicked");
//             applyTheme('light');
//         });

//         darkButton.addEventListener('click', () => {
//             console.log("Dark theme button clicked");
//             applyTheme('dark');
//         });
//     }

//     // Initialize theme switcher
//     setupThemeSwitcher();
// });

