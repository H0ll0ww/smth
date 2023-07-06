from math import pi


class Figures:
    def __init__(self):
        pass

    def area(self):
        pass

    def perimetr(self):
        pass

    def get_values(self):
        pass


class Circle(Figures):
    def __init__(self, radius: float):
        super().__init__()
        self.radius = radius

    def area(self):
        return pi * self.radius ** 2

    def perimetr(self):
        return 2 * pi * self.radius

    def get_values(self):
        return({'radius': self.radius})


class Rectangle(Figures):
    def __init__(self, length, width):
        super().__init__()
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimetr(self):
        return (self.length + self.width) * 2

    def get_values(self):
        return{'length': self.length, 'width': self.width}


class Square(Rectangle):
    def __init__(self, length):
        super().__init__()
        self.length = length
        self.width = length

    def get_values(self):
        return{'length': self.length}

