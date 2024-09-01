from flask import Flask, render_template, request, redirect, url_for, flash
#from live import welcome, load_game
from GuessGame import GuessGame

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

    @app.route('/')
    def index():
        """
        The home page for the World of Games.

        This page just renders the index.html template with no additional data.
        """
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

        message = welcome(name)
        return render_template('game.html', message=message, name=name)

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
        name = request.form.get('name')

        if not game_choice:
            flash('Game choice is required!', 'error')
            return render_template('game.html', message="Please choose a game.", name=name)
        
        if not difficulty:
            flash('Difficulty level is required!', 'error')
            return render_template('game.html', message="Please choose a difficulty level.", name=name)

        try:
            difficulty = int(difficulty)
        except ValueError:
            flash('Invalid difficulty level!', 'error')
            return render_template('game.html', message="Please choose a valid difficulty level.", name=name)

        if game_choice == '1':  # Assuming '4' refers to Memory Game
            return render_template('memory_game.html', 
                                   message="Memory Game is coming soon!",
                                   name=name)

        if game_choice == '2':  # Assuming '1' refers to GuessGame
            game = GuessGame(difficulty)
            game.generate_number()  # Generate the secret number
            return render_template('guess_game.html', 
                                   message="Guess the number!", 
                                   top_number=game.top_number,
                                   secret_number=game.secret_number, 
                                   difficulty=difficulty, 
                                   name=name, 
                                   result="")

        # Dummy function for other games
        if game_choice == '3':  # Assuming '3' refers to Currency Roulette
            return render_template('currency_roulette.html', 
                                   message="Currency Roulette is coming soon!",
                                   name=name)

        flash('Invalid game choice!', 'error')
        return redirect(url_for('index'))

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
            secret_number = int(request.form.get('secret_number'))
            difficulty = int(request.form.get('difficulty'))
            name = request.form.get('name')

            # Generate a new GuessGame instance for a new number
            game = GuessGame(difficulty)
            game.generate_number()  # Generate a new secret number
            new_secret_number = game.secret_number

#            if guess == new_secret_number:
            if game.compare_results(guess):
                result = f"You won! Your guessed {guess} and it was right!!! Congratulations!!!"
                result_class = "success"  # Class for correct guess
            else:
                result = f"You lost! You guessed {guess} but the new number was {new_secret_number}"
                result_class = "error"  # Class for incorrect guess

            return render_template('guess_game.html', 
                                   message="Guess the number!", 
                                   top_number=game.top_number,  # Update this value to reflect the current game state
                                   secret_number=new_secret_number, 
                                   difficulty=difficulty,
                                   name=name,
                                   result=result,
                                   result_class=result_class)

        except ValueError:
            flash('Invalid input. Please enter a valid number.', 'error')
            return render_template('guess_game.html', 
                                   message="Guess the number!", 
                                   top_number=request.form.get('top_number'),
                                   secret_number=request.form.get('secret_number'), 
                                   difficulty=request.form.get('difficulty'),
                                   name=request.form.get('name'),
                                   result="",
                                   result_class="error")

    @app.route('/exit_game', methods=['POST'])
    def exit_game():
        """
        Exit the current game and return to the game selection screen.
        The current user's name is passed back to the game selection screen.
        """
        return render_template('game.html',  message="Choose a game", name=request.form.get('name'))

    return app
