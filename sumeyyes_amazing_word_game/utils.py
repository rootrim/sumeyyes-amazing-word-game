import csv
import os
import sqlite3
import sys


def get_base_path():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.abspath("sumeyyes_amazing_word_game")


word_path = os.path.join(get_base_path(), "data", "words.db")
player_path = os.path.join(get_base_path(), "data", "players.db")
csv_path = os.path.join(get_base_path(), "data", "words.csv")


def fetch_words():
    conn = sqlite3.connect(word_path)
    cursor = conn.cursor()

    cursor.execute("SELECT word, meaning, level FROM words")

    words = cursor.fetchall()
    conn.close()

    return words


def init_db():
    conn = sqlite3.connect(word_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            level TEXT NOT NULL,
            meaning TEXT NOT NULL
        )
    """
    )
    print("Word database initialized.")

    conn.commit()
    conn.close()

    conn = sqlite3.connect(player_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            name TEXT NOT NULL UNIQUE,
            score INTEGER NOT NULL,
            knownWordCount INTEGER NOT NULL
        )
    """
    )
    print("Player database initialized.")
    conn.commit()
    conn.close()


def import_words_from_csv(csv_file=csv_path):
    conn = sqlite3.connect(word_path)
    cursor = conn.cursor()

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        imported = 0
        skipped = 0

        for row in reader:
            word = row["word"].strip()
            level = row["level"].strip().upper()
            meaning = row["meaning"].strip()

            try:
                cursor.execute(
                    "INSERT INTO words (word, level, meaning) VALUES (?, ?, ?)",
                    (word, level, meaning),
                )
                imported += 1
            except sqlite3.IntegrityError:
                print(f"⚠️ The word is already imported, skipped: '{word}'")
                skipped += 1

    conn.commit()
    conn.close()
    print(
        f"{imported} word imported successfully. {skipped} words skipped (already imported)."
    )


if __name__ == "__main__":
    init_db()
    import_words_from_csv()
