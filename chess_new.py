import copy
import pprint
import time
from collections import namedtuple
# from termios import TAB0
from time import time
from uuid import uuid4

from pyparsing import col


# ord of 'a'
A_ORD = 97
pp = pprint.PrettyPrinter()


def get_sign_zero(num):
    if num >= 1:
        return 1
    elif num <= -1:
        return -1
    else:
        return 0


def get_sign(x,y):
    if x <= y:
        return 1
    else:
        return -1

class V:
    x = 0
    y = 0

    def __init__(self, x, y=-1):
        if isinstance(x, str):
            if y == -1:
                y = int(x[1:])
                x = x[0]
            self.y = ord(x) - 97
            self.x = 8 - y
        else:
            self.x = x
            self.y = y

    def __repr__(self) -> str:
        return f'V({self.x},{self.y})'

    def __eq__(self, v):
        if (isinstance(v, V) and
                self.x == v.x and self.y == v.y):
            return True
        else:
            return False

    def __add__(self, v):
        if isinstance(v, V):
            return V(self.x + v.x, self.y + v.y)
        else:
            return V(self.x + v, self.y + v)

    def __sub__(self, v):
        if isinstance(v, V):
            return V(self.x - v.x, self.y - v.y)
        else:
            return V(self.x - v, self.y - v)

    def __mul__(self, v):
        if isinstance(v, V):
            return V(self.x * v.x, self.y * v.y)
        else:
            return V(self.x * v, self.y * v)

    def to_print(self):
        abc = {i: chr(i+A_ORD) for i in range(8)}
        try:
            _s = f'{abc[self.y]}{8 - self.x}'
        except Exception:
            _s = f'error {self.y} {self.x}'
        return _s

    def print(self):
        print(self.to_print())


class Move():

    def __init__(self, from_v: V, to_v: V):
        self.from_v = from_v
        self.to_v = to_v

    def __repr__(self) -> str:
        return f'Move({self.from_v},{self.to_v})'

    def __eq__(self, move):
        if (isinstance(move, Move) and
                self.from_v == move.from_v and self.to_v == move.to_v):
            return True
        else:
            return False

    def print(self):
        print(repr(self))


class CurrentColor:
    def __init__(self, colors):
        self.colors = colors
        self.current_color = colors[0]

    def __repr__(self) -> str:
        return f'{self.current_color}'

    def switch(self):
        for color in self.colors:
            if color == self.current_color:
                self.current_color = self.colors[
                        (self.colors.index(color) + 1) % len(self.colors)
                                                    ]
                return self.current_color


def get_cells_between(p1: V, p2: V):
    cells = []
    if p1.x == p2.x:
        cells = [V(p1.x, i) for i in range(min(p1.y, p2.y)+1, max(p1.y, p2.y))]
    if p1.y == p2.y:
        cells = [V(j, p1.y) for j in range(min(p1.x, p2.x)+1, max(p1.x, p2.x))]
    if abs(p1.x - p2.x) == abs(p1.y - p2.y):
        sign_x = get_sign(p1.x, p2.x)
        sign_y = get_sign(p1.y, p2.y)
        cells = [V(p1.x + i*sign_x, p1.y + i*sign_y) for i in range(1, abs(p1.x - p2.x))]
    return cells


def safe_divide(a, b):
    if b == 0:
        return 0
    else:
        return a/b


def _in(value, limit_min, limit_max):
    if value > limit_min and value < limit_max:
        return True
    else:
        return False


def _out(value, limit_min, limit_max):
    if value < limit_min and value > limit_max:
        return True
    else:
        return False


def _not(value, *args):
    for arg in args:
        if value == arg:
            return False
    return True


Figures = namedtuple('Figures', 'type color')
Fig_State = namedtuple('Fig_State', 'type color position')
Time_Counter = namedtuple('Time_Counter', 'start_time max_time')
Fig_Rules = namedtuple('Fig_Rules', 'moves ghost first_move move_fight step score type transform k')


class RuleSet:
    def pawn_transform(self, figure_id, position):
        figure = self.figures[figure_id]
        can_transform = (position.x == (self.height - 1)) or (position.x == 0)

        if can_transform:
            print('you can (not) choose figure to transform')
            new_figure_type = 'queen'
            self.figures[figure_id] = Figures(new_figure_type, figure.color)
            return new_figure_type
        else:
            return False

    def if_rook_first_move(self, params, *args, **kwargs):
        figure_id = params['figure_id']
        board = params['board']
        figures = params['figures']
        figure = figures[figure_id]
        if not self.is_first_move(figure.position, board):
            return False
        
        king_id = None
        for fig in figures:
            if figures[fig].type == 'king':
                king_id = fig

        if king_id:
            if not self.is_first_move(figures[king_id].position, board):
                return False
            vector = get_cells_between(figure.position, figures[king_id].position)
            void_line = (board[cell.x][cell.y] != 0 for cell in vector)
            if all(void_line):
                return True
        return False
    
    def if_king_first_move(self, params, *args, **kwargs):
        figure_id = params['figure_id']
        board = params['board']
        figures = params['figures']
        figure = figures[figure_id]
        if not self.is_first_move(figure.position, board):
            return False
        
        rook_ids = []
        for fig in figures:
            if figures[fig].type == 'rook':
                rook_ids.append(fig)

        if rook_ids:
            for rook_id in rook_ids:
                if not self.is_first_move(figures[rook_id].position, board):
                    return False
                vector = get_cells_between(figure.position, figures[rook_id].position)
                void_line = (board[cell.x][cell.y] != 0 for cell in vector)
                if all(void_line):
                    return True
        return False


    def __init__(self, _print=0):
        self._print = _print
        self.width = 8
        self.height = 8
        self.types = {
                'pawn': 1,
                'rook': 2,
                'knight': 3,
                'bishop': 4,
                'queen': 5,
                'king': 6,
                }
        self.__figures = {
                    1:Figures('rook', 'white'),
                    2:Figures('knight', 'white'),
                    3:Figures('bishop', 'white'),
                    4:Figures('queen', 'white'),
                    5:Figures('king', 'white'),
                    6:Figures('bishop', 'white'),
                    7:Figures('knight', 'white'),
                    8:Figures('rook', 'white'),
                    9:Figures('pawn', 'white'),
                    10:Figures('pawn', 'white'),
                    11:Figures('pawn', 'white'),
                    12:Figures('pawn', 'white'),
                    13:Figures('pawn', 'white'),
                    14:Figures('pawn', 'white'),
                    15:Figures('pawn', 'white'),
                    16:Figures('pawn', 'white'),

                    17:Figures('pawn', 'black'),
                    18:Figures('pawn', 'black'),
                    19:Figures('pawn', 'black'),
                    20:Figures('pawn', 'black'),
                    21:Figures('pawn', 'black'),
                    22:Figures('pawn', 'black'),
                    23:Figures('pawn', 'black'),
                    24:Figures('pawn', 'black'),
                    25:Figures('rook', 'black'),
                    26:Figures('knight', 'black'),
                    27:Figures('bishop', 'black'),
                    28:Figures('queen', 'black'),
                    29:Figures('king', 'black'),
                    30:Figures('bishop', 'black'),
                    31:Figures('knight', 'black'),
                    32:Figures('rook', 'black'),
        
                    }

     
        self.first_board = [
                    [25,26,27,28,29,30,31,32],
                    [17,18,19,20,21,22,23,24], 
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [9, 10,11,12,13,14,15,16],
                    [1, 2, 3, 4, 5, 6, 7, 8 ],
        ]

        self._board = [row.copy() for row in self.first_board]


        self.board_color = [ #   where # is white and * is black
                    ['#','*','#','*','#','*','#','*'],
                    ['*','#','*','#','*','#','*','#'],
                    ['#','*','#','*','#','*','#','*'],
                    ['*','#','*','#','*','#','*','#'],
                    ['#','*','#','*','#','*','#','*'],
                    ['*','#','*','#','*','#','*','#'],
                    ['#','*','#','*','#','*','#','*'],
                    ['*','#','*','#','*','#','*','#'],
                ]
    
        self._figure_pos = {}
        for i,row in enumerate(self.first_board):
            for j,cell in enumerate(row):
                if cell > 0:
                    self._figure_pos[cell] = V(i,j)

        self._fig_state = {}
        for fig in self.__figures:
            self._fig_state[fig] = Fig_State(type=self.__figures[fig].type, 
                                                  color=self.__figures[fig].color, 
                                                  position=self._figure_pos[fig])
            
# 'moves ghost first_move move_fight score type transform k
        self.rules = {'pawn' : Fig_Rules(
                                        moves={
                                            'move' : [V(1,0)], 
                                            'fight': [V(1,-1),V(1,1)], 
                                            'first': [V(2,0)], 
                                        }, 
                                        ghost=False, 
                                        first_move=lambda *x: True,
                                        move_fight=False,
                                        step=1,
                                        score=10, 
                                        type='first', 
                                        transform=self.pawn_transform, 
                                        k=1,
                                ),
                    'rook' : Fig_Rules(
                                        moves= {
                                            'move' : [V(-100,0), V(100,0), V(0,-100), V(0,100)], 
                                            'first' : [V(-100,0), V(100,0), V(0,-100), V(0,100)], 
                                            },
                                        ghost=False, 
                                        first_move= self.if_rook_first_move,
                                        move_fight= True,
                                        step=1,
                                        score=30,
                                        type='fast', 
                                        transform= False, 
                                        k=1
                                ),                   
                    'knight' : Fig_Rules(
                                        moves= {
                                            'move' : [V(2,1),V(2,-1), V(-2,1),V(-2,-1), 
                                                        V(1,2),V(1,-2), V(-1,2),V(-1,-2)], 
                                            },
                                        ghost=True, 
                                        first_move= False,
                                        move_fight= True,
                                        step='move', 
                                        score=25,
                                        type= 'knight',
                                        transform= False,  
                                        k=1
                                ),                  
                    'bishop' : Fig_Rules(
                                        moves= {
                                            'move' : [V(-100,-100),V(100,100),V(100,-100),V(-100,100)], 
                                            },
                                        ghost=False, 
                                        first_move= False,
                                        move_fight= True,
                                        step=1,
                                        score=25,
                                        type= 'fast', 
                                        transform= False,  
                                        k=1
                                ),                  
                    'queen' : Fig_Rules(
                                        moves= {
                                            'move' : [V(-100,-100),V(100,100),V(100,-100),V(-100,100),
                                                        V(-100,0), V(100,0),V(0,-100),V(0,100)], 
                                                        },
                                        ghost=False, 
                                        first_move= False,
                                        move_fight= True,
                                        step=1,
                                        score=100,
                                        type= 'fast', 
                                        transform= False, 
                                       k=1
                                ),                  
                    'king' : Fig_Rules(
                                        moves= {
                                            'move' : [V(-1,0),V(1,0),V(0,-1),V(0,1)], 
                                            'first' : [V(-1,0),V(1,0),V(0,-1),V(0,1)], 
                                            },
                                        ghost=False, 
                                        first_move= self.if_king_first_move,
                                        move_fight= True,
                                        step=1,
                                        score=10000, 
                                        type= 'slow', 
                                        transform= False, 
                                        k=1,
                            )
                }  


    @property
    def figure_pos(self):
        figure_pos = {}
        for i,row in enumerate(self.first_board):
            for j,cell in enumerate(row):
                if cell > 0:
                    figure_pos[cell] = V(i,j)
        return figure_pos

    @property
    def fig_state(self):
        fig_state = {}
        figure_pos = self.figure_pos
        for fig in self.__figures:
            fig_state[fig] = Fig_State(type=self.__figures[fig].type, 
                                 color=self.__figures[fig].color, 
                                 position=figure_pos[fig])
        return fig_state


    @property
    def board(self):
        return [row.copy() for row in self.first_board]


    def prettify(self, board=[], true_look=False, hyphens=27, indent=' '):
        if board == []:
            board = self.board
        print(' ', '-'*hyphens)
        for count, row in enumerate(board):
            if true_look:
                print(f'{count} | ', end='')
            else:
                print(f'{self.height - count} | ', end='')
            for j in row:
                if j < 10:
                    print(f'{j} {indent}', end='')
                else:
                    print(f'{j}{indent}', end='')
            print('|')
        print(' ', '-'*hyphens)
        _str = ''
        for i in range(8):
            if true_look:
                _str += f'{i}  ' 
            else:
                _str += f'{chr(i+A_ORD)}  ' 

        print(f'    {_str}')

    def if_can_beat(self, figure_id:int, position:V, board:list=[], figures:dict={}):
        if not figures:
            figures = self.__figures
        if board == []:
            board = self.board
        figure = figures[figure_id]
        if (new_figure_id := board[position.x][position.y]) != 0:
            new_figure = figures[new_figure_id]
            if new_figure.color != figure.color:
                return 'beat'
        return False

    def if_can_move_or_beat(self, figure_id:int, position:V, board:list=[], figures:dict={}):
        if not figures:
            figures = self.__figures
        if board == []:
            board = self.board
        figure = figures[figure_id]
        new_figure_id = board[position.x][position.y]
        if new_figure_id == 0:
            if self._print > 2:
                print('if_can_move_or_beat', figure_id, figure, new_figure_id, position)

            return 'move'
        else:
            new_figure = figures[new_figure_id]
            if new_figure.color != figure.color:
                if self._print > 2:
                    print('if_can_move_or_beat', new_figure.color, new_figure.type, new_figure_id, position)
                    print('if_can_move_or_beat', figure.color, figure.type, figure_id)
                return 'beat'
        return False

    def get_position_by_id(self, figure_id:int, board:list=[]):
        if board == []:
            board = self.board
        for count_x, row in enumerate(board):
            for count_y, cell in enumerate(row):
                if cell == figure_id:
                    return V(count_x,count_y)
        return -1


    def get_id_by_pos(self, position:V, board:list=[]):
        if board == []:
            board = self.board
        try:
            return board[position.x][position.y]
        except Exception:
            return -1

    def if_can_move(self, position:V, board:list=[]):
        if board == []:
            board = self.board
        
        if board[position.x][position.y] == 0:
            return True
        else:
            return False    

    def is_position_valid(self, position):
        if (position.x >= 0 and position.y >= 0 and
            position.x < self.height and position.y < self.width):
            return True
        else:
            return False 

    def is_first_move(self, position, board=[]):
        if not board:
            board = self.board
        if board[position.x][position.y] == self.first_board[position.x][position.y]:
            return True
        else:
            return False

    def move_figure(self, _from:V=0, _to:V=0, move:Move=None, board:list=[]):
        if board == []:
            board = self.board
        try:
            if not isinstance(_from, V) or not isinstance(_to, V):
                if _from == 0 or _to == 0:
                    if move is None:
                        return False
                    else:
                        _from = move.from_
                        _to = move.to_
                elif not isinstance(_from, V):
                    _from = self.get_position_by_id(_from)
                elif not isinstance(_to, V):
                    _to = self.get_position_by_id(_to)
            if self._print > 2:
                print(board[_to.x][_to.y])
            if board[_to.x][_to.y] == 0 or board[_from.x][_from.y] == 0:
                board[_from.x][_from.y], board[_to.x][_to.y] = \
                    board[_to.x][_to.y], board[_from.x][_from.y]
            else:
                board[_from.x][_from.y], board[_to.x][_to.y] = \
                    0, board[_from.x][_from.y]

        except Exception:
            return False
        return board

    def step_move(position=V(1,1), board=[], moves=[]):
        for move in moves:
            # if move in diagonal:
            if abs(move[0]) == abs(move[1]):
                pass
            # if move up right left down:
            if (move[0] == 0) or (move[1] == 0):
                pass
            #if knight
            if abs(safe_divide(move[0], move[1])) == 1:
                pass


    def get_available_steps(self, figure_id:int, figures:dict, _board:list):
        board = copy.deepcopy(_board)
        figure = figures[figure_id]
        position = self.get_position_by_id(figure_id, board=board)
        available_moves = {}
        available_moves['to'] = []
        available_moves['from'] = position
        available_moves['score'] = {}
        figure_rule = self.rules[figure.type]
        moves_list = []

        params = {'figure_id': figure_id, 
                  'board': board, 'figures': figures}
        if (figure_rule.first_move and 
                figure_rule.first_move(params) and 
                self.is_first_move(position, board)):
            moves_list.append('first') 
            # режим действия, если на первом ходу фигуры действуют особые условия
        else:
            moves_list.append('move') 
        if self._print > 2:
            self.prettify(board, true_look=True)
            self.prettify(board)
        if figure_rule.moves.get('fight'):
            moves_list.append('fight')
        for moves in moves_list:
            if self._print > 1:
                print(moves)
            for move in figure_rule.moves[moves]:
                if self._print > 1:
                    print(moves, move)
                if figure.color == 'white':
                    move = move * -1
                if figure_rule.type == 'fast' or figure_rule.type == moves:
                        # если фигура быстрая (типа туры и офицера)
                        # или быстрая во время первого хода, типа пешки
                    step_x = get_sign_zero(move.x) * figure_rule.k
                    step_y = get_sign_zero(move.y) * figure_rule.k
                    steps = abs(int(max(move.y, move.x, key=abs) / figure_rule.k))
                    step = V(step_x, step_y)
                else:
                    steps = 1
                    step = move

                for i in range(1, steps+1):
                    move = step * i * figure_rule.k
                    new_position:V = position+move
                    if self.is_position_valid(new_position):
                        if moves == 'fight':
                            res = self.if_can_beat(figure_id, new_position, board)
                            enemy_id = self.get_id_by_pos(new_position, board)
                            if self._print > 1:
                                print('can beat', res, new_position, enemy_id)
                            

                        elif figure_rule.move_fight:
                            res = self.if_can_move_or_beat(figure_id, new_position, board)
                            enemy_id = self.get_id_by_pos(new_position, board)
                            if self._print > 1:
                                print('can move or beat', res, new_position, enemy_id)
                        else:
                            res = self.if_can_move(new_position, board)
                            if self._print > 1:
                                print('can move')
                        if res:
                            if self._print > 1:
                                self.move_figure(position, new_position, board=board)
                            if self._print > 6:
                                pp.pprint(board)
                                self.prettify(board)
                                self.prettify(board, true_look=True)
                            if self._print > 1:
                                self.prettify(board)
                                self.move_figure(new_position, position, board=board)
                            available_moves['to'].append(new_position)
                            if res == 'beat':
                                if self._print > 1:
                                    print(f'beating {enemy_id} on {new_position}')
                                score = self.rules[figures[enemy_id].type].score
                                available_moves['score'][new_position.to_print()] = score
                        else:
                            break
                                
        return available_moves



class Tree():
    _nodes = set()
    def __init__(self, ancestor=None):
        # print(f'ancestor is {ancestor}')
        if ancestor is None:
            ancestor = Tree(0)
            self.ancestor = ancestor
            Tree.root = self
        elif ancestor != 0:
            self.ancestor = ancestor
            ancestor.childs.append(self)
        
        if ancestor == 0:
            self.id = 0
        else:
            self.id = uuid4().hex
        if self.id:
            Tree._nodes.add(self.id)
        self.childs = []

    def reinit(self):
        _nodes = set()

    def nodes(*args, **kwargs):
        l = list(Tree._nodes)
        # l.sort()
        return l

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
        _str = ''
        if self.ancestor.id == 0:
            _str += f'root, '
        else:
            _str += f'ancestor {self.ancestor.id[:10]}, '
        
        _str += f'id is {self.id[:10]}, '
        
        if len(self.childs) == 0:
            _str += f'no childs'
        else:
            _str += f'childs {len(self.childs)}'
        return _str 
    
    def __repr__(self):
        return self.__str__()
    
        
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


class Game():
    current_color = ''

    def __init__(self, color):
        self.current_color = color
        self.board = RuleSet().board
        self.figures = RuleSet().fig_state

    def prettify(self):
        return RuleSet().prettify(_board=self.board)

    def get_all_figures(self, color=''):
        figures = {}
        if color == '':
            color = self.current_color
        for fig in self.figures:
            if self.figures[fig].color == color or color == 'all':
                figures[fig] = self.figures[fig]
        return figures


current_color = 'white'

game = Game('white')
game.get_all_figures('black')
game.prettify()

figure = 2

colors = ['white', 'black']
color = current_color
moves = {}
figures = game.get_all_figures('all')
figures = game.get_all_figures(colors[0])

for figure_id, figure in figures.items():
    print(figure_id, figure)
    moves[figure_id] = ruleset.get_available_steps(figure_id, figures, game.board)
pp.pprint(moves)

for fig_id, move in moves.items():
    if move['to']:
        print(fig_id, move)




Tree().reinit()

t = Tree()
trees = {}
colors = ['white', 'black']
cc = CurrentColor(colors=colors)
cc.switch()
cc
t0 = time()
while t<2:
    for figure_id, figure in figures.items():
        print(figure_id, figure)
        moves[figure_id] = ruleset.get_available_steps(figure_id, figures, game.board)
    pp.pprint(moves)
    for fig_id, move in moves.items():
        if move['to']:
            _tree = Tree(t).id
            trees[_tree.id] = {'fig_id': fig_id, 'move': move, 'figure':figures[fig_id]}
            print(fig_id, move)

    t = time() - t0
    


pprint.pprint(t.childs)
pprint.pprint(trees)





moves = {}
for figure_id, figure in figures.items():
    print(figure_id, figure)
    moves[figure_id] = ruleset.get_available_steps(figure_id, figures, game.board)

moves



import matplotlib.pyplot as plt
import networkx as nx


# Defining a Class
class GraphVisualization:
   
    def __init__(self):
          
        # visual is a list which stores all 
        # the set of edges that constitutes a
        # graph
        self.visual = []
          
    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
          
    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
  
# Driver code
G = GraphVisualization()
G.addEdge(t.id[:10], 2)
G.addEdge(1, 0)
G.addEdge(1, 2)
G.addEdge(1, 3)
G.addEdge(5, 3)
G.addEdge(3, 4)

G.visualize()

print(t.id[:10])
_l = []
for _t in t.childs:
    print(t.id[:10], _t.id[:10])
    _l.append((t.id[:10], _t.id[:10]))
    for __t in _t.childs:
        _l.append((_t.id[:10], __t.id[:10]))
        print(_t.id[:10], __t.id[:10])

_l
s = '''c15915ee1a 3c3b700e50
... c15915ee1a ada8c4290e
... c15915ee1a b36cdf672d
... c15915ee1a da34a29aea
... c15915ee1a a624f92b3b
... c15915ee1a b06bc2e267
... c15915ee1a 3b9a6b4bb6'''
_l = []
l = s.split('\n')
for i in _l:
    G.addEdge(i[0], i[1])

board = copy.deepcopy(game.board)
# cc.current_color


def start_game(color: CurrentColor, max_time, _print=0):
    # figures: list[Fig_State] = game.get_all_figures(color.current_color)
    Tree().reinit()
    max_time *= 20
    tree = Tree()
    ruleset = RuleSet(_print=_print)
    game = Game('white')
    trees = {}
    board = copy.deepcopy(game.board)
    figures: list[Fig_State] = copy.deepcopy(game.get_all_figures('all'))

    start_time = time.time()
    _time = Time_Counter(start_time=start_time, max_time=max_time)
    _trees = next_round(ruleset, board, figures, color, tree, _time, _print=_print)
    trees.update(_trees)
    print(f'time is spend: {time.time() - _time.start_time}')

    return trees, tree


def next_round(ruleset, board, figures, color, tree, _time: Time_Counter, _print=0, message=''):

    if (time.time() - _time.start_time) > _time.max_time:
        if _print > 0:
            ruleset.prettify(board)

        return trees
    else:
        if _print > 1:
            print(f'time is spend: {time.time() - _time.start_time}')

    _board = copy.deepcopy(board)
    _figures: list[Fig_State] = copy.deepcopy(figures)
    moves = {}
    trees = {}
    moves_len = 0
    
    for figure_id, figure in _figures.items():
        # print(figure_id, figure.color, color.current_color)
        if figure.color == color.current_color:
            # print(figure_id, figure)
            moves[figure_id] = ruleset.get_available_steps(figure_id, _figures, _board)
            moves_len += len(moves[figure_id]['to'])
    try:
        time_2_move = _time.max_time/moves_len
    except ZeroDivisionError:
        time_2_move = _time.max_time

    print(f'moves_len: {moves_len} time_2_move: {time_2_move} spend time {time.time() - _time.start_time}')

    for fig_id, move in moves.items():
        if move['to']:
            for move_to in move['to']:
                if _print > 1:
                    print('available moves ', fig_id, move['from'], move_to)

                _board = ruleset.move_figure(move['from'], move_to, board=_board)

                # old_position = _figures[fig_id].position

                _tree = Tree(tree)
                trees[_tree.id] = {'fig_id': fig_id,
                                   'move': move,
                                   'figure': _figures[fig_id]}

                _figures[fig_id] = Fig_State(_figures[fig_id].type,
                                            _figures[fig_id].color,
                                            move_to)
                if _print > 2:
                    ruleset.prettify(_board)

                color.switch()
                _message = message + f'moves from {color.current_color}   {fig_id} {move["from"]} {move_to}\n'
                if (time.time() - _time.start_time) < time_2_move:
                    __time = Time_Counter(start_time=time.time(), max_time=time_2_move)
                    _trees = next_round(ruleset, board, _figures, color, _tree, __time, _print=_print, message=_message)
                else:
                    if _print > 0:
                        ruleset.prettify(_board)
                        print(message)
                    if _print > 1:
                        print('time is out')
                    _trees = {}

                trees.update(_trees)

                # figures[fig_id] = Fig_State(figures[fig_id].type,
                #                             figures[fig_id].color,
                #                             old_position)
                _board = ruleset.move_figure(move_to, move['from'], _board)
                if _print > 1:
                    print('\n\n\n')
    return trees


# figures: list[Fig_State] = copy.deepcopy(game.get_all_figures('all'))

cc.switch()
print('current color', cc.current_color)
trees, t = start_game(cc, 2, _print=1)
len(t.childs)
t.childs[0]
t.childs[1].childs[1]
t.childs[1].childs[1].childs[2]

for _t in t.childs:
    
    print(_t)    
    # print(_t.childs)    
    print(len(_t.childs))


len(t.childs)
tree = Tree(self)

tree.childs[1]


figures[1]
_board = copy.deepcopy(board)

ruleset.prettify(_board)


