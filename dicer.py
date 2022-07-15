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
if __name__ == "__main__":
    argv()
    load_file(LOAD_FILE)
    while True:
        op = input(">>> ")
        if not op or op == "exit":
            sys.exit()
        print(interf(op).interpret())
