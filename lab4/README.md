## Lab 4: Ray 的单机部署/分布式部署及性能测试

#### 实验简介

在本次实验中，我们小组选择了Ray进行部署，基于FFT算法实现了多项式乘法计算，并使用该程序完成了Ray的测试、分析、评价等工作。

#### 测试任务

测试程序使用python语言完成，测试时使用指令 `python3 test.py arg1 arg2 arg3`，其中参数arg1表示多项式的项数对2的对数（默认为8），arg2表示多项式的计算次数（默认为100），arg3表示任务的划分个数（默认为10）。测试程序 `test.py` 如下:
```python
import ray
import time
import sys
import math
import numpy as np

ray.init()

if len(sys.argv) < 2:
    vector_length: int = 8 # default value = 10
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

def FFT(p): # Fast Fourier Transform, p the polyminial
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
    coeff = np.empty(vector_size * 2, dtype= complex)
    
    for i in range (len(coeff2)):
        coeff[i] = coeff1[i] * coeff2[i]
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
        cur_time = time.time()
        task_res = self.poly.copy()
        for k in range(times-1):
            task_res = polyminial_mul(task_res, self.poly)
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
    print("total duration: ", time.time() - cur_time)
```