from tic_tac_toe_funcs import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk


class TicTacGame:

    def __init__(self):
        self.size = 500
        self.square_num = 3
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.geometry("{size}x{size}".format(size=self.size))
        self.root.title("tic tac toe")

        self.levels = ["level : low",  "level : medium",
                       "level : high"]
        self.level  = tk.StringVar()
        self.cpu_strength = 0 # depth=[0,1,3]
        self.list = ttk.Combobox(self.root, values=self.levels,
                                 textvariable=self.level, height=1,
                                 state="readonly", width=15)
        self.list.current(0)
        self.depth = self._get_depth()
        self.list.bind("<<ComboboxSelected>>", lambda e:self._combo_selected())
        self.list.pack()
        
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.pack()

        self.human = Human(Board.circle)
        self.human.name = "あなた"
        self.cpu   = Cpu(Board.cross)
        self.board = Board(self.square_num, self.square_num)
        self.turn  = 1

        self.margin = self.size // 10
        self.square_size = (self.size - self.margin*2) // self.square_num
        self.repaint()
        
    def _get_depth(self):
        lv_txt = self.level.get()
        index = self.levels.index(lv_txt)
        depths = [1, 3, 5]
        return depths[index]

    def _combo_selected(self):
        self.depth = self._get_depth()
        self.root.focus() # reset focus in listbox
    
    def play(self):
        self.root.deiconify()
        self.root.mainloop()

    def click(self, event):
        result = "ゲーム結果"
        draw   = "引き分け"
        win    = "{}の勝ち"
        gameset = False
        
        def is_correct_index(x, y):
            return x >= 0 and y >= 0 and x < self.square_num and y < self.square_num
        
        def put_player(x, y):
            self.board.put(x, y, Board.circle)
            self.repaint()
            if self.board.is_won(self.human.mark):
                messagebox.showinfo(result, win.format(self.human.name))
                self.board.reset()
                self.repaint()
                nonlocal gameset; gameset = True
                return
            self.repaint()
            
            if not self.board.can_put():
                messagebox.showinfo(result, draw)
                self.board.reset()                
                self.repaint()
                gameset = True

        def put_cpu(x, y):
            if gameset:return
            
            if not self.board.can_put():
                messagebox.showinfo(result, draw)
                self.board.reset()
                return

            self.cpu.set_depth(self.depth)
            self.cpu.put(self.board)

            if self.board.is_won(self.cpu.mark):
                self.repaint()
                messagebox.showinfo(result, win.format(self.cpu.name))
                self.board.reset()
                self.repaint()
                return
            
            if not self.board.can_put():
                messagebox.showinfo(result, draw)
                self.board.reset()
                
            self.repaint()
            
            
        x = (event.x - self.margin) // self.square_size
        y = (event.y - self.margin) // self.square_size
        if not is_correct_index(x, y):
            return
        if [x, y] not in self.board.get_canputs():return

        put_player(x, y)
        put_cpu(x, y)
        
    def repaint(self):
        cv = self.canvas
        cv.delete('all')        
        margin = self.margin
        square_size = ((self.size - self.margin*2) / self.square_num)
        p_size = 5
        p_color= "white"
        l_size = 3
        l_color= ""
        b_color= "#12FF90"

        w1, h1 = margin, margin
        w2, h2 = self.size - margin, self.size-margin
        cv.create_rectangle(w1, h1, w2, h2, fill=b_color, width=0)

        bar_num = int((self.size - (self.margin*2)) / square_size) +1
        for i in range(bar_num):
            x1 = margin
            x2 = self.size - margin
            y  = i * square_size + margin
            cv.create_line(x1, y, x2, y, width=l_size)
        for i in range(bar_num):
            x1 = margin
            x2 = self.size - margin
            y  = i * square_size + margin
            cv.create_line(y, x1, y, x2, width=l_size)
        board = self.board.get()
        for h, row in enumerate(board):
            y1 = margin + h * square_size + square_size//4
            y2 = y1 + square_size//2
            for w, elm in enumerate(row):
                x1 = margin + w * square_size + square_size//4
                x2 = x1 + square_size//2
                if elm == Board.circle:
                    cv.create_oval(x1, y1, x2, y2, width=p_size, outline=p_color)
                elif elm == Board.cross:
                    cv.create_line(x1, y1, x2, y2, width=p_size, fill=p_color)
                    cv.create_line(x1+square_size//2, y1, x2-square_size//2, y2,
                                   width=p_size, fill=p_color)


if __name__ == "__main__":
    TicTacGame().play()
