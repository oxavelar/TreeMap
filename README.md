TreeMap
=======

Python Library to visualize and group dictionary data types.

    >>> a = { 'cat':{'legs' : 4, 'heads' : 1}, 'dog':{'legs' : 4, 'heads' : 1} }
    >>> b = TreeMap(a)
    >>> b.tree()

    +--[ dog ]
    |     \_.--[ legs = 4 ]
    |     \_.--[ heads = 1 ]
    +--[ cat ]
    |     \_.--[ legs = 4 ]
    |     \_.--[ heads = 1 ]


    >>> d = { 'A':{'a':1, 'b':2, 'c':{'d':0, 'e':1}}, 'W':{'x':99, 'y':100} }
    >>> e = TreeMap(d)
    >>> e.tree()

    +--[ A ]
    |     \_.--[ a = 1 ]
    |     +--[ c ]
    |     |     \_.--[ e = 1 ]
    |     |     \_.--[ d = 0 ]
    |     \_.--[ b = 2 ]
    +--[ W ]
    |     \_.--[ y = 100 ]
    |     \_.--[ x = 99 ]

