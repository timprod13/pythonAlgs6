"""
Задание 1.

Выполните профилирование памяти в скриптах
Проанализировать результат и определить программы с
наиболее эффективным использованием памяти.

Примечание: Для анализа возьмите любые 3-5 ваших РАЗНЫХ скриптов!
(хотя бы 3 разных для получения оценки отл).
На каждый скрипт вы должны сделать как минимум по две реализации.

Можно взять задачи с курса Основ
или с текущего курса Алгоритмов

Результаты профилирования добавьте в виде комментариев к коду.
Обязательно сделайте аналитику (что с памятью в ваших скриптах, в чем ваша оптимизация и т.д.)

ВНИМАНИЕ: ЗАДАНИЯ, В КОТОРЫХ БУДУТ ГОЛЫЕ ЦИФРЫ ЗАМЕРОВ (БЕЗ АНАЛИТИКИ)
БУДУТ ПРИНИМАТЬСЯ С ОЦЕНКОЙ УДОВЛЕТВОРИТЕЛЬНО

Попытайтесь дополнительно свой декоратор используя ф-цию memory_usage из memory_profiler
С одновременным замером времени (timeit.default_timer())!
"""

from memory_profiler import profile, memory_usage
from functools import reduce


def mem_check(funck):
    def check_funck():
        mem_diff = []
        for i in range(5):
            m_start = memory_usage()
            funck()
            m_end = memory_usage()
            print(f'Memory usage at startup: {m_start}')
            print(f'Memory usage on completion: {m_end}')
            mem_diff.append(m_end[0] - m_start[0])
            print(f'Memory increment: {sum(mem_diff) / 5} Mib')

    return check_funck


@profile
def func_1():
    nums = list(range(50000))
    new_arr = []
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            new_arr.append(i)


''' Вывод:
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    44     20.0 MiB     20.0 MiB           1   @profile
    45                                         def func_1():
    46     21.8 MiB      1.8 MiB           1       nums = list(range(50000))
    47     21.8 MiB      0.0 MiB           1       new_arr = []
    48     23.0 MiB      0.0 MiB       50001       for i in range(len(nums)):
    49     23.0 MiB      0.8 MiB       50000           if nums[i] % 2 == 0:
    50     23.0 MiB      0.3 MiB       25000               new_arr.append(i)
'''


# Самый большой инкремент у nums, процедура требует оптимизации, удаления ссылок на объект списка, далее заменим
# итератор на генератор


@profile
def func_1_optimized():
    nums = [i for i in range(50000)]
    new_arr = [i for i in range(len(nums)) if nums[i] % 2 == 0]
    del nums
    del new_arr


''' Вывод:
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    68     41.9 MiB     41.9 MiB           1   @profile
    69                                         def func_1_optimized():
    70     42.8 MiB      0.9 MiB       50003       nums = [i for i in range(50000)]
    71     43.5 MiB      0.8 MiB       50003       new_arr = [i for i in range(len(nums)) if nums[i] % 2 == 0]
    72     42.8 MiB     -0.8 MiB           1       del nums
    73     42.2 MiB     -0.6 MiB           1       del new_arr
'''


# После оптимизации инкремент уменьшился, удаление ссылок освобождает память с отрицательным значением инкремента


@mem_check
def func_1_mem_check():
    nums = list(range(50000))
    new_arr = []
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            new_arr.append(i)


''' Вывод:
Memory usage at startup: [41.97265625]
Memory usage on completion: [42.01953125]
Memory increment: 0.009375 Mib
Memory usage at startup: [42.01953125]
Memory usage on completion: [42.01953125]
Memory increment: 0.009375 Mib
Memory usage at startup: [42.01953125]
Memory usage on completion: [42.01953125]
Memory increment: 0.009375 Mib
Memory usage at startup: [42.01953125]
Memory usage on completion: [42.0234375]
Memory increment: 0.01015625 Mib
Memory usage at startup: [42.0234375]
Memory usage on completion: [42.0234375]
Memory increment: 0.01015625 Mib
'''


# При использовании декоратора с методом memory_usage по замеру расхода памяти результат первой функции тот же
# (присутствует инкремент)


@mem_check
def func_1_optimized_mem_check():
    nums = [i for i in range(50000)]
    new_arr = [i for i in range(len(nums)) if nums[i] % 2 == 0]
    del nums
    del new_arr


''' Вывод:
Memory usage at startup: [42.0234375]
Memory usage on completion: [42.0234375]
Memory increment: 0.0 Mib
Memory usage at startup: [42.0234375]
Memory usage on completion: [42.0234375]
Memory increment: 0.0 Mib
Memory usage at startup: [42.0234375]
Memory usage on completion: [42.0234375]
Memory increment: 0.0 Mib
Memory usage at startup: [42.0234375]
Memory usage on completion: [42.0234375]
Memory increment: 0.0 Mib
Memory usage at startup: [42.0234375]
Memory usage on completion: [42.0234375]
Memory increment: 0.0 Mib
'''


# После оптимизации видно, что инкремента нет, значит память расходуется оптимально


@profile
def func_2():
    input_list = [i for i in range(50000)]
    string = ""
    for item in input_list:
        string = string + chr(item)
    return string


''' Вывод:
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
   152     42.0 MiB     42.0 MiB           1   @profile
   153                                         def func_2():
   154     42.9 MiB      0.9 MiB       50003       input_list = [i for i in range(50000)]
   155     42.9 MiB      0.0 MiB           1       string = ""
   156     43.8 MiB      0.0 MiB       50001       for item in input_list:
   157     43.8 MiB      0.9 MiB       50000           string = string + chr(item)
   158     43.8 MiB      0.0 MiB           1       return string
'''


@profile
def func_2_optimized():
    string = ""
    for character in map(chr, (i for i in range(50000))):
        string = string + character
    return string


''' Вывод:
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
   176     42.0 MiB     42.0 MiB           1   @profile
   177                                         def func_2_optimized():
   178     42.0 MiB      0.0 MiB           1       string = ""
   179     42.4 MiB      0.0 MiB      150003       for character in map(chr, (i for i in range(50000))):
   180     42.4 MiB      0.5 MiB       50000           string = string + character
   181     42.4 MiB      0.0 MiB           1       return string
'''


# При использовании профилирования, видим, что оптимизованная функция с использованием map и циклом внутри имеет
# меньший инкремент, нежели первая


@mem_check
def func_2_mem_check():
    input_list = [i for i in range(50000)]
    string = ""
    for item in input_list:
        string = string + chr(item)
    return string


''' Вывод:
Memory usage at startup: [42.4296875]
Memory usage on completion: [42.71875]
Memory increment: 0.0578125 Mib
Memory usage at startup: [42.71875]
Memory usage on completion: [42.72265625]
Memory increment: 0.05859375 Mib
Memory usage at startup: [42.72265625]
Memory usage on completion: [42.72265625]
Memory increment: 0.05859375 Mib
Memory usage at startup: [42.72265625]
Memory usage on completion: [42.84765625]
Memory increment: 0.08359375 Mib
Memory usage at startup: [42.84765625]
Memory usage on completion: [42.84765625]
Memory increment: 0.08359375 Mib
'''


@mem_check
def func_2_optimized_mem_check():
    string = ""
    for character in map(chr, (i for i in range(50000))):
        string = string + character
    return string


''' Вывод:
Memory usage at startup: [42.84765625]
Memory usage on completion: [42.84765625]
Memory increment: 0.0 Mib
Memory usage at startup: [42.84765625]
Memory usage on completion: [42.84765625]
Memory increment: 0.0 Mib
Memory usage at startup: [42.84765625]
Memory usage on completion: [42.84765625]
Memory increment: 0.0 Mib
Memory usage at startup: [42.84765625]
Memory usage on completion: [42.84765625]
Memory increment: 0.0 Mib
Memory usage at startup: [42.84765625]
Memory usage on completion: [42.84765625]
Memory increment: 0.0 Mib
'''


# Как и в первом случае, память расходуется оптимально за счет оптимизированного кода


@profile
def func_3():
    return reduce(lambda x, y: x + y, [x ** 2 for x in range(1, 100000 + 1) if x % 2 == 0])


''' Вывод:
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
   259     40.5 MiB     40.5 MiB           1   @profile
   260                                         def func_3():
   261     42.9 MiB      1.2 MiB      200001       return reduce(lambda x, y: x + y, [x ** 2 for x in range(1, 100000 + 1) if x % 2 == 0])
'''


@profile
def func_3_optimized():
    a = 0
    for j in range(100000 + 1):
        if not j % 2:
            a += j ** 2
    return a


''' Вывод:
Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
   277     41.6 MiB     41.6 MiB           1   @profile
   278                                         def func_3_optimized():
   279     41.6 MiB      0.0 MiB           1       a = 0
   280     41.6 MiB      0.0 MiB      100002       for j in range(100000 + 1):
   281     41.6 MiB      0.0 MiB      100001           if not j % 2:
   282     41.6 MiB      0.0 MiB       50001               a += j ** 2
   283     41.6 MiB      0.0 MiB           1       return a
'''


# В этом же случае мы упростили задачу и написали более понятными циклами с условием, избавившись от дополнительной
# сложности, тем самым свели инкремент до нулевого

@mem_check
def func_3_mem_check():
    return reduce(lambda x, y: x + y, [x ** 2 for x in range(1, 100000 + 1) if x % 2 == 0])


''' Вывод:
Memory usage at startup: [41.625]
Memory usage on completion: [41.703125]
Memory increment: 0.015625 Mib
Memory usage at startup: [41.70703125]
Memory usage on completion: [41.71484375]
Memory increment: 0.0171875 Mib
Memory usage at startup: [41.71484375]
Memory usage on completion: [41.72265625]
Memory increment: 0.01875 Mib
Memory usage at startup: [41.72265625]
Memory usage on completion: [41.72265625]
Memory increment: 0.01875 Mib
Memory usage at startup: [41.72265625]
Memory usage on completion: [41.7265625]
Memory increment: 0.01953125 Mib
'''


@mem_check
def func_3_optimized_mem_check():
    a = 0
    for j in range(100000 + 1):
        if not j % 2:
            a += j ** 2
    return a


''' Вывод:
Memory usage at startup: [41.7265625]
Memory usage on completion: [41.7265625]
Memory increment: 0.0 Mib
Memory usage at startup: [41.7265625]
Memory usage on completion: [41.7265625]
Memory increment: 0.0 Mib
Memory usage at startup: [41.7265625]
Memory usage on completion: [41.7265625]
Memory increment: 0.0 Mib
Memory usage at startup: [41.7265625]
Memory usage on completion: [41.7265625]
Memory increment: 0.0 Mib
Memory usage at startup: [41.7265625]
Memory usage on completion: [41.7265625]
Memory increment: 0.0 Mib
'''
# Использование memory_usage лишь подтверждает, что в оптимизированном решении инкремент нулевой


func_1()
func_1_optimized()
func_1_mem_check()
print('_' * 100)
func_1_optimized_mem_check()
func_2()
func_2_optimized()
func_2_mem_check()
print('_' * 100)
func_2_optimized_mem_check()
func_3()
func_3_optimized()
func_3_mem_check()
print('_' * 100)
func_3_optimized_mem_check()
