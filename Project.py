import tkinter as tk
import json
import os
import random

class NumberGuesserAI:
    def __init__(self, master):
        self.master = master
        self.master.title("AI Number Guesser")

        self.learning_file = "learning_data.json"
        self.learning_data = self.load_learning_data()

        self.label = tk.Label(master, text="Think of a number between 1 and 100", font=("Arial", 14))
        self.label.pack(pady=10)

        self.guess_label = tk.Label(master, font=("Helvetica", 20, "bold"))
        self.guess_label.pack(pady=10)

        self.higher_button = tk.Button(master, text="Too Low", command=self.too_low, width=15)
        self.higher_button.pack(pady=2)

        self.lower_button = tk.Button(master, text="Too High", command=self.too_high, width=15)
        self.lower_button.pack(pady=2)

        self.correct_button = tk.Button(master, text="Correct!", command=self.correct_guess, width=15, bg="lightgreen")
        self.correct_button.pack(pady=2)

        self.reset_button = tk.Button(master, text="Reset Game", command=self.reset_game, width=15)
        self.reset_button.pack(pady=10)
        self.reset_game()

    def load_learning_data(self):
        if os.path.exists(self.learning_file):
            with open(self.learning_file, "r") as f:
                return json.load(f)
        else:
            return {}

    def save_learning_data(self):
        with open(self.learning_file, "w") as f:
            json.dump(self.learning_data, f)

    def get_guess(self):
        bias = [int(k) for k in self.learning_data if self.low <= int(k) <= self.high]
        if bias:
            return max(bias, key=lambda k: self.learning_data.get(str(k), 0))
        return (self.low + self.high) // 2

    def update_guess(self):
        if self.low > self.high:
            self.guess_label.config(text="Inconsistent Answers!")
            return
        self.guess = self.get_guess()
        self.guess_label.config(text=f"Is it {self.guess}?")

    def too_low(self):
        self.low = self.guess + 1
        self.update_guess()

    def too_high(self):
        self.high = self.guess - 1
        self.update_guess()

    def correct_guess(self):
        self.guess_label.config(text=f"Yay! It's {self.guess}")
        self.learning_data[str(self.guess)] = self.learning_data.get(str(self.guess), 0) + 1
        self.save_learning_data()

    def reset_game(self):
        self.low = 1
        self.high = 100
        self.update_guess()

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuesserAI(root)
    root.mainloop()