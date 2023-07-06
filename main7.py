import random


class Human:
    genom_count = 46
    def __init__(self, name, age, description):
        self.name = name
        self.age = age
        self.description = description
    def show_discription(self):
        print(self.name, self.age, self.description)
    @classmethod
    def get_genom_count(cls):
        return cls.genom_count
    @classmethod
    def set_genom_count(cls, count: int):
        cls.genom_count = count
    @staticmethod
    def choise_name():
        return random.choice((1,1,1,1,1,1,0))


human = Human(1, 1, 1)
print(human.choise_name())