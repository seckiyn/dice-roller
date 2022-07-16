# COMMANDS

LOAD_FILE, WARNING, EXIT = "LOAD_FILE", "WARNING", "EXIT"


def handle(op):
    state = WARNING
    operation, inp = op.split()
    if operation.upper() in ("LOAD", "LOADFILE", "LOAD_FILE"):
        # LOAD THE FILE
        state = LOAD_FILE
    if operation.upper() in ("EXIT", "QUIT", "Q"):
        # EXIT FROM PROGRAM
        state = EXIT


















def main():
    pass

main()
