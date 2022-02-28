import pandas
import uuid
from collections import namedtuple


board = []
class Tree:
    root = None
    children = []
    id = None
    def __init__(self, root=None, children=[]):
        self.root = root
        self.id = uuid.uuid4().hex
        if children:
            self.children = children
        else:
            self.children = []
        if root is not None:
            root.children.append(self)

   
    def __repr__(self):
        _str = ''
        if self.root is None:
            # print(f'node is root')
            _str += f'node is root\n'
        else:
            # print(f'root of node is {self.root}')
            _str += f'root of node is {self.root.id}\n'

        # print(f'node id is {self.id}')
        _str += f'node id is {self.id}\n'

        if not self.children:
            # print(f'node is leaf')
            _str += f'node is leaf\n'
        else:
            # print(f'node has {self.children}')
            # print()
            # _str += f'node has {self.children}\n\n'
            _str += f'node has next children:\n'
            for child in self.children:
                _str += f'      {child.id} \n'
            _str += '\n'
        return _str

results = {}

tree = Tree()
player_color = 0

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, x, y):
        self.x = x
        self.y = y


figures = namedtuple('figures' , ['color', 'position', 'type'])

t=0
pos = Position(0,4)
white_figures = figures(white, pos, t)

class Figures:
    _type = None
    color = None
    def figure_move(board, figure )
# king   rook queen    bishop knight pawn
# король тура королева офицер конь   пешка

# 8  p p p p p p p p  black
# 7  r k b k q b k r  black
# 6
# 5
# 4
# 3
# 2  p p p p p p p p  white
# 1  r k b q k b k r  white 

# -> x
#  ^ y
 
#    1 2 3 4 5 6 7 8

    figure = namedtuple('figure', [ 'init_position', 
                                    'color', 
                                    'id', 
                                    'type',
                                    'direction'
                                    ]
                        )
    
    figure_type = namedtuple('figure_type', [ 'name',
                                            'first_move',
                                            'moves', 
                                            'pair_moves', 
                                            'transform', 
                                            'fight', 
                                            'teleport'
                                            ]
                        )

    figures = {'pawn': figure_type(
                            name='pawn', 
                            first_move=[(0,1),(0,2)],
                            moves=[(0,1)],
                            pair_moves=[],
                            transform=[(0,1)],
                            fight=[(1,1),(1,-1)],
                            teleport=[],
                            ),
                'rook': figure_type(
                            name='rook', 
                            first_move=[],
                            moves=[(0,100),(0,100)],
                            pair_moves=[],
                            transform=[(0,1)],
                            fight=[(1,1),(1,-1)],
                            teleport=[],
                            )
                            
                            }


    pawn01 = {'pawn': figure(
                            type='pawn', 
                            init_position=Position(2,1),
                            color='white',
                            direction=1,
                            id = 1,
                            ) }

    def __init__(self, _type, color):
        self._type = _type
        self.color = color



class RuleSet:
    figures = {}

    def step(self, figure, board):
        pass

