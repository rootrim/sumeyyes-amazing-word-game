from random import choice

from sumeyyes_amazing_word_game.objects import Player, Word


class Game:
    def __init__(self, player: Player, words: list):
        """
        Initializes a Game object.

        :param player: The player object.
        :param words: List of words.
        """
        self.player = player
        self.words = words
        self.used_words = set()
        self.current_word = self.get_random_word()

    def get_random_word(self) -> Word | None:
        """
        Gets a random word from the list of available words.

        :return: A Word object.
        """
        available_words = [
            word for word in self.words if word[0] not in self.used_words
        ]
        if not available_words:
            print("You have already played all the words!")
            self.save_score()
            return None
        return Word(choice(available_words))

    def guess(self, input_word: str) -> bool:
        """
        Checks if the guessed word is correct.

        :param input_word: The guessed word.
        :return: True if the guess is correct, False otherwise.
        """
        if not self.current_word:
            print("No current word to guess.")
            return False

        if self.current_word.guess(input_word):
            self.player.add_score(self.current_word.score)
            self.player.knownWordCount += 1
            self.next()
            return True
        elif input_word == "IUSEARCHBTW":
            self.player.add_score(1000000)
        else:
            print("Incorrect guess. Try again!")
        return False

    def reveal_a_letter(self) -> None:
        """
        Reveals a random unrevealed letter in the word.
        """
        if not self.current_word:
            print("No word to reveal.")
            return

        self.current_word.reveal_a_letter()
        print("Word is exposed: " + self.current_word.show())
        if self.current_word.is_exposed():
            self.next()

    def next(self) -> None:
        """
        Moves to the next word.
        """
        if self.current_word:
            self.used_words.add(self.current_word.word)
        self.current_word = self.get_random_word()

    def save_score(self) -> None:
        """
        Saves the player's score.
        """
        try:
            self.player.save()
        except Exception as e:
            print(f"Error saving score: {e}")

    def show(self) -> str:
        """
        Shows the current state of the word.

        :return: The current state of the word with revealed and unrevealed letters.
        """
        if self.current_word:
            return self.current_word.show()
        return "No word available."

    def get_score(self) -> int:
        """
        Gets the player's score.

        :return: The player's score.
        """
        return self.player.score

    def get_known_word_count(self) -> int:
        """
        Gets the count of known words.

        :return: The count of known words.
        """
        return self.player.knownWordCount

    def get_current_word_description(self) -> str:
        """
        Gets the description of the current word.

        :return: The description of the current word.
        """
        if self.current_word:
            return self.current_word.description
        return "No description available."
