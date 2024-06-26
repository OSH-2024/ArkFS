import time
import sys
import math
import numpy as np

if len(sys.argv) < 2:
    vector_length: int = 16 # default value = 16
else:
    vector_length: int = int(sys.argv[1])
if len(sys.argv) < 3:
    sample_num: int = 1000
else:
    sample_num: int = int(sys.argv[2])
if len(sys.argv) < 4:
    pc_num: int = 50000
else:
    pc_num: int = int(sys.argv[3])
vector_size: int = 2 ** vector_length # 2^16-order polynomial

node_task_num: int = sample_num // pc_num

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
        y[i] = ye[i] + (w**i) * yo[i]
        y[i + n // 2] = ye[i] - w**i * yo[i]
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
        
        y[i] = ye[i] + (w**i) * yo[i]
        y[i + n // 2] = ye[i] - w**i * yo[i]
    return y

def polyminial_mul(p1, p2): # coeffs -> FFT, calculate and inverse the result by IFFT
    coeff1 = FFT(p1)
    coeff2 = FFT(p2)
    coeff = np.empty(len(p1) * 2, dtype= complex)
    
    for i in range (len(coeff2)):
        coeff[i] = coeff1[i] * coeff2[i]
    res = IFFT(coeff)
    for i in range (len(res)):
        res[i] = np.divide(res[i] , len(res))
    return res

class Worker(object):
    def __init__(self):
        self.size = vector_size
        self.poly = self.poly_init()
        self.res = self.poly.copy()
        self.all_times = sample_num

    def poly_init(self):
        vector = np.random.randint(0, high = 10, size = vector_size, dtype= int)
        # print("Now we have a vector\n", vector)
        return vector

    # 计算 p^2
    def calculate(self, times):
        # print("I start doing my work.")
        cur_time = time.time()
        task_res = []
        square_sum = np.empty(vector_size * 2, dtype= complex)
        sum = np.empty(vector_size, dtype= int)
        for k in range(times): 
            task = self.poly_init()
            c_task = np.empty(vector_size, dtype= complex)
            for i in range(len(task)):
                c_task[i] += task[i]
                sum[i] += task[i]
            task_copy = c_task.copy()
            c_task = polyminial_mul(c_task, task_copy)
            for i in range(len(c_task)):
                square_sum[i] += c_task[i]
        task_res.append(sum) 
        task_res.append(square_sum)
        # print("I have finished my work, duration: ", time.time() - cur_time)
        return task_res

if __name__ == '__main__':
    cur_time=time.time()
    worker = Worker()
    temps=[]
    for i in range(pc_num):
        temp = worker.calculate(node_task_num)
        temps.append(temp)

    rsquare_sum = np.empty(vector_size * 2, dtype= complex)
    rsum = np.empty(vector_size * 2, dtype= complex)
    result = 0
    for m in temps:
        for i in range(len(m[0])):  
            rsum[i] += m[0][i] 
        for i in range(len(m[1])):  
            rsquare_sum[i] += m[1][i] 
            result += m[1][i] * (10 ** i)
    result /= sample_num
    ex = 0
    for i in range(len(rsum)):  
        ex += rsum[i] 
    ex /= sample_num
    result -= ex ** 2
    # print("final vector: \n", result)
    print("total duration: ", time.time() - cur_time)