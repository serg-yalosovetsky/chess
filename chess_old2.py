from uuid import uuid4
import numpy as np
from collections import Counter


class Tree():
    def __init__(self, ancestor=0):
        if ancestor:
            self.ancestor = ancestor
        elif ancestor == 0:
            ancestor = Tree(None)
            ancestor.id = 0
            self.ancestor = ancestor
            Tree.root = self
        self.id = uuid4().hex
        self.childs = []

    
    def all_childs(self):
        try:
            childs = []
            childs.append(self)
            # print(self)
            for child in self.childs:
                # print(child)
                childs.append(child.all_childs() )
        except Exception:
            childs = self
        return childs
        
    def __str__(self):
        return f'ancestor {self.ancestor.id} id {self.id} childs {len(self.childs)}'
    
    def __repr__(self):
        return f'ancestor {self.ancestor.id} id {self.id} childs {len(self.childs)}'
    
        
    def add_child(self):
        tree = Tree(self)
        self.childs.append(tree)
        return tree
    
    def search(self, id):
        res = 0
        # print(self)
        try:
            if self.id == id:
                return self
            for child in self.childs:
                # print(child)
                if child.id == id:
                    return child
                try:
                    res = child.search(id)
                    if res:
                        return res
                except Exception as e:
                    print(e)
                    
        except Exception as e:
            print(e)
        return res

    def get_node_path(self, id):
        res = []
        # print(self)
        node = self.search(id)
        while True:
            try:   
                print(node)
                res.append(node)
                if node.ancestor == 0:
                    break
                ancestor = node.ancestor
                # print(ancestor) 
                node = ancestor 
            except Exception as e:
                print(e)
                break
        return res
        






    
    
        
    
class Board():
    def __init__(self, basic_figure=None, board=None, rules=None, colors=None):
        if not basic_figure:
            basic_figure = {'pawn':8, 'rook':2, 'knight':2, 'bishop':2, 'king':1, 'queen':1}
            basic_color = ['white', 'black']
            
        else:
            basic_color = colors

        self.figures = []
            
        for figure, quant in basic_figure.items():
            for i in range(quant):
                self.figures.append(figure)
      
        self.figures_quantity = len(self.figures)
        self.all_figures = {}
        self.color_figures = {}
        
        for num, value in enumerate(basic_color):
            self.color_figures[value] = {}
            for fig_num, fig in enumerate(self.figures):
                self.all_figures[fig_num+1+ num * self.figures_quantity] = f'{value} {fig}'
                self.color_figures[value][fig_num+1 + num * self.figures_quantity] = f'{value} {fig}'
        self.all_figures[0] = 'cell'
        self.all_figures[-1] = 'null'
        
        
        if not board:
            self.height = 8
            self.width = 8
            self.board = np.zeros((self.height, self.width))
            self.board[1] = [i for i in range(1, 9)]
            self.board[0] = [9, 11, 13, 15, 16, 14, 12, 10]
            self.board[-1] = [25, 27, 29, 31, 32, 30, 28, 26]
            self.board[-2] = [i+16 for i in range(1, 9)]
            for i, row in enumerate(self.board):
                for j, cell in enumerate(row):
                    if cell:
                        if cell <= self.figures_quantity:
                            name = self.color_figures[basic_color[0]][cell]
                            self.color_figures[basic_color[0]][cell] = {
                                'name': name, 'pos': Pos(i,j)} 
        else:
            self.board = board
            
        self.board_color = np.zeros((self.height, self.width))
        for i, line in enumerate(self.board_color):
            for j, cell in enumerate(line):
                if (i+j)%2:
                    self.board_color[i][j] = 1
                else:
                    self.board_color[i][j] = -1
        
        if not rules:
            self.rules = {'pawn' : {'all' : [(1,0)], 'fight': [(1,1)], 'first': [(2,0)],
                                    'end': [(1,0)], 'ghost':False, 'score':10, 'k':1},
                     'rook' : {'all' : [(-100,0),(100,0),(0,-100),(0,100)],
                               'ghost':False, 'score':30, 'k':1},                   
                     'knight' : {'all' : [(2,1),(2,-1), (-2,1),(-2,-1), (1,2),(1,-2), (-1,2),(-1,-2)],
                                 'ghost':True, 'step': 'move', 'score':25, 'k':1},                  
                     'bishop' : {'all' : [(-100,-100),(100,100),(100,-100),(-100,100)],
                                 'ghost':False, 'score':25, 'k':1},                  
                     'queen' : {'all' : [(-100,-100),(100,100),(100,-100),(-100,100), (-100,0),
                                         (100,0),(0,-100),(0,100)], 'ghost':False, 'score':100, 'k':1},                  
                     'king' : {'all' : [(-1,0),(1,0),(0,-1),(0,1)], 'ghost':False, 'score':10000, 'k':1}
                     }  
                             
    def __repr__(self):
        # board_str = [ [] for i in range(self.height)]
        
        delim = '  ' +('-' * (self.width * 3+3) ) + '\n'
        row_num = '    '
        for i in range(1, self.width+1):
            row_num += f' {i} '
        row_num += '\n'  
        res = row_num + delim
        
        for i, row in enumerate(self.board): #self.
            res += f'{i+1} | '
            for j, cell in enumerate(row):
                # board_str[i].append(self.all_figures[cell])                     
                name = ''
                for val in self.all_figures[cell].split():
                    name += val[0]
                if len(name) == 1:
                    name += ' '
                res += name + ' '
            res += f'| {i+1}\n'
        res += delim + row_num
        
        return res
            
            
            
class MoveLog():
    def __init__(self):
        self.tree = Tree()
        self.history = {}
        
    def move(self, figure, move, score):
        self.tree.add_child(self.tree.id)
        self.history[self.tree.id] = {'figure': figure, 'move': move, 'score': score}
       
       
class Pos():
    def __init__(self, x, y):
        self.x = x 
        self.y = y
    
    def __add__(self, pos):
        if type(pos) == int:
            x = self.x + pos
            y = self.y + pos
        else:
            x = self.x + pos.x*k
            y = self.y + pos.y*k
        return Pos(x,y)
        
    def __sub__(self, pos):
        if type(pos) == int:
            x = self.x - pos
            y = self.y - pos
        else:
            x = self.x - pos.x
            y = self.y - pos.y
        return Pos(x,y)
        
    def __mul__(self, arg):
        if type(arg) == int:
            x = self.x * arg
            y = self.y * arg
        else:
            x = self.x * arg.x
            y = self.y * arg.y

        return Pos(x,y)
    
    def __contains__(self, pos_start, pos_final):
        if (self.x > pos_start.x and self.x < pos_final.x
            and self.y > pos_start.y and self.y < pos_final.y):
            return True
        else:
            return False
        
    
    def inclusive(self, pos_start, pos_final):
        if (self.x >= pos_start.x and self.x <= pos_final.x
            and self.y >= pos_start.y and self.y <= pos_final.y):
            return True
        else:
            return False
        
    def bigger_or_eq(self, pos):
        return (self.x >= pos.x and self.y >= pos.y)
        
    def bigger(self, pos):
        return (self.x > pos.x and self.y > pos.y)
        
    def lesser_or_eq(self, pos):
        return (self.x <= pos.x and self.y <= pos.y)
        
    def lesser_or_eq(self, pos):
        return (self.x < pos.x and self.y < pos.y)
        
    def get_tuple(self):
        return self.x, self.y
         
    def __repr__(self):
        return f'({self.x} {self.y})'
        
        
class Chess():
    def __init__(self, color=None):
        self.board = Board()
        self.movelog = MoveLog()
        self.height = self.board.height
        self.width = self.board.width
        self.figure_color = color if color else 'white' 
        self.rules = self.board.rules
        self.figures = self.board.color_figures[self.figure_color]    
        
    def move(self):
        for num, figure in self.board:
            self.board.rules[figure]
    
    def check_move_V(self, p, v):
        # p = Pos(1,1) 
        # v = Pos(-1, 0)       
        return p.plus(v).inclusive(Pos(0,0), Pos(self.height, self.width))
    
    def check_move_or_fight(self, pos:Pos, k, V, ghost, mode, step):
        move_list = []

        if step is None:
            step = 1
        
        for i in range(1, step+1, k):
            # for j in range(0, abs_y+1, step.y):

            if self.check_move_V(pos, V*i):
                # if ghost:
                    # move_list.append(p.plus(Pos(i,j)) )
                # else:
                move_pos = pos + Pos(V.x*i, V.y*i)
                if 'fight' in mode:
                    if self.board.board[move_pos.get_tuple()] == self.color*-1:
                        move_list.append(move_pos )
                if 'move' in mode:
                    if self.board.board[move_pos.get_tuple()] == 0:
                        move_list.append(move_pos )
            else:
                if not ghost:
                    break
            
        return move_list
                        
                        
    def calc_available_moves(self, figure):
        figure_rules = self.rules[figure['name'].split[-1]]
      
        if figure_rules.get('all'):
            step = figure_rules.get('step') if figure_rules.get('step') else Pos(1,1)
                
            for V in figure_rules['all']:
                if figure_rules.get('all') == figure_rules.get('fight'):
                    mode = 'move_fight'
                else:
                    mode = 'move'
                    
                move_list = self.check_move_or_fight(figure['pos'], V, ghost=figure_rules['ghost'], mode=mode, step=step)
            if mode == 'move':
                for V in figure_rules['fight']:
                    move_list += self.check_move_or_fight(figure['pos'], V, ghost=figure_rules['ghost'], mode=mode, step=step)
        return move_list
     
     
    def check_enemy_in_cell(self, pos:Pos):
        fig = self.board(pos.get_tuple())
        return not (self.figure_color in self.board.all_figures[fig])
     
     
    def scoring(self, move, figure, pos:Pos):
        # figure = self.board(pos.get_tuple())
        if self.check_enemy_in_cell(move + pos):
            score = figure['score']
        else:
            score = 0
        return score
    
            
    def do_move(self, move, pos:Pos):
        figure = self.board(pos.get_tuple())
        score = self.scoring(move, pos)
        self.move_log.move(figure, move, score)
        self.tree.add()



    def main(self):

        for figure in self.figures:
            figure_rules = self.rules[figure['name'].split[-1]]

            available_moves = self.calc_available_moves(figure, figure_rules)
            for move in available_moves:
                do_move(move, board, board_color, color, pos)
            
    
chess = Chess()
board = Board()

print(board)
repr(board)
board.all_figures
board.color_figures