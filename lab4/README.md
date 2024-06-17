# Lab 4: Ray 的单机部署/分布式部署及性能测试

### 实验简介

在本次实验中，我们小组选择了Ray进行部署，基于FFT算法实现了多项式乘法计算，并使用该程序完成了Ray的测试、分析、评价等工作。

### 测试任务

本次实验选择的测试任务为：计算大样本的方差。

#### 性能指标列表

* 延迟(Latency): 延迟是指在计算系统中，从发起一个操作或请求到操作完成之间的时间间隔。它是衡量系统响应速度和效率的重要指标之一。延迟通常以时间单位（如毫秒、微秒等）来衡量，较低的延迟意味着系统响应更快、效率更高。

* 吞吐量(Throughput): 吞吐量是指在单位时间内处理的任务或者操作数量。它是衡量计算机系统或者网络系统性能的重要指标之一，以单位时间内完成的任务数量来衡量。

* 可靠性(Reliability): 可靠性是指可靠性是指系统在特定时间内能够正常运行而不出现故障的能力。它是衡量系统在各种条件下持续运行的程度，通常包括故障率、可用性、容错能力、可恢复性和持久性等。

* 可扩展性(Scalability): 可扩展性是指系统能够有效地处理和应对增加的工作负载或者请求量而不降低性能的能力。

* 资源利用率(Resource Utilization): 资源利用率是指系统中各种资源（如CPU、内存、磁盘、网络带宽等）被有效利用的程度。资源利用率是衡量系统性能和效率的重要指标之一，它直接影响到系统的响应速度、稳定性和成本效益。

为了体现Ray对计算性能的提高作用，我们选取延迟和吞吐量作为后续测试的主要关注点。

#### 测试程序

测试程序使用python完成, 测试时使用指令 `python3 test.py arg1 arg2 arg3`, 其中参数arg1表示多项式的项数以2为底的对数（默认为16）, arg2表示样本个数（默认为1000）, arg3表示任务的划分个数（默认为10）。为了更好地使用FFT算法, 样本数据采用列表存储，数据由低位到高位对应列表表项由低位到高位。测试程序 `test.py` 如下:
```python
import ray
import time
import sys
import math
import numpy as np

ray.init()

if len(sys.argv) < 2:
    vector_length: int = 16 # default value = 16
else:
    vector_length: int = int(sys.argv[1])
if len(sys.argv) < 3:
    sample_num: int = 1000
else:
    sample_num: int = int(sys.argv[2])
if len(sys.argv) < 4:
    pc_num: int = 10
else:
    pc_num: int = int(sys.argv[3])
vector_size: int = 2 ** vector_length # 2^16-order polynomial
node_task_num: int = sample_num // pc_num

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
    coeff = np.empty(len(p1) * 2, dtype= complex)
    
    for i in range (len(coeff2)):
        coeff[i] = coeff1[i] * coeff2[i]
    res = IFFT(coeff)
    for i in range (len(res)):
        res[i] = np.divide(res[i] , len(res))
    return res

@ray.remote
class Worker(object):
    def __init__(self):
        self.size = vector_size
        self.poly = self.poly_init()
        self.res = self.poly.copy()
        self.all_times = sample_num

    def poly_init(self):
        vector = np.random.randint(0, high = 10, size = vector_size, dtype= int)
        res = np.empty(vector_size, dtype= complex)
        for i in range(vector_size):
            res[i] += vector[i]
        return res

    # 计算 p^2
    def calculate(self, times):
        cur_time = time.time()
        task_res = np.empty(vector_size * 2, dtype= complex)
        for k in range(times):  
            task = self.poly_init()
            task_copy = task.copy()
            task = polyminial_mul(task, task_copy)
            for i in range(len(task)):
                task_res[i] += task[i]
        return task_res

if __name__ == '__main__':
    cur_time=time.time()
    worker = Worker.remote()
    temps=[]
    for i in range(pc_num):
        temp = worker.calculate.remote(node_task_num)
        temps.append(temp)

    result_list = ray.get(temps)

    result = np.empty(vector_size * 2, dtype= complex)
    for m in result_list:
        for i in range(len(m)):  
            result[i] += m[i] 
    print("total duration: ", time.time() - cur_time)
```

### 单机版部署

测试机为USTC Vlab虚拟机，其操作系统为Ubuntu 22.04.4 LTS。

#### 测试流程

* 按照以下步骤安装Ray: 

    - 安装python: 

    ```
    sudo apt-get install python
    ```

    - 使用包管理器安装pip:
    ```
    sudo apt update
    sudo apt install python3-pip
    ```

    如果你希望手动安装最新版本的 pip, 可以使用官方提供的 get-pip.py 脚本。以下是安装步骤: 
    ```
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py # 使用 curl, 或者使用 wget 方法
    wget https://bootstrap.pypa.io/get-pip.py               # 使用 wget
    sudo python3 get-pip.py   # 对于 Python 3
    sudo python get-pip.py    # 对于 Python 2
    ```

    最后使用`pip --version`命令验证是否安装成功

    - 安装Ray
    ```
    pip install -U ray
    pip install 'ray[default]'
    ```

* 使用 `ray start --head` 命令创建`head`节点

* 如果测试程序命名为 `test.py` 且位于当前工作目录下, 使用`python test.py` 或 `python3 test.py`命令运行测试程序

* 运行创建节点命令之后，会出现如下内容: 

```
To monitor and debug Ray, view the dashboard at 
    127.0.0.1:8265
```

在浏览器中输入该ip地址，即可打开Dashboard查看运行结果

* 输入`ray stop`命令结束测试

#### 测试结果


### 分布式部署

#### 测试流程