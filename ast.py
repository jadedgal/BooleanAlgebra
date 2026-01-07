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
    def __init__(self, child: Node):
        self.child = child

class And(Node):
    def __init__(self, *args: Node):
        self.args = list(args)

class Or(Node):
    def __init__(self, *args: Node):
        self.args = list(args)
