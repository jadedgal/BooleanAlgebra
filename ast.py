from helpers import *

class AST:
    def __init__(self, root:Node):
        self.root = root
    
    def __eq__(self, other):
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash((type(self), tuple(self.__dict__.values())))
    
    def size(self,node):
        if isinstance(node, (Constant, Variable)):
            return 1
        if isinstance(node, Not):
            return 1 + self.size(node.child)
        return 1 + sum(self.size(a) for a in node.args)
    
    def __str__(self):
        if isinstance(self.root, Variable):
            return f"{self.root.name}"
        if isinstance(self.root, Constant):
            return f"{'1' if self.root.value else '0'}"
        if isinstance(self.root, Not):
            return f"~{self.root.args[0]}'"
        if isinstance(self.root, And):
            return f"({' · '.join(map(str, self.root.args))})"
        if isinstance(self.root, Or):
            return f"({' + '.join(map(str, self.root.args))}"

    def print(self):
        print(self.__str__())
        
    def rewrite(self):
        self.root = self.rewriteNode(self.root)

    def rewriteNode(self, node:Node) -> Node:
    
        if isinstance(node, (Variable, Constant)):
            return node

        # Rewrite children first
        if isinstance(node, Not):
            child = self.rewriteNode(node.args[0])
            return self.rewriteNot(child)

        if isinstance(node, And):
            args = [self.rewriteNode(a) for a in node.args]
            return self.rewriteAnd(args)

        if isinstance(node, Or):
            args = [self.rewriteNode(a) for a in node.args]
            return self.rewriteOr(args)

        return node
    
    def rewriteNot(self,child:Not) -> Node:
        if isinstance(child,Not):
            return child.args[0]
        
        if isinstance(child,Constant):
            return Constant(1 if child.value == 0 else 0)
        
        if isinstance(child,And):
            #demorgan's
            return Or(*[self.rewriteNot(a) for a in child.args])
        
        if isinstance(child,Or):
            #demorgan's
            return And(*[self.rewriteNot(a) for a in child.args])
        
        return Not(child)
    
    def rewriteAnd(self,args: list[Node]) -> Node:
    # If any argument is 0 return 0
        for a in args:
            if isinstance(a, Constant) and a.value == 0:
                return Constant(0)

        # Remove 1s
        args = [a for a in args if not (isinstance(a, Constant) and a.value == 1)]

        # x and not x return  0
        for a in args:
            if Not(a) in args:
                return Constant(0)

        # Remove duplicates (idempotence)
        args = list(set(args))

        if len(args) == 0:
            return Constant(1)
        if len(args) == 1:
            return args[0]

        return And(*args)

    def rewriteOr(self, args: list[Node]) -> Node:
        # If any argument is 1 → 1
        for a in args:
            if isinstance(a, Constant) and a.value == 1:
                return Constant(1)

        # Remove 0s
        args = [a for a in args if not (isinstance(a, Constant) and a.value == 0)]

        # x + not x return 1
        for a in args:
            if Not(a) in args:
                return Constant(1)

        # Remove duplicates
        args = list(set(args))

        if len(args) == 0:
            return Constant(0)
        if len(args) == 1:
            return args[0]

        return Or(*args)
    
    
