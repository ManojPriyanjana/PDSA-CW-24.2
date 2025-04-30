import threading
import time
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import unittest
import os

# ───── Database Manager ────────────────────────────────────────────────
class DBManager:
    """
    Manages MySQL connection and all database operations:
      - Ensures necessary tables exist
      - Saves unique solutions for sequential/threaded runs
      - Records performance timings
      - Tracks player-submitted solutions and flags
    """
    def __init__(self,
                 host='localhost', user='root', password='root', database='eight_queens'):
        try:
            # Attempt to connect to MySQL
            self.conn = mysql.connector.connect(
                host=host, user=user, password=password, database=database
            )
            self._ensure_tables()
        except Error as e:
            # Fatal if we cannot connect
            raise RuntimeError(f"DB connection failed: {e}")

    def _ensure_tables(self):
        """Create all required tables if they don't already exist."""
        c = self.conn.cursor()
        c.execute("""
          CREATE TABLE IF NOT EXISTS seq_solutions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pos VARCHAR(100) UNIQUE,
            found BOOL DEFAULT FALSE
          )
        """)
        c.execute("""
          CREATE TABLE IF NOT EXISTS thr_solutions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pos VARCHAR(100) UNIQUE,
            found BOOL DEFAULT FALSE
          )
        """)
        c.execute("""
          CREATE TABLE IF NOT EXISTS game_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_name VARCHAR(64),
            pos VARCHAR(100),
            mode VARCHAR(16),
            time_submitted DATETIME DEFAULT CURRENT_TIMESTAMP
          )
        """)
        c.execute("""
          CREATE TABLE IF NOT EXISTS performance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mode VARCHAR(16),
            duration FLOAT
          )
        """)
        self.conn.commit()

    def save_solution(self, pos_str, mode):
        """
        Save a solution string into the appropriate table.
        Ignores duplicates. Raises ValueError on bad mode.
        """
        if mode not in ('Sequential', 'Threaded'):
            raise ValueError(f"Unknown mode: {mode}")
        table = 'seq_solutions' if mode == 'Sequential' else 'thr_solutions'
        try:
            c = self.conn.cursor()
            c.execute(f"INSERT IGNORE INTO {table}(pos) VALUES (%s)", (pos_str,))
            self.conn.commit()
        except Error as e:
            # Log but do not crash
            print(f"[DB] Error saving solution ({mode}): {e}")

    def record_performance(self, mode, duration):
        """
        Record the time taken (in seconds) for a given mode.
        """
        if mode not in ('Sequential', 'Threaded'):
            raise ValueError(f"Unknown mode: {mode}")
        try:
            c = self.conn.cursor()
            c.execute(
                "INSERT INTO performance(mode, duration) VALUES (%s, %s)",
                (mode, duration)
            )
            self.conn.commit()
        except Error as e:
            print(f"[DB] Error recording performance: {e}")

    def get_performance(self):
        """
        Retrieve all recorded (mode, duration) pairs.
        Returns a list of tuples.
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT mode, duration FROM performance")
            return c.fetchall()
        except Error as e:
            print(f"[DB] Error fetching performance data: {e}")
            return []

    def mark_found(self, pos_str, player_name, mode):
        """
        Mark a player-submitted solution as found. Returns (ok:bool, message:str).
        - Rejects unknown solutions or duplicates.
        - If all are found, resets flags for next round.
        """
        if not player_name:
            return False, "Player name is required."
        if mode not in ('Sequential', 'Threaded'):
            return False, "Invalid mode selected."
        table = 'seq_solutions' if mode == 'Sequential' else 'thr_solutions'
        try:
            c = self.conn.cursor()
            c.execute(f"SELECT found FROM {table} WHERE pos = %s", (pos_str,))
            row = c.fetchone()
            if not row:
                return False, "That arrangement is not a recognized solution."
            if row[0]:
                return False, "This solution has already been identified. Try another."
            # Mark as found
            c.execute(f"UPDATE {table} SET found = TRUE WHERE pos = %s", (pos_str,))
            # Log the player's success
            c.execute(
                "INSERT INTO game_records(player_name, pos, mode) VALUES (%s, %s, %s)",
                (player_name, pos_str, mode)
            )
            self.conn.commit()
            # Check if we've found them all
            c.execute(f"SELECT COUNT(*) FROM {table} WHERE found = FALSE")
            remaining = c.fetchone()[0]
            if remaining == 0:
                # Reset for next session
                c.execute(f"UPDATE {table} SET found = FALSE")
                self.conn.commit()
                return True, "Correct! All solutions identified; flags have been reset."
            return True, "Correct! Your solution has been recorded."
        except Error as e:
            return False, f"Database error: {e}"

    def reset_flags(self):
        """Manually reset all 'found' flags in both solution tables."""
        try:
            c = self.conn.cursor()
            c.execute("UPDATE seq_solutions SET found = FALSE")
            c.execute("UPDATE thr_solutions SET found = FALSE")
            self.conn.commit()
        except Error as e:
            print(f"[DB] Error resetting flags: {e}")

# ───── Eight-Queens Solver ─────────────────────────────────────────────
class EightQueensSolver:
    """
    Uses backtracking to generate all non-attacking placements
    of eight queens on an 8×8 board, both sequentially and
    in parallel (one thread per first-row choice).
    """
    def __init__(self):
        self.solutions = []

    def _backtrack(self, row, pos, col_u, d1_u, d2_u):
        """Recursive helper to place queens row by row."""
        if row == 8:
            self.solutions.append(pos.copy())
            return
        for c in range(8):
            if not (col_u[c] or d1_u[row + c] or d2_u[row - c + 7]):
                pos[row] = c
                col_u[c] = d1_u[row + c] = d2_u[row - c + 7] = True
                self._backtrack(row + 1, pos, col_u, d1_u, d2_u)
                col_u[c] = d1_u[row + c] = d2_u[row - c + 7] = False

    def find_sequential(self):
        """
        Compute all solutions in a single thread.
        Returns (formatted_solutions, duration_seconds).
        """
        self.solutions.clear()
        pos = [0]*8
        col_u = [False]*8
        d1_u = [False]*15
        d2_u = [False]*15
        start = time.perf_counter()
        self._backtrack(0, pos, col_u, d1_u, d2_u)
        elapsed = time.perf_counter() - start

        # Deduplicate and format as "(row,col)" pairs, 1-indexed
        unique = sorted(set(tuple(sol) for sol in self.solutions))
        formatted = [
            ",".join(f"({i+1},{c+1})" for i, c in enumerate(sol))
            for sol in unique
        ]
        return formatted, elapsed

    def find_threaded(self):
        """
        Launch one thread per initial column choice, then
        perform backtracking from row 1 downward.
        Returns (formatted_solutions, duration_seconds).
        """
        self.solutions.clear()

        def worker(first_col):
            local = [0]*8
            local[0] = first_col
            cu = [False]*8
            d1 = [False]*15
            d2 = [False]*15
            cu[first_col] = d1[first_col] = d2[-first_col+7] = True
            self._backtrack(1, local, cu, d1, d2)

        threads = []
        start = time.perf_counter()
        for c in range(8):
            t = threading.Thread(target=worker, args=(c,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        elapsed = time.perf_counter() - start

        unique = sorted(set(tuple(sol) for sol in self.solutions))
        formatted = [
            ",".join(f"({i+1},{c+1})" for i, c in enumerate(sol))
            for sol in unique
        ]
        return formatted, elapsed

# ───── Tkinter GUI ─────────────────────────────────────────────────────
class EightQueensUI:
    """
    Builds the user interface:
      - Mode selector (Sequential / Threaded)
      - Player name entry with validation
      - 8×8 chessboard for manual queen placement, with rule checks
      - Menu bar (Generate, Compare Performance, Reset, Exit)
      - Status bar (queens left, moves, Submit)
    """
    def __init__(self, solver, db, logo_path='queen_3.png'):
        self.solver = solver
        self.db = db

        # Precompute + store all solutions & timings up front
        try:
            for mode, func in [('Sequential', solver.find_sequential),
                               ('Threaded',   solver.find_threaded)]:
                sols, dur = func()
                for s in sols:
                    db.save_solution(s, mode)
                db.record_performance(mode, dur)
        except Exception as e:
            messagebox.showerror("Initialization Error",
                                 f"Failed to precompute solutions: {e}")
            raise

        # ─── Main window setup ────────────────────────────────
        self.root = tk.Tk()
        self.root.title("Eight Queens Puzzle")
        self.root.geometry("1400x800+0+0")

        # ─── Mode selector ───────────────────────────────────
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, y=10, anchor='n')
        tk.Label(frame, text="Select Mode:", font=("Arial", 12)).pack(side='left')
        self.mode_var = tk.StringVar(value='Sequential')
        tk.Radiobutton(frame, text='Sequential',
                       variable=self.mode_var, value='Sequential').pack(side='left', padx=5)
        tk.Radiobutton(frame, text='Threaded',
                       variable=self.mode_var, value='Threaded').pack(side='left')

        # ─── Player name entry ───────────────────────────────
        nf = tk.Frame(self.root)
        nf.place(relx=0.5, y=50, anchor='n')
        tk.Label(nf, text='Player Name:', font=("Arial", 12)).pack(side='left')
        self.name_entry = tk.Entry(nf, font=("Arial", 12), width=20)
        self.name_entry.pack(side='left', padx=5)
        self.name_ok = tk.Button(nf, text='OK', command=self.set_name)
        self.name_ok.pack(side='left')
        self.name_set = False

        # ─── Menu bar ────────────────────────────────────────
        menubar = tk.Menu(self.root)
        gm = tk.Menu(menubar, tearoff=0)
        gm.add_command(label='Generate', command=self.run_generate)
        gm.add_command(label='Compare Performance', command=self.compare_performance)
        gm.add_separator()
        gm.add_command(label='Reset Board', command=self.reset_board)
        gm.add_command(label='Reset Flags',
                       command=lambda: [db.reset_flags(), self.reset_board()])
        gm.add_separator()
        gm.add_command(label='Exit', command=self.root.quit)
        menubar.add_cascade(label="Eight Queens Puzzle", menu=gm)
        self.root.config(menu=menubar)

        # ─── Load queen icon ─────────────────────────────────
        self.queen_img = None
        if os.path.exists(logo_path):
            try:
                raw = Image.open(logo_path)
                cell = 60
                img = raw.resize((cell-10, cell-10), Image.Resampling.LANCZOS)
                self.queen_img = ImageTk.PhotoImage(img, master=self.root)
            except Exception as e:
                print(f"[UI] Warning: could not load image: {e}")
        else:
            print(f"[UI] Warning: logo file not found: {logo_path}")

        # ─── Chessboard setup ────────────────────────────────
        board = tk.Frame(self.root)
        board.place(relx=0.5, y=100, anchor='n')
        cell = 60
        for i in range(10):
            board.grid_rowconfigure(i, minsize=cell)
            board.grid_columnconfigure(i, minsize=cell)

        # Column labels
        for c in range(8):
            tk.Label(board, text=str(c+1)).grid(row=0, column=c+1)
            tk.Label(board, text=str(c+1)).grid(row=9, column=c+1)

        # Buttons for each square
        self.buttons = {}
        self.queen_in_row = {}
        self.placed = 0
        self.moves = 0
        colors = {True: '#F3EFE0', False: '#7C9A6D'}
        for r in range(8):
            tk.Label(board, text=str(8-r)).grid(row=r+1, column=0)
            tk.Label(board, text=str(8-r)).grid(row=r+1, column=9)
            for c in range(8):
                btn = tk.Button(board,
                                bg=colors[((r+c)%2)==0],
                                image='' if not self.queen_img else None,
                                compound='center',
                                command=lambda r=r, c=c: self.toggle_queen(r, c))
                btn.grid(row=r+1, column=c+1, sticky='nsew')
                self.buttons[(r, c)] = btn

        # ─── Status bar ─────────────────────────────────────
        status = tk.Frame(self.root)
        status.place(relx=0.5, rely=0.95, anchor='s')
        if self.queen_img:
            tk.Label(status, image=self.queen_img).pack(side='left')
        tk.Label(status, text=' left:', font=("Arial", 12)).pack(side='left')
        self.ql_var = tk.IntVar(value=8)
        tk.Label(status, textvariable=self.ql_var, font=("Arial", 12)).pack(side='left', padx=(2,20))
        tk.Label(status, text='Moves:', font=("Arial", 12)).pack(side='left')
        self.mv_var = tk.IntVar(value=0)
        tk.Label(status, textvariable=self.mv_var, font=("Arial", 12)).pack(side='left', padx=(2,20))
        tk.Button(status, text='Submit', command=self.submit_solution).pack(side='left', padx=5)
        tk.Button(status, text='Reset Board', command=self.reset_board).pack(side='left', padx=5)

        self.root.mainloop()

    def set_name(self):
        """Validate and lock in the player's name."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror('Invalid', 'Name cannot be empty.', parent=self.root)
            return
        self.player_name = name
        self.name_entry.config(state='disabled')
        self.name_ok.config(state='disabled')
        self.root.title(f"Eight Queens Puzzle — {name}")
        self.name_set = True

    def toggle_queen(self, r, c):
        """
        Place or remove a queen at (r,c), enforcing:
          - max one per row
          - max one per column
          - no diagonal attacks
        """
        btn = self.buttons[(r, c)]
        # Remove existing queen
        if self.queen_in_row.get(r) == c:
            btn.config(image='')
            del self.queen_in_row[r]
            self.placed -= 1
        else:
            # Enforce placement rules
            if self.placed >= 8:
                messagebox.showerror('Limit Reached',
                                     'Cannot place more than 8 queens.',
                                     parent=self.root)
                return
            if r in self.queen_in_row:
                messagebox.showerror('Invalid',
                                     'Only one queen per row.',
                                     parent=self.root)
                return
            if c in self.queen_in_row.values():
                messagebox.showerror('Invalid',
                                     'Only one queen per column.',
                                     parent=self.root)
                return
            for r2, c2 in self.queen_in_row.items():
                if abs(r - r2) == abs(c - c2):
                    messagebox.showerror('Invalid',
                                         'Queens cannot attack diagonally.',
                                         parent=self.root)
                    return
            # Place queen
            if self.queen_img:
                btn.config(image=self.queen_img)
            self.queen_in_row[r] = c
            self.placed += 1

        # Update move/queen counters
        self.moves += 1
        self.ql_var.set(8 - self.placed)
        self.mv_var.set(self.moves)

    def reset_board(self):
        """Clear all queens and reset counters."""
        for btn in self.buttons.values():
            btn.config(image='')
        self.queen_in_row.clear()
        self.placed = self.moves = 0
        self.ql_var.set(8)
        self.mv_var.set(0)

    def run_generate(self):
        """Regenerate & store solutions on demand for the selected mode."""
        if not self.name_set:
            messagebox.showerror('Missing Name',
                                 'Enter your name first.',
                                 parent=self.root)
            return
        mode = self.mode_var.get()
        try:
            sols, dur = (self.solver.find_sequential()
                         if mode == 'Sequential'
                         else self.solver.find_threaded())
            for s in sols:
                self.db.save_solution(s, mode)
            self.db.record_performance(mode, dur)
            messagebox.showinfo('Done',
                                f"{mode}: {len(sols)} solutions in {dur:.4f}s",
                                parent=self.root)
        except Exception as e:
            messagebox.showerror('Error',
                                 f"Failed to generate/store solutions: {e}",
                                 parent=self.root)

    def submit_solution(self):
        """Submit the current board as a candidate solution."""
        if not self.name_set:
            messagebox.showerror('Missing Name',
                                 'Enter your name first.',
                                 parent=self.root)
            return
        if self.placed != 8:
            messagebox.showerror('Incomplete',
                                 'Place all 8 queens before submitting.',
                                 parent=self.root)
            return
        # Build "(row,col)" list
        pairs = [f"({r+1},{self.queen_in_row[r]+1})"
                 for r in sorted(self.queen_in_row)]
        pos_str = ",".join(pairs)
        ok, msg = self.db.mark_found(pos_str,
                                     self.player_name,
                                     self.mode_var.get())
        messagebox.showinfo('Result', msg, parent=self.root)
        # Clear board for next attempt
        self.reset_board()

    def compare_performance(self):
        """Fetch recorded timings and indicate which mode is faster."""
        try:
            perf = self.db.get_performance()
        except Exception as e:
            messagebox.showerror('Error',
                                 f"Could not retrieve performance data: {e}",
                                 parent=self.root)
            return
        if not perf:
            messagebox.showinfo('No Data',
                                'No performance data found.',
                                parent=self.root)
            return
        times = {}
        for mode, dur in perf:
            times.setdefault(mode, []).append(dur)
        seq_time = min(times.get('Sequential', [float('inf')]))
        thr_time = min(times.get('Threaded',   [float('inf')]))
        if seq_time < thr_time:
            winner, w_time, l_time = 'Sequential', seq_time, thr_time
        else:
            winner, w_time, l_time = 'Threaded', thr_time, seq_time
        messagebox.showinfo(
            'Performance Comparison',
            f"{winner} mode is faster: {w_time:.4f}s vs {l_time:.4f}s",
            parent=self.root
        )

# ───── Unit Tests & Launch ─────────────────────────────────────────────
class TestEightQueens(unittest.TestCase):
    """Unit tests for both solver methods."""
    def setUp(self):
        self.solver = EightQueensSolver()

    def test_sequential_count(self):
        sols, _ = self.solver.find_sequential()
        self.assertEqual(len(sols), 92,
                         "Sequential solver must find 92 unique solutions.")

    def test_threaded_count(self):
        sols, _ = self.solver.find_threaded()
        self.assertEqual(len(sols), 92,
                         "Threaded solver must find 92 unique solutions.")

    def test_threaded_no_duplicates(self):
        sols, _ = self.solver.find_threaded()
        self.assertEqual(len(sols), len(set(sols)),
                         "Threaded solver must produce no duplicate solutions.")

if __name__ == '__main__':
    # Run unit tests, then launch the UI
    unittest.main(exit=False)
    EightQueensUI(EightQueensSolver(), DBManager())
