class Ingridient:
    def __init__(self, calories: float, mass: float) -> None:
        Ingridient.calories = calories
        Ingridient.mass = mass
    def prepare(self) -> float:
        return [self.calories, self.mass]


class Bread(Ingridient):
    def prepare(self) -> float:
        self.calories += 10
        self.mass *= 0.8
        return super().prepare()


class Tomato(Ingridient):
    def __init__(self, calories: float, mass: float, color: str) -> None:
        self.color = color
        super().__init__(calories, mass)
    def prepare(self) -> float:
        self.mass *= 0.7


class soup(Ingridient):
    def __init__(self, calories: float, mass: float, salinity: float) -> None:
        self.salinity = salinity
        super().__init__(calories, mass)


def cook(ings: list[Ingridient]):
    for ing in ings:
        print(ing.prepare())