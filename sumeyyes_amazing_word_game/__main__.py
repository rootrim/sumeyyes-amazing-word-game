from sumeyyes_amazing_word_game.tui import main

if __name__ == "__main__":
    choice = input("Do you wanna play game as a TUI game(y/n)\n-> ")
    if choice.lower() == "y":
        main()
    else:
        print("Goodbye then!")
