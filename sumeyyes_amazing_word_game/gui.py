import customtkinter as ctk
import threading
import time
from sumeyyes_amazing_word_game.game_logic import Game
from sumeyyes_amazing_word_game.objects import Player
from sumeyyes_amazing_word_game.utils import fetch_leaderboard

# Theme configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class WelcomeScreen(ctk.CTk):
    def __init__(self, words):
        super().__init__()
        self.words = words
        self.title("Welcome to Sümeyye's Amazing Word Game")
        self.geometry("400x300")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(
            self,
            text="Welcome to the Word Game!",
            font=("Arial", 20),
        )
        self.label.pack(pady=20)

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter your name...",
        )
        self.name_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(
            self,
            text="Start Game",
            command=self.start_game,
        )
        self.start_button.pack(pady=10)

    def start_game(self):
        player_name = self.name_entry.get().strip()
        if player_name:
            player = Player(player_name)
            self.destroy()
            app = WordGameApp(player, self.words)
            app.mainloop()


class WordGameApp(ctk.CTk):
    def __init__(self, player: Player, words: list):
        super().__init__()
        self.title("Sümeyye's Amazing Word Game")
        self.geometry("600x500")
        self.resizable(False, False)

        # Game object
        self.game = Game(player, words)

        # Timer setup
        self.timer_label = ctk.CTkLabel(
            self, text="Time Left: 2:00", font=("Arial", 16)
        )
        self.timer_label.pack(pady=5)

        # Start timer thread
        threading.Thread(target=self.start_timer, daemon=True).start()

        # Frame for content
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Word display
        self.word_label = ctk.CTkLabel(
            self.main_frame, text=self.game.show(), font=("Arial", 30)
        )
        self.word_label.pack(pady=10)

        # Word description and level
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Hint: {self.game.get_current_word_description()} (Level {self.game.current_word.level if self.game.current_word else None})",
            font=("Arial", 16),
        )
        self.desc_label.pack(pady=5)

        # Guess input box
        self.entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Guess the word...",
        )
        self.entry.pack(pady=5)

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=5)

        self.guess_button = ctk.CTkButton(
            self.button_frame,
            text="Guess",
            command=self.make_guess,
        )
        self.guess_button.pack(side="left", padx=5)

        self.reveal_button = ctk.CTkButton(
            self.button_frame,
            text="Reveal Letter",
            command=self.reveal_letter,
        )
        self.reveal_button.pack(side="left", padx=5)

        # Lower button frame for Skip and Save & Exit
        self.lower_button_frame = ctk.CTkFrame(self.main_frame)
        self.lower_button_frame.pack(pady=10)

        self.skip_button = ctk.CTkButton(
            self.lower_button_frame,
            text="Skip",
            command=self.skip_word,
        )
        self.skip_button.pack(side="left", padx=5)

        self.save_and_exit_button = ctk.CTkButton(
            self.lower_button_frame,
            text="Save & Exit",
            command=self.save_and_exit,
        )
        self.save_and_exit_button.pack(side="left", padx=5)

        # Score and known words
        self.score_label = ctk.CTkLabel(
            self.main_frame, text=f"Score: {self.game.get_score()}", font=("Arial", 16)
        )
        self.score_label.pack(pady=5)

        self.known_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Known Words: {self.game.get_known_word_count()}",
            font=("Arial", 16),
        )
        self.known_label.pack(pady=5)

        # Result message
        self.message_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 14))
        self.message_label.pack(pady=5)

    def start_timer(self):
        while self.game.time_left > 0 and self.game.timer_running:
            mins, secs = divmod(self.game.time_left, 60)
            time_format = f"Time Left: {mins:02d}:{secs:02d}"
            self.timer_label.configure(text=time_format)
            time.sleep(1)
            self.game.time_left -= 1

        if self.game.time_left <= 0:
            self.save_and_exit()

    def make_guess(self):
        guess = self.entry.get().strip()
        if self.game.guess(guess):
            self.message_label.configure(
                text="Correct Guess! 🎉",
                text_color="green",
            )
        else:
            self.message_label.configure(
                text="Wrong Guess! ❌",
                text_color="red",
            )
        self.update_ui()

    def reveal_letter(self):
        self.game.reveal_a_letter()
        self.update_ui()

    def skip_word(self):
        self.game.next()
        self.update_ui()

    def save_and_exit(self):
        self.game.timer_running = False
        self.game.save_score()
        leaderboard = LeaderboardScreen()
        leaderboard.mainloop()
        self.destroy()

    def update_ui(self):
        self.word_label.configure(text=self.game.show())
        self.desc_label.configure(
            text=f"Hint: {self.game.get_current_word_description()} (Level {self.game.current_word.level if self.game.current_word else None})"
        )
        self.score_label.configure(text=f"Score: {self.game.get_score()}")
        self.known_label.configure(
            text=f"Known Words: {self.game.get_known_word_count()}"
        )
        self.entry.delete(0, ctk.END)


class LeaderboardScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Leaderboard")
        self.geometry("500x500")

        self.label = ctk.CTkLabel(
            self,
            text="Leaderboard",
            font=("Arial", 20),
        )
        self.label.pack(pady=20)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.populate_leaderboard()

        self.exit_button = ctk.CTkButton(
            self,
            text="Exit",
            command=self.destroy,
        )
        self.exit_button.pack(pady=10, side="bottom")

    def populate_leaderboard(self):
        leaderboard = fetch_leaderboard()

        headers = ["Rank", "Name", "Score", "Known Words"]
        for col, text in enumerate(headers):
            label = ctk.CTkLabel(self.frame, text=text, font=("Arial", 14, "bold"))
            label.grid(row=0, column=col, padx=5, pady=5, sticky="w")

        for idx, (name, score, known_words) in enumerate(leaderboard, start=1):
            rank_label = ctk.CTkLabel(self.frame, text=str(idx), font=("Arial", 14))
            rank_label.grid(row=idx, column=0, padx=5, pady=2, sticky="w")

            name_label = ctk.CTkLabel(self.frame, text=name, font=("Arial", 14))
            name_label.grid(row=idx, column=1, padx=5, pady=2, sticky="w")

            score_label = ctk.CTkLabel(self.frame, text=str(score), font=("Arial", 14))
            score_label.grid(row=idx, column=2, padx=5, pady=2, sticky="w")

            words_label = ctk.CTkLabel(
                self.frame, text=str(known_words), font=("Arial", 14)
            )
            words_label.grid(row=idx, column=3, padx=5, pady=2, sticky="w")


if __name__ == "__main__":
    words = [
        ("python", "A programming language", 1),
        ("algorithm", "Steps to solve problems", 2),
        ("database", "A system to store data", 1),
    ]

    welcome = WelcomeScreen(words)
    welcome.mainloop()
