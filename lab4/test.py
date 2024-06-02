import ray
import time
import sys
import numpy as np

ray.init()

matrix_size: int = 10 # 10 * 10 matrix
matrix_mul_times: int = 10000000
if len(sys.argv) < 1:
    pc_num: int = 10 # default value = 10
else:
    pc_num: int = int(sys.argv[1])
node_task_num: int = matrix_mul_times // pc_num


def matrix_mul(matrix1, matrix2):
    return np.matmul(matrix1, matrix2)


@ray.remote
class Worker(object):
    def __init__(self):
        self.size = matrix_size
        self.matrix0 = self.matrix_init2()
        self.res = self.matrix0.copy()
        self.all_times = matrix_mul_times

    def matrix_init2(self):
        # 每行均为正数浮点随机数，单行和为1（归一化）
        matrix = np.random.random((matrix_size, matrix_size))
        for row in range(self.size):
            total = sum(matrix[row])
            for item in matrix[row]:
                item /= total
        # print("Now we have a matrix\n", matrix)
        return matrix

    # 转移矩阵的极限分布
    # 计算若干个矩阵的相乘
    def calculate(self, times):
        # print("I start doing my work.")
        cur_time = time.time()
        task_res = self.matrix0.copy()
        for k in range(times-1):
            task_res = matrix_mul(self.res, self.matrix0)
        # print("I have finished my work, duration: ", time.time() - cur_time)
        return task_res

if __name__ == '__main__':
    cur_time=time.time()
    worker = Worker.remote()
    temps=[]
    for i in range(pc_num):
        temp = worker.calculate.remote(node_task_num)
        temps.append(temp)

    result_list = ray.get(temps)

    result = result_list[0]
    for m in result_list:
        result = matrix_mul(result, m)
    # print("final matrix: \n", result)
    print("total duration: ", time.time() - cur_time)