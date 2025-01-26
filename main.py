import multiprocessing as mp
from functools import partial
import random
import time


def generate_matrix(size):
    return [[random.randint(1, 100) for _ in range(size)] for _ in range(size)]


def element(i, j, m1, m2):
    res = 0
    for k in range(len(m2)):
        res += m1[i][k] * m2[k][j]
    return res


def write_element(filename_res, len_j, col, value):
    with open(filename_res, 'a+') as file:
        file.write(str(value))
        if col == len_j - 1:
            file.write('\n')
        else:
            file.write(' ')


def mul_matrix(pool, m1, m2, filename_res):
    num_processes = min(mp.cpu_count(), len(m1) * len(m2[0]))
    pool = mp.Pool(processes=num_processes)
    func = partial(write_element, filename_res, len(m2[0]))
    tasks = [(i, j) for i in range(len(m1)) for j in range(len(m2[0]))]

    for task in tasks:
        i, j = task
        pool.apply_async(element, args=(i, j, m1, m2), callback=lambda x, j=j: func(j, x))

    pool.close()
    pool.join()


def work_with_files(filename1, filename2, filename_res):
    try:
        with open(filename1) as file1, open(filename2) as file2:
            m1 = [[int(el) for el in elem.split()] for elem in file1.readlines()]
            m2 = [[int(el) for el in elem.split()] for elem in file2.readlines()]
        if len(m1[0]) != len(m2):
            raise Exception('Incorrect sizes for multiplication!')
        pool = mp.Pool()

        with open(filename_res, 'w') as file:
            file.write('')

        mul_matrix(pool, m1, m2, filename_res)
    except Exception as e:
        print(e.args[0])


def mul_matrix_loop(filename_res, stop_event):
    while True:
        size = random.randint(1, 10)
        m1 = generate_matrix(size)
        m2 = generate_matrix(size)

        num_processes = min(mp.cpu_count(), len(m1) * len(m2[0]))
        pool = mp.Pool(processes=num_processes)
        func = partial(write_element, filename_res, len(m2[0]))
        tasks = [(i, j) for i in range(len(m1)) for j in range(len(m2[0]))]

        with open("matrix1.txt", "a+") as f1, open("matrix2.txt", "a+") as f2:
            for row in m1:
                f1.write(' '.join(map(str, row)) + '\n')
            for row in m2:
                f2.write(' '.join(map(str, row)) + '\n')
            f1.write('\n\n')
            f2.write('\n\n')

        for task in tasks:
            i, j = task
            pool.apply_async(element, args=(i, j, m1, m2), callback=lambda x, j=j: func(j, x))

        pool.close()
        pool.join()

        if stop_event.is_set():
            print('STOP MULTIPLICATION')
            break
        
        with open(filename_res, "a+") as f:
            f.write('\n\n')


def work_with_matrices(filename_res):
    with open("matrix1.txt", "w") as f1, open("matrix2.txt", "w") as f2, open(filename_res, "w") as f3:
        f1.write('')
        f2.write('')
        f3.write('')
        
    stop_event = mp.Event()

    try:
        process = mp.Process(target=mul_matrix_loop, args=(filename_res, stop_event))
        process.start()
        time.sleep(3)
        stop_event.set()
        process.join()
        
    except Exception as e:
        print(e.args[0])


work_with_files("1.txt", "2.txt", "res.txt")  # основные задания
work_with_matrices('results.txt')  # дополнительные задания 