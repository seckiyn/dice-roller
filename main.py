""" Dice roller main interpreter """
import random

random.seed(123)

# CONSTS

VERBOSE = True
DIGITS = "1234567890"
IGNORE_CHARACTERS = " \n\t"

# TOKEN TYPES
INTEGER, FLOAT, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, DICE, EOF = (
        "INTEGER", "FLOAT", "PLUS", "MINUS", "MUL", "DIV",
        "LPAREN", "RPAREN", "DICE", "EOF"
        )

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __str__(self):
        string = f"Token({self.type}:{self.value})"
        return string
    def __repr__(self):
        return str(self)


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            # print(self.current_char)
    def integer(self):
        num = ""
        while self.current_char is not None and self.current_char in DIGITS:
            num += self.current_char
            self.advance()
        if self.current_char == ".":
            num += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char in DIGITS:
                num += self.current_char
                self.advance()
            return Token(FLOAT, float(num))
        return Token(INTEGER, int(num))
    def dicer(self):
        self.advance()
        return Token(DICE, self.integer().value)
    def math_token(self):
        if self.current_char == "+":
            self.advance()
            return Token(PLUS, "+")
        if self.current_char == "-":
            self.advance()
            return Token(MINUS, "-")
        if self.current_char == "*":
            self.advance()
            return Token(MUL, "*")
        if self.current_char == "/":
            self.advance()
            return Token(DIV, "/")
        if self.current_char == "(":
            self.advance()
            return Token(LPAREN, "(")
        if self.current_char == ")":
            self.advance()
            return Token(RPAREN, ")")
        raise Exception("Something is wrong")
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char in IGNORE_CHARACTERS:
                self.advance()
                continue
            if self.current_char in DIGITS:
                return self.integer()
            if self.current_char == "d":
                return self.dicer()
            if self.current_char in "(+-*/)":
                return self.math_token()
            raise Exception("Something is wrong") # TODO: Add line number
        return Token(EOF, None)


# PARSER AND AST CLASSES

class AST:
    def __repr__(self):
        return str(self)

class BinaryOp(AST):
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right
    def __str__(self):
        string = f"BinaryOp({self.left}:{self.op_token}:{self.right})"
        return string

class UnaryOp(AST):
    def __init__(self, op_token, right):
        self.op_token = op_token
        self.right = right
    def __str__(self):
        string = f"UnaryOp({self.op_token}:{self.right})"
        return string

class Cluster(AST):
    def __init__(self, times, dices):
        """ Cluster(INTEGER, DICE_LIST)"""
        self.dices = dices
        self.times = times
    def __str__(self):
        string = f"Cluster({self.times}:{self.dices})"
        return string

class Dice(AST):
    def __init__(self, token):
        """ Will return a random int according to value """
        self.token = token
        self.value = int(token.value)
    def __str__(self):
        string = f"DiceAST({self.value})"
        return string

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __str__(self):
        string = f"Num({self.value})"
        return string
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # print(self.lexer.text)
        self.current_token = self.lexer.get_next_token()
    def eat(self, type_):
        if self.current_token.type == type_:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception("{self.current_token.type}:{type_}")
    def parse(self):
        return self.expr()
    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            if token.type == MINUS:
                self.eat(MINUS)
            node = BinaryOp(node, token, self.term())
        return node
    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            if token.type == DIV:
                self.eat(DIV)
            node = BinaryOp(node, token, self.factor())
        return node
    def factor(self):
        # print(self.current_token)
        if self.current_token.type == INTEGER: # TODO: Add float
            token = self.current_token
            self.eat(INTEGER)
            if self.current_token.type in (DICE, LPAREN):
                return Cluster(token, self.factor())
            return Num(token)
        if self.current_token.type == DICE:
            token = self.current_token
            self.eat(DICE)
            return Dice(token)
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        if self.current_token.type == PLUS:
            token = self.current_token
            self.eat(PLUS)
            return UnaryOp(token, self.factor())
        if self.current_token.type == MINUS:
            token = self.current_token
            self.eat(MINUS)
            return UnaryOp(token, self.factor())


        raise Exception("There's something wrong with parser")


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        def no_method(node):
            raise Exception(f"There's no method called {method_name}->{node}")
        visitor = getattr(self, method_name, no_method)
        return visitor(node)
class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
    def interpret(self):
        tree = self.parser.parse()
        result = self.visit(tree)
        return result
    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        op_token = node.op_token.type
        right = self.visit(node.right)
        if op_token == PLUS:
            return left + right
        if op_token == MINUS:
            return left - right
        if op_token == MUL:
            return left * right
        if op_token == DIV:
            return left // right
    def visit_UnaryOp(self, node):
        op_token = node.op_token.type
        right = self.visit(node.right)
        if op_token == PLUS:
            return right
        if op_token == MINUS:
            return -right
    def visit_Cluster(self, node):
        times = node.times.value
        result = 0
        for time in range(times):
            result += self.visit(node.dices)
        return result
    def visit_Dice(self, node):
        value = node.value
        result = random.randint(1, value)
        if VERBOSE:
            print(f"Rolling {node}:", result)
        return result
    def visit_Num(self, node):
        return node.value


from test import *
parserf = lambda text: Parser(Lexer(text))
interf  = lambda text: Interpreter(parserf(text))
def tests():
    # test_dice_lexer(Lexer)
    test_dice_parser(parserf)
    test_dice_interpreter(interf)

def main():
    tests()

if __name__ == "__main__":
    main()

























