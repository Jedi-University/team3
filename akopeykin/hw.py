from functools import reduce

def exercise_1():
    f = lambda x: list(map(lambda y: x+y, a))
    a = ["a", "b", "c"]
    print(f("x"))


def exercise_2():
    l = [[1,2,3,4,5,6], [0,0,0,0], ["a", "b", "c"]]
    r = reduce(lambda x,y: x+y, l)
    print(r)
