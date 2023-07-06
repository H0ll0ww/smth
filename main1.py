def choose(n):
    def step(x):
        return x**n
    return step

print(choose(int(input()))(2))