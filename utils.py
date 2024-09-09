import os

# Utils.py

# Constants
SCORES_FILE_NAME = "Scores.txt"
BAD_RETURN_CODE = -1

# Screen cleaner function
def screen_cleaner():
    """Clear the screen for a new game."""
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS or Linux
    else:
        os.system('clear')
