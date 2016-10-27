from random import uniform, randint

__rate__ = 1000000

__x__ = bin(__rate__)

__gene__ = __x__[2:].zfill(100) + ('0'*100)

while int(__gene__[0:100], 2) == __rate__:
    __prob__ = 1./int(__gene__[0:100], 2)
    __edit__ = ""
    for n in __gene__:
        if __prob__ >= uniform(0, 1):
            __edit__ += str(randint(0, 1))
        else:
            __edit__ += n
    __gene__ = __edit__
    print __gene__
