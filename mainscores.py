from flask import Flask, render_template_string
import os

# MainScores.py

app = Flask(__name__)

SCORES_FILE_NAME = "Scores.txt"

@app.route('/')
def score_server():
    """Serve the score over HTTP."""
    try:
        # Try reading the score from the file
        with open(SCORES_FILE_NAME, 'r') as f:
            score = f.read()
        
        # If the score is empty or invalid, raise an exception
        if not score.strip():
            raise ValueError("Invalid score content")
        
        score_html = f"""
        <html>
        <head>
        <title>Scores Game</title>
        </head>
        <body>
        <h1>The score is <div id="score">{score}</div></h1>
        </body>
        </html>
        """
        return render_template_string(score_html)

    except Exception as e:
        error_html = f"""
        <html>
        <head>
        <title>Scores Game</title>
        </head>
        <body>
        <h1><div id="score" style="color:red">Error: {str(e)}</div></h1>
        </body>
        </html>
        """
        return render_template_string(error_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
