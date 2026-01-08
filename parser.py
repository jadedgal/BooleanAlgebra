from helpers import *
from ast import AST

class parser:
    def __init__(self):
        self.string = ""
        self.pos = 0

    def parse(self, string: str) -> AST:
        self.string = string.replace(" ", "")
        self.pos = 0
        node = self.parseExpr()
        if self.pos != len(self.string):
            raise SyntaxError(f"Unexpected input at position {self.pos}")
        return AST(node)

    # OR: lowest precedence
    def parseExpr(self):
        node = self.parseXor()
        while self.peek() == "+":
            self.consume("+")
            right = self.parseXor()
            node = Or(node, right)
        return node

    # XOR
    def parseXor(self):
        node = self.parseTerm()
        while self.peek() == '"':
            self.consume('"')
            right = self.parseTerm()
            node = Xor(node, right)
        return node

    # AND
    def parseTerm(self):
        node = self.parseFactor()
        while self.peek() == ".":
            self.consume(".")
            right = self.parseFactor()
            node = And(node, right)
        return node

    # NOT
    def parseFactor(self):
        if self.peek() == "!":
            self.consume("!")
            return Not(self.parseFactor())
        return self.parseAtom()

    def parseAtom(self):
        ch = self.peek()
        if ch == "(":
            self.consume("(")
            node = self.parseExpr()
            self.consume(")")
            return node
        if ch == "0":
            self.consume("0")
            return Constant(0)
        if ch == "1":
            self.consume("1")
            return Constant(1)
        if ch.isalpha():
            return self.parseVariable()
        raise SyntaxError(f"Unexpected character '{ch}' at position {self.pos}")

    def parseVariable(self):
        start = self.pos
        while self.peek() and self.peek().isalnum():
            self.pos += 1
        return Variable(self.string[start:self.pos])

    def peek(self):
        return self.string[self.pos] if self.pos < len(self.string) else None

    def consume(self, char):
        if self.peek() != char:
            raise SyntaxError(f"Expected '{char}' at position {self.pos}")
        self.pos += 1
