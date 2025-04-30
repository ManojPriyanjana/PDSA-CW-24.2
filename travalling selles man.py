try:
    import tkinter as tk
    from tkinter import messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

import random
import time
import mysql.connector
from mysql.connector import Error
from itertools import permutations, combinations
import unittest
import sys

"""
Algorithm Complexity:
- Greedy Nearest Neighbor: O(n^2)
- Dynamic Programming (Held-Karp): O(n^2 * 2^n)
- Brute Force (Permutation): O(n!)
"""

def tsp_greedy(dist_matrix, cities, start):
    visited = [start]
    unvisited = set(cities) - {start}
    current = start
    total = 0
    while unvisited:
        next_city = min(unvisited, key=lambda c: dist_matrix[current][c])
        total += dist_matrix[current][next_city]
        visited.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    total += dist_matrix[current][start]
    visited.append(start)
    return visited, total

def tsp_bruteforce(dist_matrix, cities, start):
    best_cost = float('inf')
    best_path = []
    others = list(cities - {start})
    for perm in permutations(others):
        path = [start] + list(perm) + [start]
        cost = sum(dist_matrix[path[i]][path[i+1]] for i in range(len(path)-1))
        if cost < best_cost:
            best_cost = cost
            best_path = path
    return best_path, best_cost

def tsp_dynamic(dist_matrix, cities, start):
    nodes = [start] + [c for c in cities if c != start]
    n = len(nodes)
    C = {}
    # Initialize base cases
    for k in range(1, n):
        C[(1 << k, k)] = (dist_matrix[start][nodes[k]], 0)
    # Build up solutions for larger subsets
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            mask = sum(1 << bit for bit in subset)
            for k in subset:
                prev_mask = mask & ~(1 << k)
                candidates = []
                for m in subset:
                    if m != k and (prev_mask, m) in C:
                        prev_cost, _ = C[(prev_mask, m)]
                        cost = prev_cost + dist_matrix[nodes[m]][nodes[k]]
                        candidates.append((cost, m))
                if candidates:
                    C[(mask, k)] = min(candidates)
    # Close the tour
    full_mask = (1 << n) - 2
    candidates = []
    for k in range(1, n):
        if (full_mask, k) in C:
            cost, prev = C[(full_mask, k)]
            candidates.append((cost + dist_matrix[nodes[k]][start], k))
    opt_cost, parent = min(candidates)
    # Reconstruct path
    path = [start]
    mask = full_mask
    last = parent
    for _ in range(n-1):
        path.append(nodes[last])
        mask, last = mask & ~(1 << last), C[(mask, last)][1]
    path.append(start)
    return path, opt_cost

if GUI_AVAILABLE:
    class TSPApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Traveling Salesman Game")
            self.geometry("1200x700+0+0")
            self._init_db()

            self.left_container = tk.Frame(self)
            self.left_container.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            self.right_container = tk.Frame(self)
            self.right_container.pack(side="right", fill="y", padx=10, pady=10)

            # Build UI panels
            self._build_matrix_frame(self.left_container)
            self._build_answer_frame(self.left_container)
            self._build_controls(self.right_container)

        def _init_db(self):
            db_name = 'tsp_game_db'
            try:
                conn = mysql.connector.connect(host='localhost', user='root', password='root')
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                cursor.execute(f"USE {db_name}")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS game_records (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        player_name VARCHAR(100),
                        home_city CHAR(1),
                        selected_cities VARCHAR(255),
                        algorithm VARCHAR(50),
                        path VARCHAR(255),
                        distance INT,
                        time_taken FLOAT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                self.conn = conn
            except Error as err:
                messagebox.showerror("Database Error", f"Error initializing database:\n{err}")
                self.conn = None

        def _build_matrix_frame(self, parent):
            keys = list("ABCDEFGHIJ")
            N = len(keys)
            self.city_keys = keys
            self.dist_matrix = {c: {} for c in keys}

            frame = tk.Frame(parent, borderwidth=1, relief="solid")
            self.matrix_frame = frame

            # Always insert matrix_frame *before* the answer_frame if it exists
            if hasattr(self, 'answer_frame'):
                frame.pack(side="top", fill="both", expand=True, before=self.answer_frame, padx=2, pady=2)
            else:
                frame.pack(side="top", fill="both", expand=True, padx=2, pady=2)

            # Configure grid
            for i in range(N+1):
                frame.grid_rowconfigure(i, weight=1, uniform="row")
                frame.grid_columnconfigure(i, weight=1, uniform="col")

            # Header row/column
            tk.Label(frame, text="", borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")
            for j, k in enumerate(keys):
                tk.Label(frame, text=f"City {k}", borderwidth=1, relief="solid")\
                    .grid(row=0, column=j+1, sticky="nsew")
                tk.Label(frame, text=f"City {k}", borderwidth=1, relief="solid")\
                    .grid(row=j+1, column=0, sticky="nsew")

            # Fill distances
            for i, ci in enumerate(keys):
                for j, cj in enumerate(keys):
                    if i == j:
                        self.dist_matrix[ci][ci] = 0
                        lbl = tk.Label(frame, bg="teal", borderwidth=1, relief="solid")
                    elif j < i:
                        val = random.randint(50, 100)
                        self.dist_matrix[ci][cj] = val
                        self.dist_matrix[cj][ci] = val
                        lbl = tk.Label(frame, text=str(val), borderwidth=1, relief="solid")
                    else:
                        lbl = tk.Label(frame, text="", borderwidth=1, relief="solid")
                    lbl.grid(row=i+1, column=j+1, sticky="nsew")

        def _build_answer_frame(self, parent):
            frame = tk.LabelFrame(parent, text="Correct answer", padx=10, pady=10)
            self.answer_frame = frame
            frame.pack(side="top", fill="x", pady=(10,0))

            tk.Label(frame, text="Correct shortest path:").grid(row=0, column=0, sticky="w")
            self.correct_entries = []
            row0 = tk.Frame(frame)
            row0.grid(row=0, column=1, sticky="w")
            for _ in range(12):
                e = tk.Entry(row0, width=3, justify="center")
                e.pack(side="left", padx=2)
                self.correct_entries.append(e)

            tk.Label(frame, text="Total Distance:").grid(row=1, column=0, sticky="w", pady=(5,0))
            self.total_dist_entry = tk.Entry(frame, width=10)
            self.total_dist_entry.grid(row=1, column=1, sticky="w", pady=(5,0))

            self.summary_lbl = tk.Label(frame, text="You have selected <algo> and it took <time> to finish")
            self.summary_lbl.grid(row=2, column=0, columnspan=2, sticky="w", pady=(5,0))

        def _build_controls(self, parent):
            # Player name
            nf = tk.Frame(parent)
            nf.pack(fill="x", pady=(0,10))
            tk.Label(nf, text="Player Name:").pack(side="left")
            self.name_entry = tk.Entry(nf)
            self.name_entry.pack(side="left", padx=5)

            # Home city display
            hf = tk.LabelFrame(parent, text="We've randomly selected your home city:")
            hf.pack(fill="x", pady=(0,10))
            self.home_city = random.choice(self.city_keys)
            self.home_label = tk.Label(hf, text=self.home_city, font=(None,16,"bold"))
            self.home_label.pack(padx=10, pady=5)

            # City-selection buttons
            vf = tk.LabelFrame(parent, text="Select the cities to visit (click):")
            vf.pack(fill="x", pady=(0,10))
            self.visit_buttons, self.selected_cities = {}, set()
            row = tk.Frame(vf)
            row.pack(padx=5, pady=5)
            for c in self.city_keys:
                btn = tk.Button(row, text=c, width=3, command=lambda c=c: self._toggle_city(c))
                btn.pack(side="left", padx=2)
                self.visit_buttons[c] = btn

            # Algorithm choice
            af = tk.LabelFrame(parent, text="Select your preferred algorithm:")
            af.pack(fill="x", pady=(0,10))
            self.algo_var = tk.StringVar(value="Greedy")
            for name in ("Greedy","Dynamic Programming","Brute Force"):
                tk.Radiobutton(af, text=name, variable=self.algo_var, value=name)\
                  .pack(anchor="w", padx=10)

            # Guess-your-path entries
            gf = tk.LabelFrame(parent, text="Guess the shortest path (left→right):")
            gf.pack(fill="x", pady=(0,10))
            self.guess_entries = []
            row2 = tk.Frame(gf)
            row2.pack(padx=5, pady=5)
            for _ in range(12):
                e = tk.Entry(row2, width=3, justify="center")
                e.pack(side="left", padx=2)
                self.guess_entries.append(e)

            self.result_lbl = tk.Label(gf, text="If correct, this will turn green; else red.")
            self.result_lbl.pack(padx=5, pady=(5,0))

            # Start / Reset buttons
            bf = tk.Frame(parent)
            bf.pack(fill="x", pady=(20,0))
            tk.Button(bf, text="Start", bg="lime", command=self._on_start).pack(side="left", padx=5)
            tk.Button(bf, text="Reset", bg="tomato", command=self._on_reset).pack(side="left", padx=5)

        def _toggle_city(self, city):
            btn = self.visit_buttons[city]
            if city in self.selected_cities:
                self.selected_cities.remove(city)
                btn.config(relief="raised")
            else:
                self.selected_cities.add(city)
                btn.config(relief="sunken")

        def _on_start(self):
            player = self.name_entry.get().strip()
            if not player:
                messagebox.showwarning("Input Error", "Please enter your name.")
                return
            if not self.selected_cities:
                messagebox.showwarning("Input Error", "Select at least one city to visit.")
                return

            cities = set(self.selected_cities) | {self.home_city}
            algo = self.algo_var.get()
            t0 = time.perf_counter()

            try:
                if algo == "Greedy":
                    path, dist = tsp_greedy(self.dist_matrix, cities, self.home_city)
                elif algo == "Dynamic Programming":
                    path, dist = tsp_dynamic(self.dist_matrix, cities, self.home_city)
                else:
                    path, dist = tsp_bruteforce(self.dist_matrix, cities, self.home_city)
            except Exception as e:
                messagebox.showerror("Algorithm Error", f"Error in {algo}: {e}")
                return

            elapsed = time.perf_counter() - t0

            # Show correct answer
            for i, e in enumerate(self.correct_entries):
                e.delete(0, tk.END)
                if i < len(path):
                    e.insert(0, path[i])
            self.total_dist_entry.delete(0, tk.END)
            self.total_dist_entry.insert(0, str(dist))
            self.summary_lbl.config(text=f"You have selected {algo} and it took {elapsed:.4f}s to finish")

            # Check user guess
            guess = [e.get().strip().upper() for e in self.guess_entries]
            gfilt = [g for g in guess if g]
            correct = gfilt == path
            self.result_lbl.config(text="Correct!" if correct else "Incorrect!",
                                   fg="green" if correct else "red")

            # Save to DB
            if self.conn:
                try:
                    cur = self.conn.cursor()
                    sel = ",".join(sorted(self.selected_cities))
                    pstr = "-".join(path)
                    cur.execute(
                        "INSERT INTO game_records "
                        "(player_name,home_city,selected_cities,algorithm,path,distance,time_taken) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (player, self.home_city, sel, algo, pstr, dist, elapsed)
                    )
                    self.conn.commit()
                except Error as e:
                    messagebox.showerror("Database Error", f"Failed to save record: {e}")

        def _on_reset(self):
            # Clear inputs
            self.name_entry.delete(0, tk.END)
            for btn in self.visit_buttons.values():
                btn.config(relief="raised")
            self.selected_cities.clear()
            for e in self.guess_entries + self.correct_entries:
                e.delete(0, tk.END)
            self.total_dist_entry.delete(0, tk.END)
            self.result_lbl.config(text="If correct, this will turn green; else red.", fg="black")
            self.summary_lbl.config(text="You have selected <algo> and it took <time> to finish")

            # New home city
            self.home_city = random.choice(self.city_keys)
            self.home_label.config(text=self.home_city)

            # Rebuild distance matrix *in place* so it stays above the answer frame
            self.matrix_frame.destroy()
            self._build_matrix_frame(self.left_container)

# Unit tests
class TestTSPAlgorithms(unittest.TestCase):
    def setUp(self):
        self.dist = {
            'A': {'A':0,'B':1,'C':5,'D':2},
            'B': {'A':1,'B':0,'C':4,'D':3},
            'C': {'A':5,'B':4,'C':0,'D':6},
            'D': {'A':2,'B':3,'C':6,'D':0}
        }
        self.cities = {'A','B','C','D'}
        self.start = 'A'

    def test_greedy(self):
        path, cost = tsp_greedy(self.dist, self.cities, self.start)
        self.assertEqual(cost, 15)
        self.assertEqual(path, ['A','B','D','C','A'])

    def test_bruteforce(self):
        path, cost = tsp_bruteforce(self.dist, self.cities, self.start)
        self.assertEqual(cost, 15)

    def test_dynamic(self):
        path, cost = tsp_dynamic(self.dist, self.cities, self.start)
        self.assertEqual(cost, 15)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=sys.argv[:1])
    else:
        if not GUI_AVAILABLE:
            print("Error: tkinter module is not available. Install tkinter and retry.")
            sys.exit(1)
        app = TSPApp()
        app.mainloop()
