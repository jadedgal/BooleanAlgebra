class Node:
    def __init__(self):
        pass
    
class Variable(Node):
    def __init__(self, name:str):
        self.name = name

class Constant(Node):
    def __init__(self, value:int):
        if value not in [0,1]:
            raise ValueError("Constant must be 0 or 1")
        self.value = value
        
class Not(Node):
    def __init__(self, *args: Node):
        self.args = list(args)
        flat = []
        for a in args:
            if isinstance(a, Not):
                flat.extend(a.args)
            else:
                flat.append(a)
        self.args = flat
        

class And(Node):
    def __init__(self, *args: Node):
        self.args = list(args)
        flat = []
        for a in args:
            if isinstance(a, And):
                flat.extend(a.args)
            else:
                flat.append(a)
        self.args = flat

class Or(Node):
    def __init__(self, *args: Node):
        self.args = list(args)
        flat = []
        for a in args:
            if isinstance(a, Or):
                flat.extend(a.args)
            else:
                flat.append(a)
        self.args = flat