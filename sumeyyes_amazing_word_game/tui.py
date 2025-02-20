from random import choice

from sumeyyes_amazing_word_game.objects import Word
from sumeyyes_amazing_word_game.utils import fetch_words


def game():
    used_words = set()
    (word, description, level) = random_word(used_words)
    word = Word(word)
    print(f"This word's level is {level}")
    print(description)

    while not word.is_exposed():
        print(word.show())
        print(
            """What do you want to do?
1. Guess the word
2. Get a random letter 
3. Skip this word
4. Exit
[Enter a number between 1-4]-> 
"""
        )
        match input():
            case "1":
                input_word = input("Enter a word:\n").lower()
                if word.guess(input_word):
                    print("You guessed the word!")
                    break

            case "2":
                word.reveal_a_letter()
            case "3":
                game()
                exit()
            case "4":
                return
    print(f"Your score is: {word.score}")


def random_word(used_words=set()):
    random_word = choice(fetch_words())
    while random_word in used_words:
        random_word = choice(fetch_words())
    return random_word
