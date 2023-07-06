def compost(*a):
    def funct(x):
        for i in range(len(a) -1 , -1, -1):
            x = a[i](x)
        return x
    return funct

def pl1(x):
    return x + 1


def ymn(x):
    return x * 2


print(compost(pl1, ymn)(2))