# метод super_range, получить из объекта длину для итерирования используя логику генератора, не создаёт массив
# генерирует значение каждый раз при вызове
# def super_range(i):
#   pass
# for x in super_range(100):
#   print(x)




def super_range(i):
    x = 0
    while x < i:
        yield x
        x += 1

for x in super_range(100):
    print(x)