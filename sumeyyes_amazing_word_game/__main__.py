from sumeyyes_amazing_word_game.gui import WelcomeScreen
from sumeyyes_amazing_word_game.utils import fetch_words


if __name__ == "__main__":
    welcome = WelcomeScreen(fetch_words())
    welcome.mainloop()
