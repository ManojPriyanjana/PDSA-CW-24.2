import tkinter as tk
from tkinter import messagebox
import threading
import random
import mysql.connector
import re
import time

BOARD_SIZE = 8
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'knight_game'
}

def setup_database():
    try:
        # connect without specifying database first
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        # create database if needed
        cursor.execute("CREATE DATABASE IF NOT EXISTS `{}`".format(DB_CONFIG['database']))
        # switch into it
        conn.database = DB_CONFIG['database']
        # create a simple scores table (optional)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                player_name VARCHAR(100),
                score INT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # create algorithm timings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS algorithm_timings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                player_name VARCHAR(100),
                algorithm VARCHAR(50),
                duration FLOAT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except mysql.connector.Error as e:
        print("Database setup error:", e)
    finally:
        cursor.close()
        conn.close()

class KnightsTourGame:
    def __init__(self, root):
        setup_database()
        self.root = root
        self.root.title("Knight's Tour Game with MySQL")
        self.player_name = tk.StringVar()
        self.suggested_move = None
        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        top = tk.Frame(self.root)
        top.pack(pady=5)

        tk.Label(top, text="Player Name:").pack(side=tk.LEFT)
        tk.Entry(top, textvariable=self.player_name, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="OK", command=self.start_game).pack(side=tk.LEFT, padx=5)
        self.warn_btn = tk.Button(top, text="Warnsdorff", command=self.suggest_warnsdorff, state=tk.DISABLED)
        self.warn_btn.pack(side=tk.LEFT, padx=5)
        self.bt_btn = tk.Button(top, text="Backtracking", command=self.suggest_backtracking, state=tk.DISABLED)
        self.bt_btn.pack(side=tk.LEFT, padx=5)

        self.move_label = tk.Label(self.root, text="Moves: 0", font=("Arial", 12), fg="green")
        self.move_label.pack()
        self.feedback = tk.Label(self.root, text="", font=("Arial", 12), fg="blue")
        self.feedback.pack()

        self.canvas = tk.Canvas(self.root, width=BOARD_SIZE*60, height=BOARD_SIZE*60)
        self.canvas.pack(pady=5)
        self.canvas.bind("<Button-1>", self.on_click)

    def reset_game(self):
        self.board = [[-1]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.visited = [[False]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.move_count = 0
        self.current_pos = None
        self.suggested_move = None
        self.draw_board()
        self.move_label.config(text="Moves: 0")
        self.feedback.config(text="")

    def start_game(self):
        name = self.player_name.get().strip()
        if not re.fullmatch(r"[A-Za-z ]{3,50}", name):
            messagebox.showwarning("Invalid Name", "Enter 3–50 letters only.")
            return
        self.reset_game()
        self.feedback.config(text=f"Welcome {name}! Click a square to start.")
        self.warn_btn.config(state=tk.NORMAL)
        self.bt_btn.config(state=tk.NORMAL)

    def draw_board(self):
        self.canvas.delete("all")
        size = 60
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                color = "white" if (r+c)%2==0 else "gray"
                if self.visited[r][c]:
                    color = "lightblue"
                if self.suggested_move == (r,c):
                    color = "yellow"
                x1, y1 = c*size, r*size
                self.canvas.create_rectangle(x1, y1, x1+size, y1+size, fill=color, outline="black")
                if self.board[r][c] != -1:
                    self.canvas.create_text(x1+size/2, y1+size/2,
                                            text=str(self.board[r][c]), font=("Arial", 16))
        if self.current_pos:
            r,c = self.current_pos
            x, y = c*size + size/2, r*size + size/2
            self.canvas.create_text(x, y, text="♞", font=("Arial", 24), fill="red")

    def on_click(self, evt):
        col, row = evt.x//60, evt.y//60
        if not (0<=row<BOARD_SIZE and 0<=col<BOARD_SIZE):
            return
        if self.move_count == 0:
            self._make_move(row, col)
            self.feedback.config(text="First move placed.")
        else:
            if self._valid(row, col):
                self._make_move(row, col)
                self.feedback.config(text=f"Move {self.move_count} made.")
            else:
                self.feedback.config(text="Invalid move! Game Over.")
                messagebox.showinfo("Game Over",
                                    f"{self.player_name.get()}, your score: {self.move_count}")
                self._save_score(self.player_name.get(), self.move_count)
                self.warn_btn.config(state=tk.DISABLED)
                self.bt_btn.config(state=tk.DISABLED)
                self.reset_game()

    def _make_move(self, r, c):
        self.board[r][c] = self.move_count
        self.visited[r][c] = True
        self.current_pos = (r, c)
        self.move_count += 1
        self.suggested_move = None
        self.move_label.config(text=f"Moves: {self.move_count}")
        self.draw_board()

    def _valid(self, r, c):
        if not (0<=r<BOARD_SIZE and 0<=c<BOARD_SIZE): return False
        if self.visited[r][c]: return False
        pr,pc = self.current_pos
        return (r-pr, c-pc) in KNIGHT_MOVES

    def _random_start(self):
        if self.move_count==0:
            r = random.randrange(BOARD_SIZE)
            c = random.randrange(BOARD_SIZE)
            self._make_move(r, c)

    def suggest_warnsdorff(self):
        try:
            self._random_start()
            start = time.time()
            r,c = self.current_pos
            best = None
            min_deg = 9
            for dr,dc in KNIGHT_MOVES:
                nr,nc = r+dr, c+dc
                if self._valid(nr,nc):
                    deg = sum(1 for d2 in KNIGHT_MOVES
                              if 0<=nr+d2[0]<BOARD_SIZE and
                                 0<=nc+d2[1]<BOARD_SIZE and
                                 not self.visited[nr+d2[0]][nc+d2[1]])
                    if deg<min_deg:
                        min_deg, best = deg, (nr,nc)
            duration = time.time() - start
            self._save_timing("Warnsdorff", duration)
            if best:
                self.suggested_move = best
                self.feedback.config(
                    text=f"Warnsdorff → {best} in {duration:.4f}s"
                )
            else:
                self.feedback.config("No moves left.")
            self.draw_board()
        except Exception as e:
            messagebox.showerror("Warnsdorff Error", str(e))

    def suggest_backtracking(self):
        try:
            self._random_start()
            threading.Thread(target=self._do_backtrack, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Backtracking Start Error", str(e))

    def _do_backtrack(self):
        start = time.time()
        r,c = self.current_pos
        # try each possible knight move
        for dr,dc in KNIGHT_MOVES:
            nr,nc = r+dr, c+dc
            if self._valid(nr,nc):
                tb = [row[:] for row in self.board]
                tv = [row[:] for row in self.visited]
                tb[nr][nc] = self.move_count
                tv[nr][nc] = True
                if self._backtrack(nr, nc, self.move_count+1, tb, tv):
                    duration = time.time() - start
                    self._save_timing("Backtracking", duration)
                    self.suggested_move = (nr,nc)
                    self.root.after(0, lambda: (
                        self.feedback.config(
                          text=f"Backtracking → {(nr,nc)} in {duration:.4f}s"
                        ),
                        self.draw_board()
                    ))
                    return
        self.root.after(0, lambda:
            self.feedback.config(text="Backtracking found no path.")
        )

    def _backtrack(self, r, c, movei, board, visited):
        if movei == BOARD_SIZE*BOARD_SIZE:
            return True
        for dr,dc in KNIGHT_MOVES:
            nr,nc = r+dr, c+dc
            if 0<=nr<BOARD_SIZE and 0<=nc<BOARD_SIZE and not visited[nr][nc]:
                board[nr][nc] = movei
                visited[nr][nc] = True
                if self._backtrack(nr,nc,movei+1, board, visited):
                    return True
                visited[nr][nc] = False
        return False

    def _save_score(self, name, score):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO scores (player_name, score) VALUES (%s,%s)",
                (name, score)
            )
            conn.commit()
        except Exception as e:
            messagebox.showerror("DB Error", f"Saving score failed: {e}")
        finally:
            cur.close()
            conn.close()

    def _save_timing(self, algorithm, duration):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO algorithm_timings (player_name, algorithm, duration) VALUES (%s,%s,%s)",
                (self.player_name.get(), algorithm, duration)
            )
            conn.commit()
        except Exception as e:
            messagebox.showerror("DB Error", f"Saving timing failed: {e}")
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    game = KnightsTourGame(root)
    root.mainloop()
