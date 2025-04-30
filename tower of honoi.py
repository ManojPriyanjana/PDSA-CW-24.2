import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import time
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import traceback
import sys
import unittest

# ─── 3-Peg Algorithms ───────────────────────────────────────────────
def recursive_hanoi(n, src, aux, dst, moves):
    if n == 0:
        return
    recursive_hanoi(n-1, src, dst, aux, moves)
    moves.append((src, dst))
    recursive_hanoi(n-1, aux, src, dst, moves)

def iterative_hanoi(n, src, aux, dst):
    moves = []
    stack = [(n, src, aux, dst, False)]
    while stack:
        cn, csrc, caux, cdst, processed = stack.pop()
        if cn == 0:
            continue
        if not processed:
            stack.append((cn-1, caux, csrc, cdst, False))
            stack.append((1, csrc, caux, cdst, True))
            stack.append((cn-1, csrc, cdst, caux, False))
        else:
            moves.append((csrc, cdst))
    return moves

# ─── 4-Peg Frame–Stewart Algorithms ────────────────────────────────
def frame_stewart_recursive(n, src, aux1, aux2, dst, moves):
    if n == 0:
        return
    if n == 1:
        moves.append((src, dst))
        return
    frame_stewart_recursive(n-1, src, aux2, dst, aux1, moves)
    moves.append((src, dst))
    frame_stewart_recursive(n-1, aux1, src, aux2, dst, moves)

def frame_stewart_iterative(n, src, aux1, aux2, dst):
    moves = []
    stack = [(n, src, aux1, aux2, dst, False)]
    while stack:
        cn, csrc, caux1, caux2, cdst, done = stack.pop()
        if cn == 0:
            continue
        if cn == 1:
            moves.append((csrc, cdst))
            continue
        if not done:
            stack.append((cn-1, caux1, csrc, caux2, cdst, False))
            stack.append((1, csrc, caux1, caux2, cdst, True))
            stack.append((cn-1, csrc, caux2, cdst, caux1, False))
        else:
            moves.append((csrc, cdst))
    return moves

# ─── GUI Application ───────────────────────────────────────────────
class HanoiUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tower of Hanoi")
        self.geometry("1200x900+0+0")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # --- MySQL setup with exception handling ---
        try:
            self.db = mysql.connector.connect(
                host="localhost", user="root", password="root"
            )
            self.cursor = self.db.cursor()
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS hanoi_stats")
            self.db.database = 'hanoi_stats'
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS algorithm_times (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME,
                    game_type VARCHAR(10),
                    algorithm VARCHAR(20),
                    disks INT,
                    duration DOUBLE
                ) ENGINE=InnoDB;
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_solutions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME,
                    player_name VARCHAR(100),
                    game_type VARCHAR(10),
                    moves INT,
                    sequence TEXT
                ) ENGINE=InnoDB;
            """)
            self.db.commit()
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to initialize DB:\n{e}")
            self.destroy()
            return

        # --- State & dimensions ---
        self.name_entered     = False
        self.n_disks          = random.randint(5, 10)
        self.disk_height      = 20
        self.left_move_count  = 0
        self.right_move_count = 0
        self.left_start_time  = None
        self.right_start_time = None
        self.left_user_moves  = []
        self.right_user_moves = []

        # store canvas dims for reset
        self.tw, self.th = 600, 400
        full_w, full_h = 1200, 900
        ctrl_h = 50

        # --- Control panel ---
        ctrl = tk.Frame(self, bg="#f0f0f0")
        ctrl.place(x=0, y=0, width=full_w, height=ctrl_h)
        tk.Button(ctrl, text="Reset", font=("Helvetica",12),
                  command=self.reset_game).pack(side=tk.LEFT, padx=10)
        tk.Label(ctrl, text="Player Name:", font=("Helvetica",12),
                 bg="#f0f0f0").pack(side=tk.LEFT)
        self.player_name_var = tk.StringVar()
        tk.Entry(ctrl, textvariable=self.player_name_var,
                 font=("Helvetica",12), width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="OK", font=("Helvetica",12),
                  command=self.on_name_submit).pack(side=tk.LEFT)

        # --- Towers & Canvases ---
        offset_y = ctrl_h
        self.left_tower  = self._create_canvas(0,           offset_y, "Classic 3-Peg",    3)
        self.right_tower = self._create_canvas(full_w//2,   offset_y, "Frame–Stewart 4-Peg",4)

        self.left_pos  = self._draw_pegs(self.left_tower,  self.tw, self.th, 3)
        self.right_pos = self._draw_pegs(self.right_tower, self.tw, self.th, 4)

        self.left_pegs  = [[] for _ in range(3)]
        self.right_pegs = [[] for _ in range(4)]
        self._draw_disks(self.left_tower,  self.tw, self.th, 3, self.left_pegs)
        self._draw_disks(self.right_tower, self.tw, self.th, 4, self.right_pegs)

        # --- Info & Solutions ---
        info_y = offset_y + self.th
        left_info = tk.Frame(self, bg="#f0f0f0")
        left_info.place(x=0, y=info_y, width=full_w//2, height=30)
        self.left_move_label = tk.Label(left_info, text="Moves: 0",
                                        font=("Helvetica",12), bg="#f0f0f0")
        self.left_move_label.pack(side=tk.LEFT, padx=10)
        self.left_time_label = tk.Label(left_info, text="Time: 0s",
                                        font=("Helvetica",12), bg="#f0f0f0")
        self.left_time_label.pack(side=tk.LEFT, padx=10)
        self.sol3_text = scrolledtext.ScrolledText(self, width=60,
                                                   height=6, font=("Helvetica",10))
        self.sol3_text.place(x=0, y=info_y+30)

        right_info = tk.Frame(self, bg="#f0f0f0")
        right_info.place(x=full_w//2, y=info_y, width=full_w//2, height=30)
        self.right_move_label = tk.Label(right_info, text="Moves: 0",
                                         font=("Helvetica",12), bg="#f0f0f0")
        self.right_move_label.pack(side=tk.LEFT, padx=10)
        self.right_time_label = tk.Label(right_info, text="Time: 0s",
                                         font=("Helvetica",12), bg="#f0f0f0")
        self.right_time_label.pack(side=tk.LEFT, padx=10)
        self.sol4_text = scrolledtext.ScrolledText(self, width=60,
                                                   height=6, font=("Helvetica",10))
        self.sol4_text.place(x=full_w//2, y=info_y+30)

        # --- Drag/drop bindings ---
        self.drag = {"item": None}
        for cv in (self.left_tower, self.right_tower):
            cv.bind('<ButtonPress-1>',    self.on_press)
            cv.bind('<B1-Motion>',        self.on_move)
            cv.bind('<ButtonRelease-1>',  self.on_release)

        self.after(1000, self.update_timers)

    # ─── UI Helpers ──────────────────────────────────────────────────
    def _create_canvas(self, x, y, title, peg_count):
        c = tk.Canvas(self, width=self.tw, height=self.th, bg="#ffffff",
                      highlightthickness=1, highlightbackground="#cccccc")
        c.place(x=x, y=y)
        c.create_text(self.tw//2, 20, text=title, font=("Helvetica",18,"bold"))
        return c

    def _draw_pegs(self, cv, w, h, count):
        base = h - 40
        cv.create_rectangle(20, base, w-20, base+20, fill="#0000CC", outline="")
        positions = []
        for i in range(count):
            x = (i+1)*w/(count+1)
            positions.append(x)
            cv.create_rectangle(x-5, base-0.6*h, x+5, base,
                                fill="#888888", outline="")
            cv.create_text(x, base-0.6*h-20,
                           text=chr(ord('A')+i),
                           font=("Helvetica",16,"bold"))
        return positions

    def _draw_disks(self, cv, w, h, count, stacks):
        base = h - 40
        max_w = w/(count+1)*0.8
        min_w = max_w*0.3
        colors = ["#FFD700","#FF8C00","#00BFFF","#ADFF2F",
                  "#FF69B4","#BA55D3","#7FFFD4","#FFE4B5",
                  "#AFEEEE","#D3D3D3"]
        positions = (self.left_pos if cv is self.left_tower
                                 else self.right_pos)
        for i in range(self.n_disks):
            frac = (self.n_disks - i)/self.n_disks
            disk_w = min_w + (max_w - min_w)*frac
            x0 = positions[0] - disk_w/2
            x1 = positions[0] + disk_w/2
            y1 = base - self.disk_height*(i+1)
            y0 = y1 - self.disk_height
            disk = cv.create_rectangle(x0, y0, x1, y1,
                                       fill=colors[i%len(colors)],
                                       outline="black",
                                       tags=("disk",))
            stacks[0].append(disk)

    def on_name_submit(self):
        name = self.player_name_var.get().strip()
        if not name:
            messagebox.showwarning("Name Required",
                                   "Please enter your name before playing.")
            return
        self.name_entered = True
        self.title(f"Tower of Hanoi – Player: {name}")

    def reset_game(self):
        # reset state
        self.name_entered     = False
        self.player_name_var.set("")
        self.title("Tower of Hanoi")
        self.n_disks          = random.randint(5, 10)
        self.left_move_count  = self.right_move_count = 0
        self.left_start_time  = self.right_start_time = None
        self.left_time_label.config(text="Time: 0s")
        self.right_time_label.config(text="Time: 0s")
        self.left_move_label.config(text="Moves: 0")
        self.right_move_label.config(text="Moves: 0")
        self.left_user_moves  = []
        self.right_user_moves = []

        # clear disks and rebuild pegs
        for cv in (self.left_tower, self.right_tower):
            cv.delete("disk")
        self.left_pegs  = [[] for _ in self.left_pos]
        self.right_pegs = [[] for _ in self.right_pos]
        self._draw_disks(self.left_tower,  self.tw, self.th, 3, self.left_pegs)
        self._draw_disks(self.right_tower, self.tw, self.th, 4, self.right_pegs)

        # clear solution texts
        self.sol3_text.delete('1.0', tk.END)
        self.sol4_text.delete('1.0', tk.END)

    def update_timers(self):
        now = time.time()
        if self.left_start_time:
            self.left_time_label.config(
                text=f"Time: {int(now - self.left_start_time)}s"
            )
        if self.right_start_time:
            self.right_time_label.config(
                text=f"Time: {int(now - self.right_start_time)}s"
            )
        self.after(1000, self.update_timers)

    # ─── Drag & Drop ─────────────────────────────────────────────────
    def on_press(self, event):
        if not self.name_entered:
            messagebox.showwarning("Name Required",
                                   "Please enter your name before playing.")
            return
        cv = event.widget
        clicked = cv.find_overlapping(event.x, event.y,
                                      event.x, event.y)
        for item in reversed(clicked):
            if "disk" in cv.gettags(item):
                pegs = (self.left_pegs
                         if cv is self.left_tower
                         else self.right_pegs)
                for idx, stack in enumerate(pegs):
                    if stack and stack[-1] == item:
                        self.drag = {"item": item,
                                     "x": event.x,
                                     "y": event.y,
                                     "orig": idx,
                                     "cv": cv}
                        return
        self.drag = {"item": None}

    def on_move(self, event):
        d = self.drag; item = d.get("item")
        if item:
            cv = d["cv"]
            cv.move(item, event.x - d["x"], event.y - d["y"])
            d["x"], d["y"] = event.x, event.y

    def on_release(self, event):
        d = self.drag; item = d.get("item")
        if not item:
            return
        try:
            src = d["cv"]
            tgt = (event.widget
                   if event.widget in (self.left_tower,
                                       self.right_tower)
                   else src)
            is_left_src = (src is self.left_tower)
            is_left_tgt = (tgt is self.left_tower)
            src_pegs = (self.left_pegs
                         if is_left_src else self.right_pegs)
            tgt_pegs = (self.left_pegs
                         if is_left_tgt else self.right_pegs)
            tgt_pos = (self.left_pos
                        if is_left_tgt else self.right_pos)
            orig = d["orig"]

            coords = src.coords(item)
            w = coords[2] - coords[0]
            base = tgt.winfo_height() - 40
            target_idx = min(
                range(len(tgt_pos)),
                key=lambda i: abs(event.x - tgt_pos[i])
            )
            top = (tgt_pegs[target_idx][-1]
                    if tgt_pegs[target_idx] else None)
            top_w = ((tgt.coords(top)[2] - tgt.coords(top)[0])
                      if top else None)

            valid = (not tgt_pegs[target_idx] or
                     (top_w and top_w > w))
            if valid:
                # start timers & record move
                if is_left_src:
                    if not self.left_start_time:
                        self.left_start_time = time.time()
                    self.left_move_count += 1
                    self.left_move_label.config(
                        text=f"Moves: {self.left_move_count}"
                    )
                    self.left_user_moves.append(
                        f"{chr(ord('A')+orig)}->"
                        f"{chr(ord('A')+target_idx)}"
                    )
                else:
                    if not self.right_start_time:
                        self.right_start_time = time.time()
                    self.right_move_count += 1
                    self.right_move_label.config(
                        text=f"Moves: {self.right_move_count}"
                    )
                    self.right_user_moves.append(
                        f"{chr(ord('A')+orig)}->"
                        f"{chr(ord('A')+target_idx)}"
                    )

                # perform move
                fill = src.itemcget(item,'fill')
                src.delete(item)
                src_pegs[orig].pop()
                x0 = tgt_pos[target_idx] - w/2
                x1 = tgt_pos[target_idx] + w/2
                y1 = base - self.disk_height*(len(tgt_pegs[target_idx])+1)
                y0 = y1 - self.disk_height
                new_item = tgt.create_rectangle(
                    x0,y0,x1,y1,
                    fill=fill, outline="black", tags=("disk",)
                )
                tgt_pegs[target_idx].append(new_item)

                # check win
                if tgt is self.left_tower and target_idx==2 \
                   and len(self.left_pegs[2])==self.n_disks:
                    self._on_win('3')
                if tgt is self.right_tower and target_idx==3 \
                   and len(self.right_pegs[3])==self.n_disks:
                    self._on_win('4')
            else:
                # invalid → snap back
                px = (self.left_pos if is_left_src else self.right_pos)[orig]
                y1 = src.winfo_height()-40 \
                     - self.disk_height*(len(src_pegs[orig])+1)
                y0 = y1 - self.disk_height
                src.coords(item, px-w/2, y0, px+w/2, y1)

        except Exception as ex:
            traceback.print_exc()
            messagebox.showerror("Error", f"An error occurred:\n{ex}")
        finally:
            self.drag = {"item": None}

    def _on_win(self, side):
        if side=='3':
            elapsed = int(time.time()-self.left_start_time)
            messagebox.showinfo("Win",
                f"You win 3-peg! Moves: {self.left_move_count} Time: {elapsed}s"
            )
            self._save_player_solution('3-peg',
                                       self.left_move_count,
                                       self.left_user_moves)
            self.show_solution('3')
        else:
            elapsed = int(time.time()-self.right_start_time)
            messagebox.showinfo("Win",
                f"You win 4-peg! Moves: {self.right_move_count} Time: {elapsed}s"
            )
            self._save_player_solution('4-peg',
                                       self.right_move_count,
                                       self.right_user_moves)
            self.show_solution('4')

    def _save_player_solution(self, game_type, moves, seq):
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute(
                "INSERT INTO player_solutions "
                "(timestamp, player_name, game_type, moves, sequence) "
                "VALUES (%s,%s,%s,%s,%s)",
                (now, self.player_name_var.get().strip(),
                 game_type, moves, ",".join(seq))
            )
            self.db.commit()
        except Error as e:
            messagebox.showwarning("DB Insert Failed",
                                   f"Could not save solution:\n{e}")

    def show_solution(self, side):
        try:
            if side=='3':
                t0=time.time(); rec3=[]; recursive_hanoi(self.n_disks,'A','B','C',rec3)
                t1=time.time(); itr3=iterative_hanoi(self.n_disks,'A','B','C')
                now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data=[
                    (now,'3-peg','3-recursive',self.n_disks,t1-t0),
                    (now,'3-peg','3-iterative',self.n_disks,time.time()-t1)
                ]
                self.cursor.executemany(
                    "INSERT INTO algorithm_times "
                    "(timestamp,game_type,algorithm,disks,duration) "
                    "VALUES(%s,%s,%s,%s,%s)", data
                )
                self.db.commit()
                self.sol4_text.delete('1.0',tk.END)
                self.sol3_text.delete('1.0',tk.END)
                self.sol3_text.insert(tk.END,
                    f"3-Peg Recursive({len(rec3)}) in {t1-t0:.4f}s: " +
                    ", ".join(f"{s}->{d}" for s,d in rec3)+"\n"
                )
                self.sol3_text.insert(tk.END,
                    f"3-Peg Iterative({len(itr3)}) in {(time.time()-t1):.4f}s: " +
                    ", ".join(f"{s}->{d}" for s,d in itr3)
                )
            else:
                t0=time.time(); rec4=[]; frame_stewart_recursive(
                    self.n_disks,'A','B','C','D',rec4
                )
                t1=time.time(); itr4=frame_stewart_iterative(
                    self.n_disks,'A','B','C','D'
                )
                now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data=[
                    (now,'4-peg','4-recursive',self.n_disks,t1-t0),
                    (now,'4-peg','4-iterative',self.n_disks,time.time()-t1)
                ]
                self.cursor.executemany(
                    "INSERT INTO algorithm_times "
                    "(timestamp,game_type,algorithm,disks,duration) "
                    "VALUES(%s,%s,%s,%s,%s)", data
                )
                self.db.commit()
                self.sol3_text.delete('1.0',tk.END)
                self.sol4_text.delete('1.0',tk.END)
                self.sol4_text.insert(tk.END,
                    f"4-Peg Recursive({len(rec4)}) in {t1-t0:.4f}s: " +
                    ", ".join(f"{s}->{d}" for s,d in rec4)+"\n"
                )
                self.sol4_text.insert(tk.END,
                    f"4-Peg Iterative({len(itr4)}) in {(time.time()-t1):.4f}s: " +
                    ", ".join(f"{s}->{d}" for s,d in itr4)
                )
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to display solution:\n{e}")

# ─── Integrated Unit Tests ───────────────────────────────────────────
class TestHanoiAlgorithms(unittest.TestCase):
    def test_recursive_hanoi_3(self):
        m=[]; recursive_hanoi(3,'A','B','C',m)
        self.assertEqual(len(m),7)
        self.assertEqual(m[0],('A','C'))
    def test_iterative_hanoi_3(self):
        m=iterative_hanoi(3,'A','B','C')
        self.assertEqual(len(m),7)
        self.assertEqual(m[0],('A','C'))
    def test_frame_stewart_recursive_4(self):
        m=[]; frame_stewart_recursive(3,'A','B','C','D',m)
        self.assertEqual(len(m),5)
    def test_frame_stewart_iterative_4(self):
        m=frame_stewart_iterative(3,'A','B','C','D')
        self.assertEqual(len(m),5)

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=='test':
        unittest.main(argv=[sys.argv[0]])
    else:
        try:
            app = HanoiUI()
            app.mainloop()
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Fatal Error", f"Application crashed:\n{e}")
