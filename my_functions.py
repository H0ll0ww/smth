import numpy as np
from numpy import sin, cos, tg

def deriv(f, x, h=0.000001):
    return (f(x + h) - f(x - h)) / (2 * h)



def my_function(s, x) -> float:
    s = s.replace(' ', '')
    s = s.replace('^', '**')
    s = s[2:]
    n = len(s) - 1
    for i in range(n):
        if s[i].isdigit():
            if s[i+1] == 'x':
                n += 1
                s = s[:i+1] + '*' + s[i+1:]
        elif s[i] == 'x':
            if s[i+1].isdigit():
                n += 1
                s = s[:i+1] + '*' + s[i+1:]
    return eval(s)

def main():
    x = 3#np.array([2])
    def bounded_function(x): return my_function("y = x**2", x)
    print(deriv(bounded_function, x))

if __name__ == '__main__':
    main()