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
