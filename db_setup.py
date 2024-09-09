import sqlite3

def create_database():
    """
    Creates the 'games.db' SQLite database with two tables: 'sessions' and 'top_10_scores'.
    
    The 'sessions' table stores information about each game session, including the user's name, game choice, difficulty level, score, and how many games they've played. The UNIQUE constraint ensures that only one record exists for each combination of user, game choice, and difficulty level.
    
    The 'top_10_scores' table stores the top 10 scores for each game, with the user's name and the score.
    
    This function is called when the application starts, and will create the database if it doesn't already exist.
    """
    with sqlite3.connect('games.db') as conn:
        cursor = conn.cursor()

        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                game_choice TEXT,
                difficulty INTEGER,
                total_score INTEGER DEFAULT 0,
                total_games INTEGER DEFAULT 0,
                last_played DATETIME DEFAULT CURRENT_TIMESTAMP,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, game_choice, difficulty) 
            )
        ''')

        # Create top_10_scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS top_10_scores (
                name TEXT PRIMARY KEY,
                score INTEGER
            )
        ''')

        conn.commit()

def update_session(name: str, game_choice: str, difficulty: int, won: bool, games_played: int) -> None:
    """
    Updates the session table with the user's score and game data.

    If the user won, updates their score in the top_10_scores table.

    :param name: The user's name
    :param game_choice: The game the user chose
    :param difficulty: The difficulty level the user chose
    :param won: Whether the user won or not
    :param games_played: The number of games played
    """
    with sqlite3.connect('games.db') as conn:
        cursor = conn.cursor()

        score = difficulty * 10 if won else -1 *difficulty * 5 # 0
        cursor.execute('''
            INSERT INTO sessions (name, game_choice, difficulty, total_score, total_games, last_played)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(name, game_choice, difficulty) DO UPDATE SET
                last_played = CURRENT_TIMESTAMP,
                total_score = total_score + excluded.total_score,
                total_games = total_games + excluded.total_games
        ''', (name, game_choice, difficulty, score, games_played))

        conn.commit()

    #if won:
    update_score(name)


def update_score(name: str) -> None:
    """
    Updates the user's score in the top_10_scores table.

    If the user is already in the table, updates their score.
    If the user is not in the table, inserts their score.
    Removes the user from the table if they are no longer in the top 10.
    """
    with sqlite3.connect('games.db') as conn:
        cursor = conn.cursor()

        # Calculate the total score for the user
        cursor.execute('SELECT SUM(total_score) FROM sessions WHERE name = ?', (name,))
        total_score = cursor.fetchone()[0] or 0

        # Insert or update the user's score in the top_10_scores table
        cursor.execute('INSERT INTO top_10_scores (name, score) VALUES (?, ?) ON CONFLICT(name) DO UPDATE SET score = excluded.score', (name, total_score))

        # Maintain only the top 10 scores
        cursor.execute('DELETE FROM top_10_scores WHERE name NOT IN (SELECT name FROM top_10_scores ORDER BY score DESC LIMIT 10)')

        conn.commit()

def get_user_score(name: str) -> int:
    """
    Updates the user's score in the top_10_scores table.

    If the user is already in the table, updates their score.
    If the user is not in the table, inserts their score.
    Removes the user from the table if they are no longer in the top 10.
    """
    with sqlite3.connect('games.db') as conn:
        cursor = conn.cursor()

        # Calculate the total score for the user
        cursor.execute('SELECT SUM(total_score) FROM sessions WHERE name = ?', (name,))
        total_score = cursor.fetchone()[0] or 0

    return total_score

if __name__ == '__main__':
    create_database()
