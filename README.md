# dice-roller
A dice roller(interpreter) written in Python.

How to use:

    Run the dicer.py and write your expressions like:

        python3 dicer.py

        >>> 1d10
        10
        >>> 2d20 - 5
        16
        Or you can just use it as a simple calculator
        >>> 1 + 3 * (42 - 24)
        55
        Rolls the d20 and d8 two times and adds them
        >>> 2(d20+d8)
        36 
        You can assign dices to variables and use them anywhere
        >>> sword = 3d6 + 6
        0
        >>> sword
        21
        >>> 2sword
        31
        You can execute commands with an exclamation point(!)
        >>> !exit
        You can print things by "print", "say", "tell", "out"
        >>> !print Hello World!

        You can assign or throw dice upon running file by adding the 
        expressions in load.txt. You can also use commands here.
        load.txt:
        d1
        d20
        sword = d20 + 2

        You can load your own files using !load command:
        >>> !load mysword.txt
        My sword:
        28



    Use it directly from command-line:
        
        python3 dicer.py "expression"

        $ py dicer.py "d20"
        9
        $ py dicer.py "d20 - 15"
        0
        $ py dicer.py "241 * 461"
        111101
        
