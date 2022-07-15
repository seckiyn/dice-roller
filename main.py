""" Dice roller main interpreter """
import random

# TODO: Add ID compatibilty to cluster
# CONSTS

# random.seed(12345)
VERBOSE = False # Adds additional output information
DIGITS = "1234567890" # Digits(not neccessary)
IGNORE_CHARACTERS = " \n\t" # Characters to ignore in expression

# TOKEN TYPES
INTEGER, FLOAT, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, DICE, EOF = (
        "INTEGER", "FLOAT", "PLUS", "MINUS", "MUL", "DIV",
        "LPAREN", "RPAREN", "DICE", "EOF"
        )

ASSIGN, ID = ("ASSIGN", "ID")


class Token:
    """ Token storage class """
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __str__(self):
        string = f"Token({self.type}:{self.value})"
        return string
    def __repr__(self):
        return str(self)


class Lexer:
    """ Lexical analyzer """
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.row, self.col = 0, -1
        self.current_char = None
        self.advance()
    def advance(self):
        """ Move forward the cursor """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.col += 1
            if self.current_char == "\n":
                self.row += 1
                self.col = 0

            # print(self.current_char)
    def integer(self):
        """ Returns a number token """
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
        """ Returns a DICE token """
        self.advance() # Advance the "d" character
        return Token(DICE, int(self.integer().value))
    def math_token(self):
        """ Returns operation(math) tokens """
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
    def id_token(self):
        id_ = ""
        while self.current_char is not None and self.current_char.isalnum():
            id_ += self.current_char
            self.advance()
        return Token(ID, id_)
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        return self.text[peek_pos]
    def get_next_token(self):
        """ Returns the token """
        while self.current_char is not None:
            if self.current_char in IGNORE_CHARACTERS:
                self.advance()
                continue
            if self.current_char in DIGITS:
                return self.integer()
            if self.current_char == "d" and self.peek() in DIGITS:
                return self.dicer()
            if self.current_char in "(+-*/)":
                return self.math_token()
            if self.current_char == "=":
                self.advance()
                return Token(ASSIGN, "=")
            if self.current_char.isalnum():
                return self.id_token()
            ex = "Unexpected char {} at {} (row: {}, col: {})"
            ex = ex.format(self.current_char, self.pos, self.row, self.col)
            raise Exception(ex)
        return Token(EOF, None)


# PARSER AND AST CLASSES

class AST:
    """ AST base class """
    def __repr__(self):
        return str(self)

class BinaryOp(AST):
    """ Binary operations """
    def __init__(self, left, op_token, right):
        """
            left: node -> Left side of op
            op_token: token -> operation
            right: node -> Right side of op
        """
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

class Assign(AST):
    def __init__(self, name, node):
        self.name = name
        self.node = node
    def __str__(self):
        string = f"Assign({self.name}:{self.node})"
        return string
class Id(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.name = token.value
    def __str__(self):
        string = f"Id({self.value})"
        return string
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # print(self.lexer.text)
        self.current_token = self.lexer.get_next_token()
    def eat(self, type_):
        """ Check the current token type and get next """
        if self.current_token.type == type_:
            self.current_token = self.lexer.get_next_token()
        else:
            lex = self.lexer
            ex = "Unexpected token {} at {}({},{}) waited {}"
            ex = ex.format(self.current_token, lex.pos, lex.col, lex.row, type_)
            raise Exception(ex)
    def parse(self):
        return self.look()
    def look(self):
        return self.expr()
    def assign(self, name):
        self.eat(ASSIGN)
        to_assign = self.expr()
        return Assign(name, to_assign)
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
        if self.current_token.type in (INTEGER, FLOAT):
            token = self.current_token
            if self.current_token.type == INTEGER:
                self.eat(INTEGER)
            if self.current_token.type == FLOAT:
                self.eat(FLOAT)
            if self.current_token.type in (DICE, LPAREN, ID):
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
        return self.variable()
    def variable(self):
        token = self.current_token
        self.eat(ID)
        if self.current_token.type == ASSIGN:
            return self.assign(token.value)
        return Id(token)



class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        def no_method(node):
            raise Exception(f"There's no method called {method_name}->{node}")
        visitor = getattr(self, method_name, no_method)
        return visitor(node)

assigned = dict() # Find a better way
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
    def visit_Assign(self, node):
        assigned[node.name] = node.node
        return 0
    def visit_Id(self, node):
        return self.visit(assigned[node.name])


import test
parserf = lambda text: Parser(Lexer(text))
interf = lambda text: Interpreter(parserf(text))
def tests():
    # test.test_dice_lexer(Lexer)
    test.test_dice_parser(parserf)
    test.test_dice_interpreter(interf)

def main():
    tests()

if __name__ == "__main__":
    main()
