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

测试程序使用python完成, 测试时使用指令 `python3 test.py arg1 arg2 arg3`, 其中参数arg1表示多项式的项数以2为底的对数（默认为16）, arg2表示样本个数（默认为1000）, arg3表示任务的划分个数（默认为50000）。为了更好地使用FFT算法, 样本数据采用列表存储，数据由低位到高位对应列表表项由低位到高位。测试程序 `test.py` 如下:
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
    pc_num: int = 50000
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
        task_res = []
        square_sum = np.empty(vector_size * 2, dtype= complex)
        sum = np.empty(vector_size, dtype= int)
        for k in range(times): 
            task = self.poly_init()
            task_copy = task.copy()
            for i in range(len(task)):
                sum[i] += task[i]
            task = polyminial_mul(task, task_copy)
            for i in range(len(task)):
                square_sum[i] += task[i]
        task_res.append(sum, square_sum)
        return task_res

if __name__ == '__main__':
    cur_time=time.time()
    worker = Worker.remote()
    temps=[]
    for i in range(pc_num):
        temp = worker.calculate.remote(node_task_num)
        temps.append(temp)

    result_list = ray.get(temps)

    rsquare_sum = np.empty(vector_size * 2, dtype= complex)
    rsum = np.empty(vector_size * 2, dtype= complex)
    result = 0
    for m in result_list:
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

测试结果截图见result.md。

| 多项式项数 | 总吞吐量 | pc_num = 1 | pc_num = 10 | pc_num = 100 | pc_num = 1000 | pc_num = 10000 | pc_num = 50000 |
|-------|-------|-------|-------|-------|-------|-------|-------|
| 256 | 100000 | 611.6088 | 615.0404 | 622.7523 | 617.4893 | 673.1099 | 704.8914 |
| 16 | 500000 | 151.6565 | 158.4516 | 156.1609 | 153.4860 | 161.6348 | 171.9120 |

由上表可得，当任务划分数小于1000时，其对程序延迟的影响很小，而当任务划分数大于10000时，程序延迟明显增大，我们认为任务数量的增加导致进程间开销增大，显著降低了运行效率，因此需要取一个较小的任务划分数。

使用 `no_ray.py` 测试不使用Ray进行部署时, 总吞吐量为 500000 的程序延迟, 并与上表数据作对比统计如下:

|  | 总吞吐量 | pc_num = 1 | pc_num = 10 | pc_num = 100 | pc_num = 1000 | pc_num = 10000 | pc_num = 50000 |
|-------|-------|-------|-------|-------|-------|-------|-------|
| 不使用 Ray 部署 | 500000 | 152.3679 | 152.1764 | 152.4549 | 149.3331 | 153.9519 | 156.5193 |
| 使用 Ray 部署 | 500000 | 151.6565 | 158.4516 | 156.1609 | 153.4860 | 161.6348 | 171.9120 |

由上表可得，Ray 的单机部署在一定程度上增大了程序的运行时间，产生了额外的开销; 任务划分数取 1000 时程序延迟较小，相较于默认的 pc_num = 50000时提高了 10.66% 的运行效率，因此选定 pc_num = 1000 作为后续测试的参数值。

计算以上测试数据的吞吐量（单位: 任务数量/秒）如下:

|  | 多项式项数 | 总吞吐量 | pc_num = 1 | pc_num = 10 | pc_num = 100 | pc_num = 1000 | pc_num = 10000 | pc_num = 50000 |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| 不使用 Ray 部署 | 16 | 500000 | 3281.53 | 3285.66 | 3279.66 | 3348.22 | 3247.77 | 3194.49 |
| 使用 Ray 部署 | 256 | 100000 | 163.50 | 162.59 | 160.58 | 161.95 | 148.56 | 141.87 |
| 使用 Ray 部署 | 16 | 500000 | 3296.92 | 3155.54 | 3201.83 | 3257.63 | 3093.39 | 2908.46 |

考虑到多项式项数较大时程序运行时间过长, 吞吐量较小, 不利于后续实验的数据统计, 因此选定多项式项数为8作为后续测试的对应参数值。

### 分布式部署

#### 测试流程