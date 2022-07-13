import sys
from main import interf

def argv():
    op = ""
    if len(sys.argv) == 2:
        op = sys.argv[1]
        print(interf(op).interpret())
        sys.exit()
argv()
while True:
    op = input(">>> ")
    if not op or op == "exit":
        sys.exit()
    print(interf(op).interpret())
