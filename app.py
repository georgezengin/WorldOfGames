from flask import Flask, render_template, request, redirect, url_for, flash, session
#from live import welcome, load_game
from GuessGame import GuessGame
from MemoryGame import MemoryGame
from db_setup import update_session, update_score, get_user_score

def welcome(name):
    return f"Hello {name}! Welcome to the World of Games!\n\n" #\
#           f"Here you can find many cool games to play"

def create_app():
    """
    Creates a Flask application.

    This function creates a Flask application with the appropriate routes and
    functions to handle the World of Games web application.

    The application has the following routes:

    - `/`: The home page, which renders the `index.html` template.
    - `/welcome`: Handles the user's welcome message and redirects them to the game
        selection page.
    - `/handle_game`: Handles the user's game choice and difficulty level, and
        redirects them to the appropriate game page.
    - `/submit_guess`: Submits a guess for the Guess Game, and redirects to a page
        that displays the result of the guess.
    - `/exit_game`: Exits the current game and returns to the game selection screen.

    :return: A Flask application instance.
    """
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        """
        The home page for the World of Games.

        This page just renders the index.html template with no additional data.
        """
        session['name'] = "Guest"  # Store the user's name in the session
        session['score'] = 0  # Initialize score in session for user

        return render_template('index.html')

    @app.route('/welcome', methods=['POST'])
    def welcome_user():
        """
        Handles the user's welcome message and redirects them to the game selection page.

        If the user does not enter a name, they are flashed an error message and redirected to the home page.

        If the user enters a valid name, they are redirected to the game selection page with a welcome message.

        :param name: The user's name.
        :return: A redirect to the game selection page, or a redirect to the home page with an error message.
        """
        name = request.form.get('name')
        if not name:
            flash('Name is required!', 'error')
            return redirect(url_for('index'))

        session['name'] = name  # Store the user's name in the session
        session['game_choice'] = None  # Initialize game choice in session
        session['difficulty'] = None  # Initialize difficulty in session
        session['guess'] = None  # Initialize guess in session
        session['score'] = get_user_score(name)  # Initialize score in session for user

        message = welcome(name)
        return render_template('game.html', message=message, name=session.get('name'), score=session.get('score'))

    @app.route('/handle_game', methods=['POST'])
    def handle_game():
        """
        Handles the user's game choice and difficulty level, and redirects them to the appropriate game page.

        If the user does not choose a game or does not choose a difficulty level, they are flashed an error message and redirected to the game selection page.

        If the user chooses an invalid game or difficulty level, they are flashed an error message and redirected to the game selection page.

        If the user chooses a valid game and difficulty level, they are redirected to the appropriate game page with the secret number and other game-specific information.

        :param game_choice: The number of the game chosen by the user.
        :param difficulty: The difficulty level chosen by the user.
        :param name: The player's name.
        :return: A redirect to the game page, or a redirect to the game selection page with an error message.
        """
        game_choice = request.form.get('game_choice')
        difficulty = request.form.get('difficulty')

        if not game_choice and not difficulty:
            return render_template('game.html', message="", name=session.get('name'))

        if not game_choice:
            flash('Game choice is required!', 'error')
            return render_template('game.html', message="Please choose a game.", name=session.get('name'))
        
        if not difficulty:
            flash('Difficulty level is required!', 'error')
            return render_template('game.html', message="Please choose a difficulty level.", name=session.get('name'), score=session.get('score'))

        try:
            difficulty = int(difficulty)
        except ValueError:
            flash('Invalid difficulty level!', 'error')
            return render_template('game.html', message="Please choose a valid difficulty level.", name=session.get('name'), score=session.get('score'))

        session['game_choice'] = game_choice
        session['difficulty'] = difficulty
        session['score'] = get_user_score(session['name'])

        if game_choice == '1':  # Memory Game
            game = MemoryGame(difficulty)
            sequence = game.generate_sequence()
            session['target'] = sequence # save solution to game
            return render_template('memory_game.html', message="Guess the sequence!", sequence=sequence, difficulty=difficulty, name=session.get('name'), score=session.get('score'))#, result='')
#            return render_template('memory_game.html', message="Memory Game is coming soon!", name=name)

        if game_choice == '2':  # GuessGame
            game = GuessGame(difficulty)
            game.generate_number()  # Generate the secret number
            session['target'] = game.secret_number
            return render_template('guess_game.html', message="Guess the number!", top_number=game.top_number, secret_number=game.secret_number, difficulty=difficulty, name=session.get('name'), score=session.get('score'))#, result="")

        # Dummy function for other games
        if game_choice == '3':  # Currency Roulette
            return render_template('currency_roulette.html', message="Currency Roulette is coming soon!", name=session.get('name'), score=session.get('score'))

        flash('Invalid game choice!', 'error')
        return redirect(url_for('index'))

    @app.route('/submit_memory_game', methods=['POST'])
    def submit_memory_game() -> str:
        """
        Handle the sequence submission in the Memory Game.
        :return: Rendered result.html template with the game outcome.
        """
        try:
            difficulty = session.get('difficulty')  # Retrieve the difficulty from the session
            sequenceform = session['target'] #request.form.get('sequence').split(' ')
            sequenceform = [int(num) for num in sequenceform]

            user_input = request.form.get('user-sequence')
            session['guess'] = user_input
            user_sequence = [int(num) for num in user_input.split()] if user_input else []

            if sorted(sequenceform) == sorted(user_sequence):
                result = f"You won! Your guessed the sequence {user_sequence} and it was right!!! Congratulations!!!"
                result_class = "success"  # Class for correct guess
                flash(result, 'success')
                update_session(session['name'], 1, difficulty, True, 1)
            else:
                result = f"You lost! You guessed {user_sequence} but the sequence was {sequenceform}"
                result_class = "error"  # Class for incorrect guess
                flash(result, 'error')
                update_session(session['name'], 1, difficulty, False, 1)
            session['score'] = get_user_score(session['name'])

            game = MemoryGame(difficulty)
            game.generate_sequence()
            sequence = game.sequence
            session['target'] = sequence

            return render_template('memory_game.html', message=f"Guess the sequence! [{session['target']}]", sequence=sequence, 
                                   difficulty=difficulty, name=session.get('name'), score=session.get('score')) #, result=result, result_class=result_class)
        except ValueError:
            result = 'Invalid input. Please enter a valid sequence of numbers separated by spaces.'
            flash(result, 'error')
            return render_template('memory_game.html', message="Guess the sequence!["+' '.join([str(i) for i in session['target']])+']', sequence=sequenceform, 
                                   difficulty=session.get('difficulty'), name=session.get('name'), score=session.get('score')) #, result=result, result_class="error")

    @app.route('/submit_guess', methods=['POST'])
    def submit_guess():
        """
        Submits a guess for the Guess Game, and redirects to a page that displays
        the result of the guess. If the guess is correct, the user is presented with a
        success message and a new secret number. If the guess is incorrect, the user is
        presented with an error message and the same secret number.
        """
        try:
            guess = int(request.form.get('guess'))
            secret_number = session['target']
            session['guess'] = guess  # Store the guess in the session

            if guess == secret_number: #or game.compare_results(guess):
                result = f"You won! Your guessed {guess} and it was right!!! Congratulations!!!"
                result_class = "success"  # Class for correct guess
                flash(result, 'success')
                update_session(session['name'], 2, difficulty, True, 1)
            else:
                result = f"You lost! You guessed {guess} but the new number was {new_secret_number}"
                result_class = "error"  # Class for incorrect guess
                flash(result, 'error')
                update_session(session['name'], 2, difficulty, False, 1)
            session['score'] = get_user_score(session['name'])

            # generate new game and re-render template
            game = GuessGame(difficulty)
            game.generate_number()  # Generate the secret number
            session['target'] = game.secret_number

            return render_template('guess_game.html', message="Guess the number!", top_number=game.top_number, secret_number=new_secret_number, 
                                   difficulty=difficulty, name=session.get('name'), score=session.get('score')) #, result=result, result_class=result_class)

        except ValueError:
            result = 'Invalid input. Please enter a valid number.'
            flash(result, 'error')
            return render_template('guess_game.html', message="Guess the number!", top_number=request.form.get('top_number'), secret_number=request.form.get('secret_number'), 
                                   difficulty=request.form.get('difficulty'), name=session.get('name'), score=session.get('score'))#, result=result, result_class="error")


    @app.route('/play_again', methods=['POST'])
    def play_again():
        """
        Redirects the user to the game selection screen, passing their name through the URL.
        """
        return redirect(url_for('welcome_user'), name=session.get('name'), score=session.get('score'))

    @app.route('/exit_game', methods=['POST'])
    def exit_game():
        """
        Exit the current game and return to the game selection screen.
        The current user's name is passed back to the game selection screen.
        """
        return render_template('game.html',  message="Choose a game", name=session.get('name'), score=session.get('score'))#, result="")


    import sqlite3

    @app.route('/top_scores', methods=['POST'])
    def top_scores():
        """Fetches the top 10 scores from the database and renders the top_scores.html template with the data."""

        # Connect to the database
        conn = sqlite3.connect('games.db')
        cursor = conn.cursor()

        # Fetch the top 10 scores
        cursor.execute('SELECT name, score FROM top_10_scores ORDER BY score DESC LIMIT 10')
        cursor.execute('SELECT name, score FROM top_10_scores ORDER BY score DESC LIMIT 10')
        top_scores = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Render the top_scores.html template
        return render_template('top_scores.html', top_scores=top_scores, name=session.get('name'), message="") #, result=""

    return app
