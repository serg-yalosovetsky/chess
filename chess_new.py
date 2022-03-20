from collections import namedtuple
import pprint
from turtle import position

A_ORD = 97  #ord of 'a'
pp = pprint.PrettyPrinter()

def get_sign(num):
    if num >= 1:
        return 1
    elif num <= -1:
        return -1
    else:
        return 0

def unsign_max(a,b):
    m = abs(a)
    n = abs(b)
    return max(n,m)

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
    Figures = namedtuple('Figures' , 'type color')
    width = 8
    height = 8
    types = {
            'pawn': 1,
            'rook': 2,
            'knight': 3,
            'bishop': 4,
            'queen': 5,
            'king': 6,
            }
    figures = {
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

    first_board = [
                [25,26,27,28,29,30,31,32],
                [17,18,19,20,21,22,23,24], 
                [0, 0, 0, 0, 0, 0, 0, 0 ],
                [0, 0, 0, 0, 0, 0, 0, 0 ],
                [0, 0, 0, 0, 0, 0, 0, 0 ],
                [0, 0, 0, 0, 0, 0, 0, 0 ],
                [9, 10,11,12,13,14,15,16],
                [1, 2, 3, 4, 5, 6, 7, 8 ],
    ]
    board = [row.copy() for row in first_board]
    board_color = [ #   where # is white and * is black
                ['#','*','#','*','#','*','#','*'],
                ['*','#','*','#','*','#','*','#'],
                ['#','*','#','*','#','*','#','*'],
                ['*','#','*','#','*','#','*','#'],
                ['#','*','#','*','#','*','#','*'],
                ['*','#','*','#','*','#','*','#'],
                ['#','*','#','*','#','*','#','*'],
                ['*','#','*','#','*','#','*','#'],
            ]
 
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
 
    rules = {'pawn' : {
                'moves': {
                    'move' : [V(1,0)], 
                    'fight': [V(1,-1),V(1,1)], 
                    'first': [V(2,0)], 
                    }, 
                'ghost':False, 
                'first_move': True,
                'move&fight': False,
                'score':10, 
                'type': 'first', 
                'transform': pawn_transform, 
                'k':1,
                },
             'rook' : {
                'moves': {
                     'move' : [V(-100,0), V(100,0), V(0,-100), V(0,100)], 
                     },
                'ghost':False, 
                'first_move': True,
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
                     },
                'ghost':False, 
                'first_move': True,
                'move&fight': True,
                'score':10000, 
                'type': 'slow', 
                'transform': False, 
                'k':1,
                }
            }  

    def prettify(self, _list=[], true_look=False, hyphens=27, indent=' '):
        if _list == []:
            _list = self.board
        print(' ', '-'*hyphens)
        for count, row in enumerate(_list):
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

    def if_can_beat(self, figure_id, position):
        figure = self.figures[figure_id]
        if (new_figure_id := self.board[position.x][position.y]) != 0:
            new_figure = self.figures[new_figure_id]
            if new_figure.color != figure.color:
                return True
        return False

    def if_can_move_or_beat(self, figure_id, position):
        figure = self.figures[figure_id]
        if (new_figure_id := self.board[position.x][position.y]) == 0:
            return 'move'
        else:
            new_figure = self.figures[new_figure_id]
            if new_figure.color != figure.color:
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

    def if_can_move(self, position):
        if self.board[position.x][position.y] == 0:
            return True
        else:
            return False    

    def is_position_valid(self, position):
        if (position.x >= 0 and position.y >= 0 and
            position.x < self.height and position.y < self.width):
            return True
        else:
            return False 

    def is_first_move(self, position):
        if self.board[position.x][position.y] == self.first_board[position.x][position.y]:
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


    def moves_product(self, figure, figure_id, figure_rule, _print, moves, available_moves):
        if figure.color == 'white':
            move = move * -1
        if figure_rule['type'] == 'fast' or figure_rule['type'] == moves:
                # если фигура быстрая (типа туры и офицера)
                # или быстрая во время первого хода, типа пешки
            if _print > 4:
                print('figure_rule[type] == fast', figure_rule['type'])
            step_x = get_sign(move.x) * figure_rule['k']
            step_y = get_sign(move.y) * figure_rule['k']
            steps = int(unsign_max(move.y, move.x) / figure_rule['k'])
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
                        self.move_figure(position, new_position)
                    if _print > 6:
                        pp.pprint(self.board)
                        self.prettify(true_look=True)
                    if _print > 1:
                        self.prettify()
                        self.move_figure(new_position, position)
                    available_moves['to'].append(new_position)
                    

    def get_available_step(self, figure_id, board, _print=0):
        figure = self.figures[figure_id]
        position = self.get_position_by_id(figure_id)
        available_moves = {}
        available_moves['to'] = []
        available_moves['from'] = position
        figure_rule = self.rules[figure.type]
        moves_list = []
        if figure_rule['first_move'] and self.is_first_move(position):
            moves_list.append('first') 
            # режим действия, если на первом ходу фигуры действуют особые условия
        else:
            moves_list.append('move') 
        if _print > 2:
            self.prettify(true_look=True)
            self.prettify()
            if _print > 4:
                print(figure_id, figure.type, figure.color)
                print(figure_rule)
                print('first move')
        if figure_rule['moves'].get('fight'):
            moves_list.append('fight')
        for moves in moves_list:
            for move in figure_rule['moves'][moves]:
                if figure.color == 'white':
                    move = move * -1
                if figure_rule['type'] == 'fast' or figure_rule['type'] == moves:
                        # если фигура быстрая (типа туры и офицера)
                        # или быстрая во время первого хода, типа пешки
                    if _print > 4:
                        print('in move or first', moves, figure_rule['moves'][moves])
                        print('figure_rule[type] == fast', figure_rule['type'])
                    step_x = get_sign(move.x) * figure_rule['k']
                    step_y = get_sign(move.y) * figure_rule['k']
                    steps = int(unsign_max(move.y, move.x) / figure_rule['k'])
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
                        if moves == 'fight':
                            res = self.if_can_beat(figure_id, new_position)
                            if _print > 4:
                                print('can beat', res)
                        elif figure_rule['move&fight']:
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
                                self.move_figure(position, new_position)
                            if _print > 6:
                                pp.pprint(self.board)
                                self.prettify(true_look=True)
                            if _print > 1:
                                self.prettify()
                                self.move_figure(new_position, position)
                            available_moves['to'].append(new_position)
                                
        return available_moves


   
ruleset = RuleSet()
ruleset.move_figure(V('c2'), V('c6') )
ruleset.move_figure(11, 19)
ruleset.prettify()
ruleset.get_available_step(20, ruleset.board, _print=2)

ruleset.board = ruleset.first_board



