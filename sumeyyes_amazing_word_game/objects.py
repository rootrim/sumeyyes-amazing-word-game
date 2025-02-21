import os
import sqlite3
from random import choice
from sumeyyes_amazing_word_game.utils import get_base_path

player_path = os.path.join(get_base_path(), "data", "players.db")


class Letter:
    def __init__(self, character):
        self.character = character
        self.revealed = False

    def show(self):
        return self.character if self.revealed else "_"


class Word:
    def __init__(self, word):
        self.word = word[0]
        self.letters = [Letter(character) for character in self.word]
        self.score = len(self.word) * 100
        self.len = len(self.word)
        self.description = word[1]
        self.level = word[2]

    def reveal_a_letter(self):
        choices = [letter for letter in self.letters if not letter.revealed]
        choice(choices).revealed = True
        self.score -= 100

    def show(self):
        return " ".join([letter.show() for letter in self.letters])

    def is_exposed(self):
        return all([letter.revealed for letter in self.letters])

    def guess(self, word):
        if word == self.word:
            return True
        else:
            self.score -= 20
            return False


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.knownWordCount = 0

    def add_score(self, score):
        self.score += score

    def __str__(self):
        return f"{self.name} has {self.score} points with {self.knownWordCount} known words."

    def save(self):
        conn = sqlite3.connect(player_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO players VALUES (?, ?, ?)",
            (self.name, self.score, self.knownWordCount),
        )
        conn.commit()
        conn.close()


#   def load(self):
#       conn = sqlite3.connect("players.db")
#       c = conn.cursor()
#       c.execute("SELECT * FROM players WHERE name=?", (self.name,))
#       player = c.fetchone()
#       if player:
#           self.score = player[1]
#           self.knownWordCount = player[2]
#       conn.close()
#       return player
