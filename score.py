import os

# Score.py

SCORES_FILE_NAME = "Scores.txt"

def add_score(difficulty: int) -> None:
    """Add score based on the difficulty level."""
    points_of_winning = (difficulty * 3) + 5
    
    # Try reading the current score
    try:
        with open(SCORES_FILE_NAME, 'r') as f:
            current_score = int(f.read())
    except (FileNotFoundError, ValueError):
        # If the file doesn't exist or has bad content, start with 0 score
        current_score = 0

    # Add new points and update the file
    new_score = current_score + points_of_winning
    with open(SCORES_FILE_NAME, 'w') as f:
        f.write(str(new_score))

    print(f"New score added: {new_score}")
