from random import choice
from sumeyyes_amazing_word_game.objects import Word


class Game:
    def __init__(self, player, words):
        self.player = player
        self.words = words
        self.used_words = set()
        self.current_word = Word(self.get_random_word())

    def get_random_word(self):
        try:
            return choice(
                [word for word in self.words if word[0] not in self.used_words]
            )
        except IndexError:
            print("Are you the Master? You have already known all the words!")

    def guess(self, input_word):
        if self.current_word.guess(input_word):
            self.player.add_score(self.current_word.score)
            self.player.knownWordCount += 1
            self.skip()
            return True
        return False

    def reveal_a_letter(self):
        self.current_word.reveal_a_letter()

    def skip(self):
        self.used_words.add(self.current_word.word)
        self.current_word = Word(self.get_random_word())

    def save_score(self):
        self.player.save()

    def show(self):
        return self.current_word.show()

    def get_score(self):
        return self.player.score

    def get_known_word_count(self):
        return self.player.knownWordCount

    def get_current_word_description(self):
        return self.current_word.description
