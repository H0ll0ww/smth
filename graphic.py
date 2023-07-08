import matplotlib.pyplot as plt
import numpy as np


def my_fucntion(x):
    return x ** 2


x = np.linspace(-10, 10, 100)
y = my_fucntion(x)
plt.plot(x, y)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Graph of y = x^2')


plt.savefig('graph.png')