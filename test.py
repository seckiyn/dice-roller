""" Tests for dice roller interpreter """
from colorama import init, Fore

init(autoreset=True)
TEST_FILE = "tests.txt"
def test_cases(file):
    test_cases = list()
    with open(file, "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            if line:
                # Strip the comments
                line = line.split("#")[0].strip()
                test_cases.append(line)
    return test_cases


def out(*text, **kwargs):
    print(*text, **kwargs)


# out(test_cases(TEST_FILE))
def lexer_looper(lexer):
    token = lexer.get_next_token()
    out(token)
    while token.value is not None:
        token = lexer.get_next_token()
        out(token)
def test_dice_lexer(Lexer):
    tests = test_cases(TEST_FILE)
    for test in tests:
        lexer = Lexer(test)
        out(Fore.YELLOW + "Processing", test)
        lexer_looper(lexer)


def test_dice_parser(Parser):
    tests = test_cases(TEST_FILE)
    for test in tests:
        parser = Parser(test)
        out(Fore.YELLOW + "Processing", test)
        out(parser.parse())

def test_dice_interpreter(Interpreter):
    tests = test_cases(TEST_FILE)
    for test in tests:
        interpreter = Interpreter(test)
        out(Fore.YELLOW + "Processing", test)
        out(interpreter.interpret())
