from collections import namedtuple
from multiprocessing.connection import answer_challenge
import pprint
from re import S
from turtle import position
from uuid import uuid4

from pyparsing import col 


A_ORD = 97  #ord of 'a'
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
        abc = {i:chr(i+A_ORD) for i in range(8)}
        try:
            _s = f'{abc[self.y]}{8 - self.x}'
        except Exception:
            _s = f'error {self.y} {self.x}'
        return _s
    def print(self):
        print(self.to_print())



def get_cells_between(p1:V, p2:V):
    if p1.x == p2.x:
        cells = [V(p1.x, i) for i in range(min(p1.y, p2.y)+1, max(p1.y, p2.y))]
    if p1.y == p2.y:
        cells = [V(j, p1.y) for j in range(min(p1.x, p2.x)+1, max(p1.x, p2.x))]
    if abs(p1.x - p2.x) == abs(p1.y - p2.y):
        sign_x = get_sign(p1.x, p2.x)
        sign_y = get_sign(p1.y, p2.y)
        cells = [V(p1.x + i*sign_x, p1.y + i*sign_y) for i in range(1, abs(p1.x - p2.x))]
    return cells









def safe_divide(a,b):
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








class RuleSet:
    def pawn_transform(self, figure_id, position):
        figure = self.figures[figure_id]
        can_transform = (position.x == (self.height - 1)) or (position.x == 0)

        if can_transform:
            print('you can (not) choose figure to transform')
            new_figure_type = 'queen'
            self.figures[figure_id] = self.Figures(new_figure_type, figure.color)
            return new_figure_type
        else:
            return False

    def if_rook_first_move(self, params, *args, **kwargs):
        figure_id = params['figure_id']
        board = params['board']
        figures = params['figures']
        figure = figures[figure_id]
        if not ruleset.is_first_move(figure.position, board):
            return False
        
        king_id = None
        for fig in figures:
            if figures[fig].type == 'king':
                king_id = fig

        if king_id:
            if not ruleset.is_first_move(figures[king_id].position, board):
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
        if not ruleset.is_first_move(figure.position, board):
            return False
        
        rook_ids = []
        for fig in figures:
            if figures[fig].type == 'rook':
                rook_ids.append[fig]

        if rook_ids:
            for rook_id in rook_ids:
                if not ruleset.is_first_move(figures[rook_id].position, board):
                    return False
                vector = get_cells_between(figure.position, figures[rook_id].position)
                void_line = (board[cell.x][cell.y] != 0 for cell in vector)
                if all(void_line):
                    return True
        return False


    def __init__(self):
        self.Figures = namedtuple('Figures' , 'type color')
        self.Fig_State = namedtuple('Fig_State' , 'type color position')
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
                    1:self.Figures('rook', 'white'),
                    2:self.Figures('knight', 'white'),
                    3:self.Figures('bishop', 'white'),
                    4:self.Figures('queen', 'white'),
                    5:self.Figures('king', 'white'),
                    6:self.Figures('bishop', 'white'),
                    7:self.Figures('knight', 'white'),
                    8:self.Figures('rook', 'white'),
                    9:self.Figures('pawn', 'white'),
                    10:self.Figures('pawn', 'white'),
                    11:self.Figures('pawn', 'white'),
                    12:self.Figures('pawn', 'white'),
                    13:self.Figures('pawn', 'white'),
                    14:self.Figures('pawn', 'white'),
                    15:self.Figures('pawn', 'white'),
                    16:self.Figures('pawn', 'white'),

                    17:self.Figures('pawn', 'black'),
                    18:self.Figures('pawn', 'black'),
                    19:self.Figures('pawn', 'black'),
                    20:self.Figures('pawn', 'black'),
                    21:self.Figures('pawn', 'black'),
                    22:self.Figures('pawn', 'black'),
                    23:self.Figures('pawn', 'black'),
                    24:self.Figures('pawn', 'black'),
                    25:self.Figures('rook', 'black'),
                    26:self.Figures('knight', 'black'),
                    27:self.Figures('bishop', 'black'),
                    28:self.Figures('queen', 'black'),
                    29:self.Figures('king', 'black'),
                    30:self.Figures('bishop', 'black'),
                    31:self.Figures('knight', 'black'),
                    32:self.Figures('rook', 'black'),
        
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
            self._fig_state[fig] = self.Fig_State(type=self.__figures[fig].type, 
                                                  color=self.__figures[fig].color, 
                                                  position=self._figure_pos[fig])
            

        self.rules = {'pawn' : {
                    'moves': {
                        'move' : [V(1,0)], 
                        'fight': [V(1,-1),V(1,1)], 
                        'first': [V(2,0)], 
                        }, 
                    'ghost':False, 
                    'first_move': lambda *x: True,
                    'move&fight': False,
                    'score':10, 
                    'type': 'first', 
                    'transform': self.pawn_transform, 
                    'k':1,
                    },
                'rook' : {
                    'moves': {
                        'move' : [V(-100,0), V(100,0), V(0,-100), V(0,100)], 
                        'first' : [V(-100,0), V(100,0), V(0,-100), V(0,100)], 
                        },
                    'ghost':False, 
                    'first_move': self.if_rook_first_move,
                    'move&fight': True,
                    'score':30,
                    'type': 'fast', 
                    'transform': False, 
                    'k':1
                    },                   
                'knight' : {
                    'moves': {
                        'move' : [V(2,1),V(2,-1), V(-2,1),V(-2,-1), 
                                    V(1,2),V(1,-2), V(-1,2),V(-1,-2)], 
                        },
                    'ghost':True, 
                    'first_move': False,
                    'move&fight': True,
                    'step': 'move', 
                    'score':25,
                    'type': 'knight',
                    'transform': False,  
                    'k':1
                    },                  
                'bishop' : {
                    'moves': {
                        'move' : [V(-100,-100),V(100,100),V(100,-100),V(-100,100)], 
                        },
                    'ghost':False, 
                    'first_move': False,
                    'move&fight': True,
                    'score':25,
                    'type': 'fast', 
                    'transform': False,  
                    'k':1
                    },                  
                'queen' : {
                    'moves': {
                        'move' : [V(-100,-100),V(100,100),V(100,-100),V(-100,100),
                                    V(-100,0), V(100,0),V(0,-100),V(0,100)], 
                                    },
                    'ghost':False, 
                    'first_move': False,
                    'move&fight': True,
                    'score':100,
                    'type': 'fast', 
                    'transform': False, 
                    'k':1},                  
                'king' : {
                    'moves': {
                        'move' : [V(-1,0),V(1,0),V(0,-1),V(0,1)], 
                        'first' : [V(-1,0),V(1,0),V(0,-1),V(0,1)], 
                        },
                    'ghost':False, 
                    'first_move': self.if_king_first_move,
                    'move&fight': True,
                    'score':10000, 
                    'type': 'slow', 
                    'transform': False, 
                    'k':1,
                    }
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
            fig_state[fig] = self.Fig_State(type=self.__figures[fig].type, 
                                 color=self.__figures[fig].color, 
                                 position=figure_pos[fig])
        return fig_state


    @property
    def board(self):
        return [row.copy() for row in self.first_board]


    def prettify(self, _board=[], true_look=False, hyphens=27, indent=' '):
        if _board == []:
            _board = self.board
        print(' ', '-'*hyphens)
        for count, row in enumerate(_board):
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

    def if_can_beat(self, figure_id, position, board=[], figures={}):
        if not figures:
            figures = self.__figures
        if board == []:
            board = self.board
        figure = figures[figure_id]
        if (new_figure_id := board[position.x][position.y]) != 0:
            new_figure = figures[new_figure_id]
            if new_figure.color != figure.color:
                return True
        return False

    def if_can_move_or_beat(self, figure_id, position, board=[], figures={}):
        if not figures:
            figures = self.__figures
        if board == []:
            board = self.board
        figure = figures[figure_id]
        if (new_figure_id := board[position.x][position.y]) == 0:
            print(figure_id, figure, new_figure_id, position)

            return 'move'
        else:
            new_figure = figures[new_figure_id]
            if new_figure.color != figure.color:
                print(new_figure.color, new_figure.type, new_figure_id, position)
                print(figure.color, figure.type, figure_id)
                return 'beat'
        return False

    def get_position_by_id(self, figure_id, board=[]):
        if board == []:
            board = self.board
        for count_x, row in enumerate(board):
            for count_y, cell in enumerate(row):
                if cell == figure_id:
                    return V(count_x,count_y)
        return -1


    def get_id_by_pos(self, position, board=[]):
        if board == []:
            board = self.board
        try:
            return board[position.x][position.y]
        except Exception:
            return -1

    def if_can_move(self, position, board=[]):
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

    def move_figure(self, _from, _to, board=[]):
        if board == []:
            board = self.board
        try:
            if not isinstance(_from, V):
                if _from == 0:
                    return False
                _from = self.get_position_by_id(_from)
            if not isinstance(_to, V):
                if _to == 0:
                    return False
                _to = self.get_position_by_id(_to)
            print(board[_to.x][_to.y])
            if board[_to.x][_to.y] == 0 or board[_from.x][_from.y] == 0:
                board[_from.x][_from.y], board[_to.x][_to.y] = \
                    board[_to.x][_to.y], board[_from.x][_from.y]
            else:
                board[_from.x][_from.y], board[_to.x][_to.y] = \
                    0, board[_from.x][_from.y]

        except Exception:
            return False
        return True


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


    def moves_product(self, figure, figure_id, figure_rule, _print, moves, available_moves, board=[]):
        if figure.color == 'white':
            move = move * -1
        if figure_rule['type'] == 'fast' or figure_rule['type'] == moves:
                # если фигура быстрая (типа туры и офицера)
                # или быстрая во время первого хода, типа пешки
            if _print > 4:
                print('figure_rule[type] == fast', figure_rule['type'])
            step_x = get_sign_zero(move.x) * figure_rule['k']
            step_y = get_sign_zero(move.y) * figure_rule['k']
            steps = int(max(move.y, move.x, key=abs) / figure_rule['k'])
            step = V(step_x, step_y)
        else:
            steps = 1
            step = move
        if _print > 6:
            print(move)
            print('steps, step, figure_rule[k]', steps, step, figure_rule['k'])
            print(figure_rule['type'])

        for i in range(1, steps+1):
            move = step * i * figure_rule['k']
            new_position = position+move
            if self.is_position_valid(new_position):
                if figure_rule['moves'].get('fight'):
                    res = self.if_can_beat(figure_id, new_position)
                    if _print > 4:
                        print('can beat', res)
                if figure_rule['move&fight']:
                    res = self.if_can_move_or_beat(figure_id, new_position)
                    if _print > 4:
                        print('move&fight', res)
                else:
                    res = self.if_can_move(new_position)
                    if _print > 4:
                        print('can move', res)
                if _print > 4:
                    print(position, new_position, 'new_position move')
                    print('figure to move', self.get_id_by_pos(position), self.get_id_by_pos(new_position))
                    
                if res:
                    if _print > 1:
                        self.move_figure(position, new_position, board=board)
                    if _print > 6:
                        pp.pprint(self.board)
                        self.prettify(true_look=True)
                    if _print > 1:
                        self.prettify()
                        self.move_figure(new_position, position, board=board)
                    available_moves['to'].append(new_position)
                    

    def get_available_step(self, figure_id, figure, board, _print=0):
        # figure = self.__figures[figure_id]
        position = self.get_position_by_id(figure_id, board=board)
        available_moves = {}
        available_moves['to'] = []
        available_moves['from'] = position
        figure_rule = self.rules[figure.type]
        print(figure_rule)
        moves_list = []
        params = {'figure_id': figure_id, 'board': board, 'figures': figures}
        if figure_rule['first_move'] and figure_rule['first_move'](params) and self.is_first_move(position):
            moves_list.append('first') 
            # режим действия, если на первом ходу фигуры действуют особые условия
        else:
            moves_list.append('move') 
        if _print > 2:
            self.prettify(board, true_look=True)
            self.prettify(board)
        if figure_rule['moves'].get('fight'):
            moves_list.append('fight')
        for moves in moves_list:
            print(moves)
            for move in figure_rule['moves'][moves]:
                print(moves, move)
                if figure.color == 'white':
                    move = move * -1
                if figure_rule['type'] == 'fast' or figure_rule['type'] == moves:
                        # если фигура быстрая (типа туры и офицера)
                        # или быстрая во время первого хода, типа пешки
                    step_x = get_sign_zero(move.x) * figure_rule['k']
                    step_y = get_sign_zero(move.y) * figure_rule['k']
                    steps = abs(int(max(move.y, move.x, key=abs) / figure_rule['k']))
                    step = V(step_x, step_y)
                else:
                    steps = 1
                    step = move

                for i in range(1, steps+1):
                    move = step * i * figure_rule['k']
                    new_position = position+move
                    if self.is_position_valid(new_position):
                        if moves == 'fight':
                            res = self.if_can_beat(figure_id, new_position)
                            print('can beat')
                        elif figure_rule['move&fight']:
                            res = self.if_can_move_or_beat(figure_id, new_position)
                            print('can move or beat', res)
                        else:
                            res = self.if_can_move(new_position)
                            print('can move')
                        if res:
                            if _print > 1:
                                self.move_figure(position, new_position, board=board)
                            if _print > 6:
                                pp.pprint(board)
                                self.prettify(board)
                                self.prettify(board, true_look=True)
                            if _print > 1:
                                self.prettify(board)
                                self.move_figure(new_position, position, board=board)
                            available_moves['to'].append(new_position)
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

    def reinit():
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
           
t = Tree()

ruleset = RuleSet()
ruleset.move_figure(V('c2'), V('c6') )
# ruleset.move_figure(21, 13 )
# ruleset.move_figure(11, 19)
ruleset.prettify()

ruleset.get_available_step(12, ruleset.board, _print=2)
ruleset.move_figure(V('c7'), V('c3') )

pp.pprint(ruleset.board)
pp.pprint(ruleset.first_board)


current_color = 'white'


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
            if self.figures[fig].color == color:
                figures[fig] = self.figures[fig]  
        return figures

game = Game('white')
game.get_all_figures('black')
game.prettify()


current_color = 'white'
current_color = 'black'
figures = game.get_all_figures(current_color)

for fig in figures:
    ruleset.get_available_step(fig, figures[fig], game.board)


game.get_all_figures(current_color)[1]

figure = 2
figure = 25
ruleset.get_available_step(figure, figures[figure], game.board, figure)



ruleset.fig_state