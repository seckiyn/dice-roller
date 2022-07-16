import sys
from main import interf
from command import handle

LOAD_FILE = "load.txt"

def load_file(file_name):
    with open(file_name, "r") as f:
        for line in f.readlines():
            if not(line.startswith("#")) and not(line == "\n"):
                interf(line).interpret()

def argv():
    op = ""
    if len(sys.argv) == 2:
        op = sys.argv[1]
        print(interf(op).interpret())
        sys.exit()

def handle_command(op):
    if not op or op == "exit":
        sys.exit()
    print(interf(op).interpret())

def parse_command(op):
    if op.startswith("!"):
        handle(op, parse_command)
    else:
        handle_command(op)

def command_line():
    """ Command line of dicer """
    while True:
        op = input(">>> ")
        parse_command(op)

if __name__ == "__main__":
    argv()
    handle("!load " + LOAD_FILE, parse_command)
    command_line()
