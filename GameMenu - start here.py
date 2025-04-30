import tkinter as tk
import subprocess
import sys
import os

class GameMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Work 24.2 – Game Menu")
        self.geometry("800x600")
        self.resizable(False, False)

        nav_frame = tk.Frame(self, bd=2, relief="groove", width=200)
        nav_frame.pack(side="left", fill="y")
        container = tk.Frame(self)
        container.pack(side="right", expand=True, fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Define frames; now including TSP and Eight Queens
        games = [
            ("Tic-Tac-Toe", TicTacToeFrame),
            ("TSP", TSPFrame),
            ("Tower of Hanoi",TowerOfHonoiFrame ),
            ("Eight Queens", EightQueensFrame),
            ("Knight's Tour", KnightTourFrame)
        ]

        self.frames = {}
        for name, F in games:
            frame = F(container, name)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            btn = tk.Button(nav_frame, text=name, width=18, pady=5,
                            command=lambda n=name: self.show_frame(n))
            btn.pack(padx=10, pady=5)

        self.show_frame("Tic-Tac-Toe")

    def show_frame(self, name):
        self.frames[name].tkraise()


class TicTacToeFrame(tk.Frame):
    def __init__(self, parent, _name):
        super().__init__(parent)
        tk.Label(self, text="Tic-Tac-Toe 5×5", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Launch Tic-Tac-Toe", font=("Arial", 16),
                  command=self.launch_game).pack(pady=10)

    def launch_game(self):
        here = os.path.dirname(__file__)
        script = os.path.join(here, "tic_tac_toe.py")
        subprocess.Popen([sys.executable, script])


class TSPFrame(tk.Frame):
    def __init__(self, parent, _name):
        super().__init__(parent)
        tk.Label(self, text="Traveling Salesman", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Launch Traveling Salesman", font=("Arial", 16),
                  command=self.launch_game).pack(pady=10)

    def launch_game(self):
        here = os.path.dirname(__file__)
        script = os.path.join(here, "travalling selles man.py")
        subprocess.Popen([sys.executable, script])


class EightQueensFrame(tk.Frame):
    def __init__(self, parent, _name):
        super().__init__(parent)
        tk.Label(self, text="Eight Queens Puzzle", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Launch Eight Queens Puzzle", font=("Arial", 16),
                  command=self.launch_game).pack(pady=10)

    def launch_game(self):
        here = os.path.dirname(__file__)
        script = os.path.join(here, "Eight queen's puzzle.py")
        subprocess.Popen([sys.executable, script])


class TowerOfHonoiFrame(tk.Frame):
    # def __init__(self, parent, name):
    #     super().__init__(parent)
    #     tk.Label(self, text=name, font=("Arial", 24), fg="gray").pack(expand=True)
     def __init__(self, parent, _name):
        super().__init__(parent)
        tk.Label(self, text="Tower of honoi", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Launch Tower of honoi", font=("Arial", 16),
                  command=self.launch_game).pack(pady=10)

     def launch_game(self):
        here = os.path.dirname(__file__)
        script = os.path.join(here, "tower of honoi.py")
        subprocess.Popen([sys.executable, script])

class KnightTourFrame(tk.Frame):
     def __init__(self, parent, _name):
        super().__init__(parent)
        tk.Label(self, text="knight's tour", font=("Arial", 24)).pack(pady=20)
        tk.Button(self, text="Launch knight's tour", font=("Arial", 16),
                  command=self.launch_game).pack(pady=10)

     def launch_game(self):
        here = os.path.dirname(__file__)
        script = os.path.join(here, "knights tour game.py")
        subprocess.Popen([sys.executable, script])


if __name__ == "__main__":

    app = GameMenu()
    app.mainloop()
