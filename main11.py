class SuperTuple(tuple):
    def __new__(cls, args: tuple):
        mass = []
        for x in args:
            mass.append(str(x).upper())
        return args.__new__(cls, mass)

b = SuperTuple(('abc', 'dE1f'))
print(b)