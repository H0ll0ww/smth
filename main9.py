class Student:
    def __init__(self, age, name, grades: list):
        self.age = age
        self.name = name
        self.grades = grades
    def count_scholarship(self):
        return 5000*sum(self.grades)/len(self.grades)
    def add_grade(self, grade: int):
        self.grades.append(grade)
    def __repr__(self) -> str:
        return f'Student: name - {self.name}, age - {self.age}, grades - {self.grades}'

student = Student(17, 8, [1, 2, 3, 4])
student.add_grade(5)
print(student)