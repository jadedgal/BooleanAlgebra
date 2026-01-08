from parser import parser
from ast import AST

def main():
    p = parser()
    ast = p.parse(input("Enter boolean: \n"))
    print(ast.getString())
    ast.rewrite()
    print(ast.getString())

if __name__ == "__main__":
    main()