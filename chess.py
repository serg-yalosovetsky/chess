import pandas
import uuid


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

