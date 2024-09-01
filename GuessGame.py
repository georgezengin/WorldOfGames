import random

class GuessGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.secret_number = None
        self.top_number = self.get_top_number()

    def generate_number(self):
        self.secret_number = random.randint(1, self.top_number)

    def compare_results(self, guess):
        return guess == self.secret_number

    def get_top_number(self):
        return self.difficulty*10