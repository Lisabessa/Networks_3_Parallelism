import multiprocessing as mp
from functools import partial


def element(i, j, m1, m2):
    res = 0
    for k in range(len(m2)):
        res += m1[i][k] * m2[k][j]
    return res


def write_element(filename_res, len_j, col, value):
    with open(filename_res, 'a+') as file:
        file.write(str(value))
        print(len_j, col)
        if col == len_j - 1:
            file.write('\n')
        else:
            file.write(' ')


def mul_matrix(pool, m1, m2, filename_res):
    num_processes = min(mp.cpu_count(), len(m1) * len(m2[0]))
    pool = mp.Pool(processes=num_processes)
    func = partial(write_element, filename_res, len(m2[0]))
    tasks = [(i, j) for i in range(len(m1)) for j in range(len(m2[0]))]
    print(tasks)

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


work_with_files("1.txt", "2.txt", "res.txt")