"""
Задание 3 *.
Сделать профилировку для скриптов с рекурсией и сделать описание,
можно ли так профилировать и есть ли 'подводные камни' в профилировании?
Придумать как это решить!
Есть очень простое решение!
"""

from memory_profiler import profile


@profile
def wrapper(length):
    def fib_in_wrap(n):
        if n == 0 or n == 1:
            return n
        else:
            return fib_in_wrap(n - 2) + fib_in_wrap(n - 1)

    print(f'Fibonacci sequence of {length} is {fib_in_wrap(length)}')


'''
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    12     40.4 MiB     40.4 MiB           1   @profile
    13                                         def wrapper(length):
    14     40.4 MiB      0.0 MiB          16       def fib(n):
    15     40.4 MiB      0.0 MiB          15           if n == 0 or n == 1:
    16     40.4 MiB      0.0 MiB           8               return n
    17                                                 else:
    18     40.4 MiB      0.0 MiB           7               return fib(n - 2) + fib(n - 1)
    19                                         
    20     40.4 MiB      0.0 MiB           1       print(f'Fibonacci sequence of {length} is {fib(length)}')
'''


# Для профилирования рекурсии необходимо поместить рекурсию в функцию-обертку, с помощью которой создется только одна
# таблица вызовов. Профилировать так можно, явных "подводных камней" я не вижу


@profile
def fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return fib(n - 2) + fib(n - 1)


# Без обертки на каждый рекурсивный вызов функции будет новая таблица вызовов

wrapper(5)
fib(10)
