import tkinter as tk
from tkinter import messagebox
import time
import random
import sys
import json

import mysql.connector
from mysql.connector import Error
import unittest

# ───── DATABASE CONFIG ─────────────────────────────────────────────
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'root',
    'database': 'tictactoe5x5'
}

# ───── DATABASE SETUP ──────────────────────────────────────────────
def init_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`;")
        conn.database = DB_CONFIG['database']
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS wins (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            player        VARCHAR(100),
            board_state   TEXT,
            won_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          ) ENGINE=InnoDB
        """)
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS move_times (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            algorithm     VARCHAR(50),
            move_no       INT,
            duration      DOUBLE,
            recorded_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          ) ENGINE=InnoDB
        """)
        conn.commit()
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Unable to initialize database:\n{e}")
        sys.exit(1)

# ───── GLOBAL CONSTANTS ─────────────────────────────────────────────
BOARD_SIZE    = 5      # 5×5 board
WIN_LENGTH    = 5      # need 5 in a row
AI_RANDOMNESS = 0.30   # 30% purely random moves
MINIMAX_DEPTH = 1      # reduced depth for further weakening

# ───── MAIN GAME WINDOW ────────────────────────────────────────────
class TicTacToe5x5(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe 5×5")
        self.resizable(False, False)

        # DB + state
        self.conn        = init_db()
        self.move_count  = 0
        self.player_name = None

        # — Player Name Input —
        name_frame = tk.Frame(self, pady=5)
        tk.Label(name_frame, text="Player Name:").pack(side="left")
        self.name_entry = tk.Entry(name_frame, width=20)
        self.name_entry.pack(side="left", padx=5)
        tk.Button(name_frame, text="OK", command=self._set_player_name).pack(side="left")
        name_frame.pack()

        # — Algorithm Selection —
        controls = tk.Frame(self, pady=10)
        self.algo_var = tk.StringVar(value="heuristic")
        tk.Radiobutton(controls, text="Heuristic", variable=self.algo_var,
                       value="heuristic").pack(side="left", padx=5)
        tk.Radiobutton(controls, text="Minimax", variable=self.algo_var,
                       value="minimax").pack(side="left", padx=5)
        controls.pack()

        # — Status —
        self.status = tk.Label(self, text="Enter name before play game", font=("Arial", 18))
        self.status.pack()

        # — Board —
        self.board   = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.buttons = []
        grid = tk.Frame(self)
        for r in range(BOARD_SIZE):
            row = []
            for c in range(BOARD_SIZE):
                btn = tk.Button(grid, text=" ",
                                width=4, height=2,
                                font=("Arial", 24),
                                command=lambda r=r, c=c: self._on_human_move(r, c))
                btn.grid(row=r, column=c, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        grid.pack()

        # — Restart —
        self.reset_button = tk.Button(self, text="Restart Game", font=("Arial", 16),
                                      command=self._reset)
        self.reset_button.pack(pady=10)

    def _set_player_name(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Validation Error", "Player Name cannot be empty.")
            return
        self.player_name = name
        messagebox.showinfo("Name Set", f"Player name set to: {name}")
        self.status.config(text="Your turn (X)")

    def _on_human_move(self, row, col):
        if not self.player_name:
            messagebox.showwarning("Validation Error", "Enter name before play game.")
            return
        if self.board[row][col] != " ":
            return
        self.board[row][col] = "X"
        self.buttons[row][col]["text"] = "X"
        try:
            if self._check_win("X"): return self._handle_win("You (X)")
            if self._check_draw(): return self._handle_draw()
            self.status.config(text="Computer thinking…")
            self.after(100, self._computer_move)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error during your move:\n{e}")

    def _computer_move(self):
        try:
            self.move_count += 1
            start = time.time()

            # 30% random
            empties = [(r, c)
                       for r in range(BOARD_SIZE)
                       for c in range(BOARD_SIZE)
                       if self.board[r][c] == " "]
            if random.random() < AI_RANDOMNESS:
                move = random.choice(empties)
            else:
                if self.algo_var.get() == "minimax":
                    move = self._minimax_move(MINIMAX_DEPTH)
                else:
                    move = self._heuristic_move()

            duration = time.time() - start
            self._record_move_time(self.algo_var.get(), self.move_count, duration)

            r, c = move
            self.board[r][c] = "O"
            self.buttons[r][c]["text"] = "O"
            if self._check_win("O"): return self._handle_win("Computer (O)")
            if self._check_draw(): return self._handle_draw()
            self.status.config(text="Your turn (X)")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error during computer move:\n{e}")

    def _heuristic_move(self):
        # win or block
        for p in ("O", "X"):
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if self.board[r][c] == " ":
                        self.board[r][c] = p
                        if self._check_win(p):
                            self.board[r][c] = " "
                            return (r, c)
                        self.board[r][c] = " "
        return random.choice([(r, c)
                              for r in range(BOARD_SIZE)
                              for c in range(BOARD_SIZE)
                              if self.board[r][c] == " "])

    def _minimax_move(self, depth, is_max=True):
        best = (-999, None)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == " ":
                    self.board[r][c] = "O" if is_max else "X"
                    score = self._minimax(depth-1, not is_max)
                    self.board[r][c] = " "
                    if (is_max and score > best[0]) or (not is_max and score < best[0]):
                        best = (score, (r, c))
        return best[1] or self._heuristic_move()

    def _minimax(self, depth, is_max):
        if self._check_win("O"): return  1
        if self._check_win("X"): return -1
        if self._check_draw() or depth <= 0: return 0
        best = -999 if is_max else 999
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == " ":
                    self.board[r][c] = "O" if is_max else "X"
                    val = self._minimax(depth-1, not is_max)
                    self.board[r][c] = " "
                    best = max(best, val) if is_max else min(best, val)
        return best

    def _check_win(self, p):
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == p for j in range(BOARD_SIZE)): return True
            if all(self.board[j][i] == p for j in range(BOARD_SIZE)): return True
        if all(self.board[i][i] == p for i in range(BOARD_SIZE)): return True
        if all(self.board[i][BOARD_SIZE-1-i] == p for i in range(BOARD_SIZE)): return True
        return False

    def _check_draw(self):
        return all(self.board[r][c] != " "
                   for r in range(BOARD_SIZE)
                   for c in range(BOARD_SIZE))

    def _handle_win(self, who):
        messagebox.showinfo("Game Over", f"{who} wins!")
        if who.startswith("You"):
            self._record_win(self.player_name)
        self.status.config(text="Game over")

    def _handle_draw(self):
        messagebox.showinfo("Game Over", "It's a draw!")
        self.status.config(text="Game over")

    def _reset(self):
        if not self.player_name:
            messagebox.showwarning("Validation Error", "Enter name before play game.")
            return
        self.move_count = 0
        self.status.config(text="Your turn (X)")
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.board[r][c] = " "
                self.buttons[r][c].config(text=" ", state="normal")

    def _record_win(self, player_name):
        try:
            state = json.dumps(self.board)
            cur = self.conn.cursor()
            cur.execute("INSERT INTO wins (player, board_state) VALUES (%s,%s)",
                        (player_name, state))
            self.conn.commit()
        except (Error, json.JSONDecodeError) as e:
            messagebox.showwarning("DB Warning", f"Failed to record win:\n{e}")

    def _record_move_time(self, algo, move_no, duration):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO move_times (algorithm, move_no, duration) VALUES (%s,%s,%s)",
                        (algo, move_no, duration))
            self.conn.commit()
        except Error as e:
            messagebox.showwarning("DB Warning", f"Failed to record move time:\n{e}")

# ───── UNIT TESTS ────────────────────────────────────────────────
class TestTicTacToeLogic(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe5x5.__new__(TicTacToe5x5)
        self.game.board = [[" "] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    def test_check_win_row(self):
        g = self.game
        g.board[0] = ["X"] * BOARD_SIZE
        self.assertTrue(g._check_win("X"))

    def test_check_win_column(self):
        g = self.game
        for i in range(BOARD_SIZE):
            g.board[i][1] = "O"
        self.assertTrue(g._check_win("O"))

    def test_check_win_diagonal(self):
        g = self.game
        for i in range(BOARD_SIZE):
            g.board[i][i] = "X"
        self.assertTrue(g._check_win("X"))

    def test_check_win_anti_diagonal(self):
        g = self.game
        for i in range(BOARD_SIZE):
            g.board[i][BOARD_SIZE-1-i] = "O"
        self.assertTrue(g._check_win("O"))

    def test_check_draw(self):
        g = self.game
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                g.board[r][c] = "X" if (r+c) % 2 == 0 else "O"
        self.assertTrue(g._check_draw())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        TicTacToe5x5().mainloop()
