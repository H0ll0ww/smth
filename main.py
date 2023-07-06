def choose(s):
    def rectangle(a, b):
        return a*b
    def circle(r):
        return 3.14*r*r
    def square(a):
        return a**2
    def triangle(a, b, c):
        p = a + b + c
        return (p * (p - a) * (p - b) * (p - c))**(1/2)
    if s == 'rectangle':
        return rectangle
    if s=='circle':
        return circle
    if s=='triangle':
        return triangle
    if s=='square':
        return square


s = input()
print(choose(s)(2))