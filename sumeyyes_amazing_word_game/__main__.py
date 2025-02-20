from .utils import fetch_words
from random import choice


def main():
    words = fetch_words()

    x = choice(words)
    print(x[0])


if __name__ == "__main__":
    main()
