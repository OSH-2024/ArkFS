import ray
import time
import sys
import math
import numpy as np

ray.init()

if len(sys.argv) < 2:
    vector_length: int = 16 # default value = 10
else:
    vector_length: int = int(sys.argv[1])
if len(sys.argv) < 3:
    poly_mul_times: int = 100
else:
    poly_mul_times: int = int(sys.argv[2])
if len(sys.argv) < 4:
    pc_num: int = 10
else:
    pc_num: int = int(sys.argv[3])
vector_size: int = 2 ** vector_length # 2^16-order polynomial

node_task_num: int = poly_mul_times // pc_num
# print(len(sys.argv))
# print("vector_length: ", vector_length)
# print("poly_mul_times: ", poly_mul_times)
# print(pc_num)
def FFT(p): # Fast Fourier Transform, p the polyminial
    # print(type(p))
    n = int(len(p))
    if n == 1 :
        return p
    w = math.e ** (2 * math.pi * 1j / n)
    pe = p[::2]
    po = p[1::2]
    ye = FFT(pe)
    yo = FFT(po)
    y = np.empty(n, dtype= complex)
    for i in range(0, n // 2):
        y[i] = ye[i] + np.multiply((w**i) , yo[i])
        y[i + n // 2] = ye[i] - np.multiply((w**i) , yo[i])
    return y

def IFFT(p): # Inverse Fast Fourier Transform, p the polyminial
    n = int(len(p))
    if n == 1 :
        return p
    w = math.e ** (-2 * math.pi * 1j / n)
    pe = p[::2]
    po = p[1::2]
    ye = IFFT(pe)
    yo = IFFT(po)
    y = np.empty(n, dtype= complex)
    
    for i in range(0, n // 2):
        
        y[i] = ye[i] + np.multiply((w**i) , yo[i])
        y[i + n // 2] = ye[i] - np.multiply((w**i) , yo[i])
    return y



def polyminial_mul(p1, p2): # coeffs -> FFT, calculate and inverse the result by IFFT
    coeff1 = FFT(p1)
    coeff2 = FFT(p2)
    coeff = np.empty(vector_size * 2, dtype= complex)
    
    for i in range (len(coeff2)):
        coeff[i] = np.multiply(coeff1[i] ,coeff2[i])
    res = IFFT(coeff)
    for i in range (vector_size * 2):
        res[i] = np.divide(res[i] ,( vector_size * 2))
    return res



@ray.remote
class Worker(object):
    def __init__(self):
        self.size = vector_size
        self.poly = self.poly_init()
        self.res = self.poly.copy()
        self.all_times = poly_mul_times

    def poly_init(self):
        vector = np.random.random(size = vector_size)
        print("Now we have a vector\n", vector)
        res = np.empty(vector_size, dtype= complex)
        for i in range(vector_size):
            res[i] += vector[i]
        return res

    # 计算 p^n
    def calculate(self, times):
        # print("I start doing my work.")
        cur_time = time.time()
        task_res = self.poly.copy()
        for k in range(times-1):
            task_res = polyminial_mul(task_res, self.poly)
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
        result = polyminial_mul(result, m)
    # print("final matrix: \n", result)
    print("total duration: ", time.time() - cur_time)