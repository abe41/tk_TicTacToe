import random
import itertools
import time
import copy


class TicTacToe:
    
    def __init__(self):
        self.players = [Human, Cpu]
        self.first_player  = None
        self.second_player = None
        self.decide_pturn()
        self.board = Board(3, 3)
        self.turn  = 1

    def decide_pturn(self):
        plis = random.sample(self.players, 2)
        self.first_player  = plis[0](Board.circle)
        self.second_player = plis[1](Board.cross)        
    
    def play(self):
        self.turn = 1
        players_ite = itertools.cycle([self.first_player, self.second_player])
        while True:
            p = next(players_ite)
            print("TURN : {turn} {name} {mark}"
                  .format(turn=self.turn, name=p.name, mark=Board.get_mark(p.mark)))
            print(self.board)
            if not self.board.can_put():                
                break
            p.put(self.board)
            if self.board.is_won(p.mark):
                print(self.board)
                self.print_winner(p.name)
                return
            self.turn += 1
            print()
        self.print_draw()

    def print_winner(self, name):
        print(f"winner: {name}")

    def print_draw(self):
        print("draw")
        

class Board:

    empty  =  0
    circle =  1
    cross  = -1
    mark_map = {
        empty  : "-",
        circle : "◯",
        cross  : "×"
        }
    
    def __init__(self, width, height):
        self.board = [[self.empty for i in range(width)]for j in range(height)]
        self.width = width
        self.height = height

    def can_put(self):
        cp = False
        for row in self.board:
            cp  = cp or not(all(row))
        return cp

    def is_won(self, mark):
        exist_line = False
        for y in range(self.height):
            tmp = []
            for x in range(self.width):
                val = self.board[y][x]
                tmp.append(val==mark)
            exist_line = exist_line or all(tmp)
        for x in range(self.height):
            tmp = []
            for y in range(self.width):
                val = self.board[y][x]
                tmp.append(val==mark)
            exist_line = exist_line or all(tmp)
        tmp = []
        for i in range(self.height):
            val = self.board[i][i]
            tmp.append(val==mark)
        exist_line = exist_line or all(tmp)
        tmp = []
        for i in range(self.height-1, -1, -1):
            j = abs( i - (self.height-1) )
            val = self.board[i][j]
            tmp.append(val==mark)
        exist_line = exist_line or all(tmp)
            
        return exist_line

    def is_exist(self, x, y):
        return self.board[y][x] != self.empty

    def get_canputs(self):
        coordinates = []
        for y in range(self.height):
            for x in range(self.width):
                if self.is_exist(x, y): continue
                coordinates.append([x, y])
        return coordinates                  
    
    def put(self, x, y, mark):
        self.board[y][x] = mark

    def __str__(self):
        b = " " + "".join([str(i) for i in range(self.width)]) + "\n"
        for cnt, row in enumerate(self.board):
            b += str(cnt)
            for s in row:
                b += self.mark_map.get(s, s)
            b += "\n"
        return b.rstrip("\n")

    def get(self):
        return self.board

    @classmethod
    def get_mark(cls, mark):
        return cls.mark_map.get(mark, mark)

    def reset(self):
        self.board =  [[self.empty for i in range(self.width)]for j in range(self.height)]

    def count(self):
        cnt =  0
        for row in self.board:
            for elm in row:
                if elm != self.empty:
                    cnt += 1
        return cnt


class Player:

    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

    def put(self, board):
        x, y = self.think(board)
        board.put(x, y, self.mark)

    def think(self, board):
        raise NotImplementedError


class Human(Player):

    def __init__(self, mark):
        super().__init__("Human", mark)

    def think(self, board):
        def get():
            return map(int, input("enter your hand(x y): ").strip().split())
        x, y = get()
        while [x, y] not in board.get_canputs():
            print(f"{x},{y} is an invalid coordinate.")
            x, y = get()
        return x, y


class Cpu(Player):

    def __init__(self, mark):
        super().__init__("Cpu", mark)
        self.depth = 5

    def random(self, board):
        return random.choice(board.get_canputs())

    def static_value(self, board):
        pt = 10
        if board.is_won(-self.mark):
            return -pt
        if board.is_won(self.mark):
            return pt
        return 0
    
    def minmax_depth_1(self, board):
        hand  = []
        score = -99
        canput = board.get_canputs()
        random.shuffle(canput)
        for xy in canput:
            x, y = xy
            b = copy.deepcopy(board)
            b.put(x, y, self.mark)
            s = self.static_value(b)
            if s >= score:
                score = s
                hand = xy
        return hand
    
    def minimax(self, board, depth):
        node_num = 0
        start = time.time()
        def get_children(board, mark):
            children = []
            for h in board.get_canputs():
                b = copy.deepcopy(board)
                x, y = h
                b.put(x, y, mark)
                children.append(b)
            nonlocal node_num
            node_num += len(children)
            return children
                
        def _minmax(self, board, mark, depth):
            if depth == 0 or board.is_won(-mark):
                return self.static_value(board)
            children = get_children(board, mark)
            if len(children) == 0:
                return self.static_value(board)
            if mark == self.mark:
                max = -9999
                for c in children:                
                    score = _minmax(self, c, -1 * mark, depth-1)
                    if score > max: max = score
                return max
            if mark == -self.mark:
                min = 9999
                for c in children:                
                    score = _minmax(self, c, -1 * mark, depth-1)
                    if score < min: min = score
                return min
        
        children = get_children(board, self.mark)
        hands = board.get_canputs()
        max  = -9999
        hand = []
        for c,h in zip(children, hands):
            score = (_minmax(self, c, -self.mark, depth=depth))
            #print(c)
            #print("last_score:"+str(score))
            if score > max:
                max = score
                hand = h
                end = time.time()
                
        print("elapsed time: ", end-start)
        print("node number : ",node_num)
        return hand

    def alpha_beta(self, board, depth):
        node_num = 0
        start = time.time()
        def get_children(board, mark):
            children = []
            for h in board.get_canputs():
                b = copy.deepcopy(board)
                x, y = h
                b.put(x, y, mark)
                children.append(b)
            nonlocal node_num
            node_num += len(children)
            return children
                
        def _alpha_beta(self, board, mark, depth, a, b):
            if depth == 0 or board.is_won(-mark):
                return self.static_value(board)
            children = get_children(board, mark)
            if len(children) == 0:
                return self.static_value(board)
            if mark == self.mark:
                for c in children:
                    if a < b:
                        score = _alpha_beta(self, c, -1 * mark, depth-1, a, b)
                    if score > a: a = score
                return a
            if mark == -self.mark:
                for c in children:
                    if a < b:
                        score = _alpha_beta(self, c, -1 * mark, depth-1, a, b)
                    if score < b: b = score
                return b
        
        children = get_children(board, self.mark)
        hands = board.get_canputs()
        map_ch = random.sample(list(zip(children, hands)), len(children))
        max  = -9999
        hand = []
        for c,h in map_ch:
            score = (_alpha_beta(self, c, -self.mark, depth, -9999, 9999))
            if score > max:
                max = score
                hand = h
                
        end = time.time()
        print("elapsed times  : ", end-start)
        print("number of nodes: ",node_num)
        return hand

    def set_depth(self, lv):
        self.depth = lv
        
    def think(self, board):
        #return self.minimax(board, 5)
        return self.alpha_beta(board, self.depth)


if __name__ == "__main__":
    g = TicTacToe()
    g.play()
