from helpers import *

class AST:
    def __init__(self, root: Node):
        self.root = root

    def __eq__(self, other):
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash((type(self), tuple(self.__dict__.values())))

    def getString(self, node:Node = None) -> str:
        if node is None:
            node = self.root

        if isinstance(node, Variable):
            return node.name
        if isinstance(node, Constant):
            return str(node.value)
        if isinstance(node, Not):
            # ! has highest precedence, always prefix
            return f"!{self.getString(node.args[0])}"
        if isinstance(node, And):
            return "(" + ".".join(self.getString(a) for a in node.args) + ")"
        if isinstance(node, Or):
            return "(" + "+".join(self.getString(a) for a in node.args) + ")"
        if isinstance(node, Xor):
            return "(" + '"'.join(self.getString(a) for a in node.args) + ")"
        return str(node)
        
    def rewrite(self):
        self.root = self.rewriteNode(self.root)

    def rewriteNode(self, node: Node) -> Node:
        if isinstance(node, (Variable, Constant)):
            return node

        if isinstance(node, Not):
            child = self.rewriteNode(node.args[0])
            return self.rewriteNot(child)

        if isinstance(node, And):
            args = [self.rewriteNode(a) for a in node.args]
            return self.rewriteAnd(args)

        if isinstance(node, Or):
            args = [self.rewriteNode(a) for a in node.args]
            return self.rewriteOr(args)

        if isinstance(node, Xor):
            args = [self.rewriteNode(a) for a in node.args]
            return self.rewriteXor(args)

        return node
    
    def rewriteNot(self, child: Node) -> Node:
        if isinstance(child, Not):
            return child.args[0]
        if isinstance(child, Constant):
            return Constant(1 - child.value)
        if isinstance(child, And):
            return Or(*[self.rewriteNot(a) for a in child.args])
        if isinstance(child, Or):
            return And(*[self.rewriteNot(a) for a in child.args])
        return Not(child)

    def rewriteAnd(self, args: list[Node]) -> Node:
        # Flatten
        flat = []
        for a in args:
            if isinstance(a, And):
                flat.extend(a.args)
            else:
                flat.append(a)
        args = flat

        # x . 0 -> 0
        if any(isinstance(a, Constant) and a.value == 0 for a in args):
            return Constant(0)

        # x . 1 -> x
        args = [a for a in args if not (isinstance(a, Constant) and a.value == 1)]

        # x . !x -> 0
        for a in args:
            if any(isinstance(b, Not) and b.args[0] == a for b in args):
                return Constant(0)

        # remove duplicates
        args = list(dict.fromkeys(args))

        if len(args) == 0:
            return Constant(1)
        if len(args) == 1:
            return args[0]

        return And(*args)

    def rewriteOr(self, args: list[Node]) -> Node:
        # Flatten
        flat = []
        for a in args:
            if isinstance(a, Or):
                flat.extend(a.args)
            else:
                flat.append(a)
        args = flat

        # x + 1 -> 1
        if any(isinstance(a, Constant) and a.value == 1 for a in args):
            return Constant(1)

        # x + 0 -> x
        args = [a for a in args if not (isinstance(a, Constant) and a.value == 0)]

        # x + !x -> 1
        for a in args:
            if any(isinstance(b, Not) and b.args[0] == a for b in args):
                return Constant(1)

        # remove duplicates
        args = list(dict.fromkeys(args))

        if len(args) == 0:
            return Constant(0)
        if len(args) == 1:
            return args[0]

        return Or(*args)

    def rewriteXor(self, args: list[Node]) -> Node:
        # Flatten
        flat = []
        for a in args:
            if isinstance(a, Xor):
                flat.extend(a.args)
            else:
                flat.append(a)
        args = flat

        if not args:
            return Constant(0)
        if len(args) == 1:
            return args[0]

        left = args[0]
        right = args[1]

        # identities
        if left == right:
            new_node = Constant(0)
        elif isinstance(right, Constant) and right.value == 0:
            new_node = left
        elif isinstance(left, Constant) and left.value == 0:
            new_node = right
        elif isinstance(right, Constant) and right.value == 1:
            new_node = Not(left)
        elif isinstance(left, Constant) and left.value == 1:
            new_node = Not(right)
        else:
            # x " y -> (x . !y) + (!x . y)
            new_node = Or(
                And(left, Not(right)),
                And(Not(left), right)
            )

        if len(args) > 2:
            return self.rewriteXor([new_node] + args[2:])
        else:
            return new_node
