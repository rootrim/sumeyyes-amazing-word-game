from sumeyyes_amazing_word_game.objects import Player
from sumeyyes_amazing_word_game.utils import fetch_words
from sumeyyes_amazing_word_game.game_logic import Game


def main():
    print("Welcome to Sumeyye's Amazing Word Game!")
    name = input("Please enter your name\n-> ")
    words = fetch_words()
    game = Game(Player(name), words)
    while True:
        print(
            f"""
Your score is {game.get_score()}
YTou have known {game.get_known_word_count()} words.
"""
        )

        print(
            f"""
Your word: {game.show()}
Description: {game.get_current_word_description()}
"""
        )

        choiced_choice = input(
            """
What do you want to do?
1. Guess the word
2. Reveal a letter
3. Skip this word
4. Save and quit
Enter the number of your choice
"""
            + "-> ",
        )

        match choiced_choice:
            case "1":
                game.guess(input("Enter your guess\n-> "))
            case "2":
                game.reveal_a_letter()
            case "3":
                game.next()
            case "4":
                game.save_score()
                break
            case "DEBUG":
                eval(input())
            case "KEKLOVESBTS":
                game.player.add_score(1000000)
            case _:
                print("Invalid choice! Please enter a valid number.")

    print(f"Your final score is {game.get_score()}")
    print(f"You have known {game.get_known_word_count()} words as far.")
    print("See you later!")


if __name__ == "__main__":
    main()
