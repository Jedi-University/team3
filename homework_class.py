import random

class Person:
    def __init__(self, name, age, gender):
        self.name = name  # устанавливаем имя
        self.age = age  # устанавливаем возраст
        self.gender = gender # устанавливаем пол
 
    def think(self):
        return random.randrange(10)

    def speak(self, t):
        return t + 10

 
class Teacher(Person):
    # определение конструктора
    def __init__(self, name, age, gender, subject, experience):
        Person.__init__(self, name, age, gender)
        self.subject = subject
        self.experience = experience

    # переопределение метода speak
    def speak(self,t):
        return t + 10 + self.experience

    # определение метода answer
    def answer(self, v):
        return v ** 10
        
 
class Student(Person):
    # определение конструктора
    def __init__(self, name, age, gender, num_class, speciality):
        Person.__init__(self, name, age, gender)
        self.num_class = num_class
        self.speciality = speciality

    # определение метода sum
    def sum(self,a,b):
        return a + b

student1 = Student("Tom", 18, 'male', 3, 'BigData')
student2 = Student("Bob", 17, 'male', 2, 'ML')

teacher1 = Teacher('Kate', 25, 'female', 'geography', 4)
teacher2 = Teacher('Maria', 38, 'female', 'chemistry', 17)

print(student1.think())
print(student1.speak(5))
print(student1.sum(3,4))

print()

print(teacher1.think())
print(teacher1.speak(2))
print(teacher1.answer(2))

print(student1.__dict__)

