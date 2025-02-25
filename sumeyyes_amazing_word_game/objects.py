import sqlite3
from random import choice
from typing import Tuple
from sumeyyes_amazing_word_game.utils import player_path

# Constants
LETTER_REVEAL_PENALTY = 100
WRONG_GUESS_PENALTY = 20
SCORE_MULTIPLIER = 100


class Letter:
    def __init__(self, character: str):
        """
        Initializes a Letter object.

        :param character: The character of the letter.
        """
        self.character = character
        self.revealed = False

    def show(self) -> str:
        """
        Shows the letter if revealed, otherwise shows an underscore.

        :return: The character or an underscore.
        """
        return self.character if self.revealed else "_"


class Word:
    def __init__(self, word: Tuple[str, str, int]):
        """
        Initializes a Word object.

        :param word: A tuple containing the word, its description, and its level.
        """
        self.word = word[0]
        self.letters = [Letter(character) for character in self.word]
        self.score = len(self.word) * SCORE_MULTIPLIER
        self.len = len(self.word)
        self.description = word[1]
        self.level = word[2]

    def reveal_a_letter(self) -> None:
        """
        Reveals a random unrevealed letter in the word and reduces the score.
        """
        choices = [letter for letter in self.letters if not letter.revealed]
        if choices:
            choice(choices).revealed = True
            self.score -= LETTER_REVEAL_PENALTY

    def show(self) -> str:
        """
        Shows the current state of the word.

        :return: The current state of the word with revealed and unrevealed letters.
        """
        return " ".join([letter.show() for letter in self.letters])

    def is_exposed(self) -> bool:
        """
        Checks if all letters in the word are revealed.

        :return: True if all letters are revealed, False otherwise.
        """
        return all(letter.revealed for letter in self.letters)

    def guess(self, word: str) -> bool:
        """
        Checks if the guessed word is correct.

        :param word: The guessed word.
        :return: True if the guess is correct, False otherwise.
        """
        word = word.strip().lower()
        if word == self.word:
            return True
        else:
            self.score -= WRONG_GUESS_PENALTY
            return False


class Player:
    def __init__(self, name: str):
        """
        Initializes a Player object.

        :param name: The name of the player.
        """
        self.name = name
        self.score = 0
        self.knownWordCount = 0

    def add_score(self, score: int) -> None:
        """
        Adds score to the player.

        :param score: The score to add.
        """
        self.score += score

    def __str__(self) -> str:
        """
        Returns the string representation of the player.

        :return: The string representation of the player.
        """
        return f"{self.name} has {self.score} points with {self.knownWordCount} known words."

    def save(self) -> None:
        """
        Saves the player's data to the database.
        """
        try:
            conn = sqlite3.connect(player_path)
            c = conn.cursor()
            c.execute(
                """
                INSERT OR REPLACE INTO players (name, score, knownWordCount)
                VALUES (?, ?, ?)
                """,
                (self.name, self.score, self.knownWordCount),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"An error occurred while saving the player: {e}")
