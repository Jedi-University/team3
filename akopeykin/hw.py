from functools import reduce

def exercise_1():
    func = lambda a,b,c: lambda x: [x+a, x+b, x+c]
    f = func("a", "b", "c")
    print(f("x"))


def exercise_2():
    l = [[1,2,3,4,5,6], [0,0,0,0], ["a", "b", "c"]]
    r = reduce(lambda x,y: x+y, l)
    print(r)

def exercise_3():
    def super_range(i):
        n = 0
        while n < i:
            yield n
            n += 1

    for x in super_range(10):
        print(x)

def exercise_4():
    def a(x,y):
        print(f"{x} - {y}")
        
    def caller(func, c, j):
        return lambda x,y: func(c+x, j+y)

    f = caller(a, "100", "200")
    f("h", "z")


import random
def exercise_5():

    class Student():

        def __init__(self, name, age, gender, class_number, speciality):
            self.name = name
            self.age = age
            self.gender = gender
            self.class_number = class_number
            self.speciality = speciality

        def think(self):
            return random.randint(0, 10)

        def speak(self, t):
            return t + 10

        def sum(self, a, b):
            return a + b

    class Lecturer():

        def __init__(self, name, age, gender, speciality, experience):
            self.name = name
            self.age = age
            self.gender = gender
            self.experience = experience
            self.speciality = speciality

        def think(self):
            return random.randint(0, 10)

        def speak(self, t):
            return t + 10 + self.experience

        def answer(self, v):
            return v ** 10