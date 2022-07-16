
# CONST

VERBOSE = False
# COMMANDS

LOAD_FILE, WARNING, EXIT, PRINT = "LOAD_FILE", "WARNING", "EXIT", "PRINT"

def load_file(filename, handler):
    with open(filename, "r") as file:
        for line in file.readlines():
            if line != "\n" and not(line.startswith("#")):
                handler(line[:-1])
    if VERBOSE: print("load_file", filename)

def op_parse(op):
    op = op[1:].strip()
    operation = None
    inp = None
    splitted_op = op.split()
    if len(splitted_op) == 1:
        operation = splitted_op[0]
    else:
        operation, *inp = splitted_op
    inp = " ".join(inp) if type(inp) == list else inp
    return operation, inp


def handle(op, handler):
    state = WARNING
    operation, inp = op_parse(op)
    if VERBOSE: print("Operation:", operation, "Input:", inp)
    # LOOK TO THE STATE
    if operation.upper() in ("LOAD", "LOADFILE", "LOAD_FILE"):
        # LOAD THE FILE
        state = LOAD_FILE
    elif operation.upper() in ("EXIT", "QUIT", "Q"):
        # EXIT FROM PROGRAM
        state = EXIT
    elif operation.upper() in ("PRINT", "TELL", "SAY", "OUT"):
        state = PRINT
    elif operation.upper() == "YEYUH":
        state = "YEYUH"



    # Do the STATE
    if state == LOAD_FILE:
        load_file(inp, handler)
    elif state == EXIT:
        sys.exit()
    elif state == PRINT:
        print(inp)
    elif state == WARNING:
        raise Exception("There's something wrong")
    else:
        raise NotImplementedError(state + " doesn't implemented")
    return "handle"

