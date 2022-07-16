import sys
from main import interf

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
def command_line():
    """ Command line of dicer """
    while True:
        op = input(">>> ")
        handle_command(op)
if __name__ == "__main__":
    argv()
    load_file(LOAD_FILE)
    command_line()
