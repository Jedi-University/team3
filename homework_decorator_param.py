#Сделать декоратор, который может считать время выполнения функции
#и выводить его в консоль, нужно сделать возможным передать min=True/False,
#что позволит выводить время в минутах в случае True и в секундах в случае False

import time

def decor_timeit(min):
    def outer(func):
        def wrapper(*args,**kwargs):
            start_time = time.monotonic()
            result = func(*args,**kwargs)
            if min:
                print(round((time.monotonic()-start_time)/60,4), 'minutes')
            else:
                print(round((time.monotonic()-start_time),4), 'seconds')
            return result
        return wrapper
    return outer

@decor_timeit(True)
def create_even_list_min(n):
    time.sleep(n)

@decor_timeit(False)
def create_even_list_sec(n):
    time.sleep(n)


create_even_list_min(6)
create_even_list_sec(6)