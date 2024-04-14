# **可行性报告**

## 小组成员 
* 队长：杨柄权
* 队员：常圣、李岱峰、刘明乐

## 目录

- [**可行性报告**](#可行性报告)
  - [小组成员](#小组成员)
  - [目录](#目录)
  - [**1 概述**](#1-概述)
  - [**2 需求分析**](#2-需求分析)
    - [2.1 优化文件组织](#21-优化文件组织)
    - [2.2 共享存储](#22-共享存储)
    - [2.3 本地与云端相结合](#23-本地与云端相结合)
    - [2.4 文件安全](#24-文件安全)
  - [**3 技术可行性**](#3-技术可行性)
    - [3.1 大语言模型自身优势](#31-大语言模型自身优势)
    - [3.1.1 文本内容深度理解与分析](#311-文本内容深度理解与分析)
    - [3.1.2 文件管理智能化](#312-文件管理智能化)
  - [**4 进度可行性**](#4-进度可行性)
  - [**5 风险评估**](#5-风险评估)
    - [5.1 工作简介](#51-工作简介)
    - [5.2 研究困难](#52-研究困难)
    - [5.3 工作方向](#53-工作方向)
  - [**6 结论和建议**](#6-结论和建议)

## **1 概述**

传统文件系统的设计理念是基于文件的存储和管理，但是随着数据量的增长，文件系统的性能和可扩展性受到了严重的挑战。为了解决这一问题，研究人员提出了基于大模型的文件系统设计理念。大模型是一种基于深度学习的技术，可以对海量数据进行高效的处理和管理。大模型的引入为文件系统的设计提供了新的思路，可以有效地提高文件系统的性能和可扩展性。
<br>
本小组拟在AIOS（即大语言模型智能体操作系统）思想的基础上，在应用和内核层面优化文件索引技术、存储结构和数据备份及恢复技术，以提高文件系统的性能和可靠性。
<br>

![An overview of the AIOS architecture, https://arxiv.org/html/2403.16971v2/x2.png](https://arxiv.org/html/2403.16971v2/x2.png)

<br>

## **2 需求分析**

### 2.1 优化文件组织

LLM根据文件在一定时空内的使用频率确定文件的存储位置，将热点文件存储在高速存储介质上，将冷门文件存储在低速存储介质上，以提高文件的访问速度。并且，LLM可以根据文件的内容和用户的行为进行文件的自动分类和检索，以提高文件的组织和检索效率。

### 2.2 共享存储

实现LLM agents之间的存储共享，以改进模型的决策能力和调度性能。

### 2.3 本地与云端相结合

将本地数据库与云端相结合，引入Next4的快照备份技术，以加强文件系统的数据备份和恢复能力。

### 2.4 文件安全

引入LLM的自然语言处理技术，对文件进行内容分析和风险评估，以提高文件的安全性。

<br>

## **3 技术可行性**

### 3.1 大语言模型自身优势

### 3.1.1 文本内容深度理解与分析

- 自动摘要。大语言模型可以自动提取文本的关键信息，生成文本摘要，以帮助用户快速了解文本内容。以下是使用Transformers库中pipeline模块进行文本摘要的示例代码：

```python

from transformers import pipeline

summarizer = pipeline("summarization")
summarizer(
    """
    America has changed dramatically during recent years. Not only has the number of 
    graduates in traditional engineering disciplines such as mechanical, civil, 
    electrical, chemical, and aeronautical engineering declined, but in most of 
    the premier American universities engineering curricula now concentrate on 
    and encourage largely the study of engineering science. As a result, there 
    are declining offerings in engineering subjects dealing with infrastructure, 
    the environment, and related issues, and greater concentration on high 
    technology subjects, largely supporting increasingly complex scientific 
    developments. While the latter is important, it should not be at the expense 
    of more traditional engineering.

    Rapidly developing economies such as China and India, as well as other 
    industrial countries in Europe and Asia, continue to encourage and advance 
    the teaching of engineering. Both China and India, respectively, graduate 
    six and eight times as many traditional engineers as does the United States. 
    Other industrial countries at minimum maintain their output, while America 
    suffers an increasingly serious decline in the number of engineering graduates 
    and a lack of well-educated engineers.
"""
)
```

```
[{'summary_text': ' America has changed dramatically during recent years . The '
                  'number of engineering graduates in the U.S. has declined in '
                  'traditional engineering disciplines such as mechanical, civil '
                  ', electrical, chemical, and aeronautical engineering . Rapidly '
                  'developing economies such as China and India, as well as other '
                  'industrial countries in Europe and Asia, continue to encourage '
                  'and advance engineering .'}]
```

- 智能回答。在文本内容基础上加以分析，从中检索出相关信息回答用户问题。以下是使用Transformers库中pipeline模块进行问答的示例代码：

```python
from transformers import pipeline

question_answerer = pipeline("question-answering")
question_answerer(
    question="Where do I work?",
    context="My name is Sylvain and I work at Hugging Face in Brooklyn",
)
```

```
{'score': 0.6385916471481323, 'start': 33, 'end': 45, 'answer': 'Hugging Face'}
```

### 3.1.2 文件管理智能化

- 文件组织与检索。大语言模型可以自动分析内容，提取包括主题、人物、地点、时间、事件等关键信息，并根据用户意图、上下文和历史行为等进行智能化组织和推荐。以下是使用Transformers库中pipeline模块进行零样本分类的示例代码：

```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification")
classifier(
    "This is a course about the Transformers library",
    candidate_labels=["education", "politics", "business"],
)
```

```
{'sequence': 'This is a course about the Transformers library',
 'labels': ['education', 'business', 'politics'],
 'scores': [0.8445963859558105, 0.111976258456707, 0.043427448719739914]}
```

从上述运行结果，我们看到，模型将输入文本分类为“education”类别的概率最高，为0.8446。这种零样本分类技术可以应用于文件管理系统中，以实现文件的自动分类和检索。

- 自动化文件管理。大语言模型可以根据用户的行为和历史记录，自动化地对文件存储、备份、恢复和共享，提升用户的工作效率。如，用户在编辑器中输入“保存文件”命令时，模型可以自动将文件保存到云端，并生成文件的快照备份。

- 保障文件安全。一方面，大语言模型可以通过对文件内容进行语义分析来判断文件的风险等级，设置其访问权限；另一方面，模型也可以对用户的文件行为进行监控，及时发现异常行为，保障文件的安全性。下面展示的是使用Transformers库中pipeline模块进行简单的情感分析和命名实体识别的示例代码：

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
classifier("I've been waiting for a HuggingFace course my whole life.")
```

```
[{'label': 'POSITIVE', 'score': 0.9598047137260437}]
```

```python
from transformers import pipeline

ner = pipeline("ner", grouped_entities=True)
ner("My name is Sylvain and I work at Hugging Face in Brooklyn.")
```

```
[{'entity_group': 'PER', 'score': 0.99816, 'word': 'Sylvain', 'start': 11, 'end': 18}, 
 {'entity_group': 'ORG', 'score': 0.97960, 'word': 'Hugging Face', 'start': 33, 'end': 45}, 
 {'entity_group': 'LOC', 'score': 0.99321, 'word': 'Brooklyn', 'start': 49, 'end': 57}
]
```

从上述运行结果，我们看到，模型将输入文本判断为“POSITIVE”情感，且识别出了“Sylvain”为人名、 “Hugging Face”为组织名、 “Brooklyn”为地名。这种情感分析和命名实体识别技术可以应用于文件管理系统中，以实现对文件内容的风险评估和访问控制。

<br>

## **4 进度可行性**

  根据现实情况，我们设计了一系列验证实验，并将在接下来的几天时间内进行验证。

- 实验步骤

> 1. 配置好VMware，准备好Gemini/openai的api，测试网络可行：
 确保在VMware中设置了适当的虚拟机配置，包括内存、CPU和网络设置。
 准备Gemini/OpenAI API的访问凭证，并确保已经正确设置了环境变量或配置文件以便访问API。
 在虚拟机中测试网络连接，包括访问互联网以及Gemini/OpenAI API的连接，以确保网络通畅。
 挑选适合的Linux内核编译器，编译AIOS提供的内核：

> 2. 选择一个适合的编译器，比如GCC或者Clang，以编译AIOS提供的内核源代码。
 下载并配置内核源代码，并根据需求进行自定义配置，例如选择合适的设备驱动和功能模块。
 使用选定的编译器编译内核，并确保编译过程中没有出现错误。
 试用一些自带的syscall来完成文件操作，调查那些相关的SDK：

> 3. 使用一些常见的系统调用（如open、read、write、close等）来完成文件操作，例如创建、读取、写入和关闭文件。
 调查并研究与文件操作相关的系统开发工具包（SDK），如Linux的libc、POSIX标准库等，以便更深入地了解系统调用的使用方法和原理。
 理解新内核syscall的原理，分析优化可行性：

> 4. 详细研究新内核提供的系统调用接口，了解其设计原理和工作机制。
 分析现有系统调用的性能特征和瓶颈，以及可能的优化方向。
 评估优化的可行性，考虑到性能、稳定性和兼容性等方面的因素。
 利用C++或Python进行部分syscall的优化：

> 5. 根据分析结果，选择一些关键的系统调用进行优化，例如文件操作、进程管理等。
 使用C++或Python等编程语言编写优化后的系统调用函数，以提高其性能和效率。
 在进行优化时注意保持系统调用的正确性和可靠性，并进行充分的测试和验证。
 比对优化前后变化，验证通过syscall是否可以高效有序的调用LLM：

> 6. 比较优化前后的性能指标，包括系统调用的响应时间、吞吐量等。
 验证通过系统调用调用LLM（可能是Gemini/OpenAI API）是否可以高效、有序地进行，以确保系统整体性能的提升。
 进行综合性的性能测试和评估，并根据测试结果调整和优化系统调用的实现。

- 验证方法
  
   - 观察AIOS提供的内核是否可用，其大模型集成效果：
  在安装并配置好AIOS提供的内核后，确保系统能够正常启动，并且能够运行常见的任务和应用程序。
测试AIOS内核的大模型集成效果，例如是否能够顺利运行需要大量计算资源和内存的机器学习模型，以及模型的运行性能和准确性如何。
实验新syscall是否可以正常运行，其内置LLM是否可用：

   - 编写简单的程序来测试新的系统调用，确保其可以正常调用并执行所需的功能。
在调用新的系统调用时，观察系统的行为，包括内核日志和系统性能指标，以确保调用过程中没有出现异常或错误。
如果新的系统调用涉及到内置的LLM（例如Gemini/OpenAI API），确保在调用过程中能够正常访问和使用LLM，并且能够获取正确的结果。
对比程序自己编写，主要通过同一文件索引计时对比：

   - 编写自己的程序来执行与新系统调用相同的功能，例如文件操作或LLM访问，并记录执行时间。
使用相同的文件或任务，分别调用新系统调用和自己编写的程序，并记录它们的执行时间。
对比两种方法的执行时间和性能，评估新系统调用的效率和性能优劣。
  

<br>

## **5 风险评估**

从4月9日至4月14日间，本小组通过阅读文献和下载AIOS所提供的开源程序，充分地研究了AIOS在Linux上运行的可行性，并评估了实验的风险。  

### 5.1 工作简介

在过去的一周之内，本小组所有成员均已阅读完毕AIOS相关的重要论文，优先考虑在Linux环境下运行。同时，本小组也没有放弃
AIOS在Windows上运行的可能性。综合考虑之后，本小组分别在vlab，VMware，以及各自笔记本电脑上的Windows系统上下载AIOS的
开源代码并尝试执行。在三种运行环境之下都获得了下载的成功。

### 5.2 研究困难

虽然在三种环境之下都成功的clone了AIOS的仓库，但三种环境都遇到了困难，vlab与VMware上因为AIOS所提供的API无一例外都不支持
中国大陆端口的运行，若要解决这个问题，必须要使用VPN。vlab在学校的服务器上运行，使用学校提供的网络，基本已经断绝了AIOS在
其上运行的希望；而VMware一方，小组成员暂未发现具有可行性的VPN，导致API仍然无法运行。在Windows上，除了前述问题以外，还具有
AIOS在Linux上运行的代码不与Windows环境兼容的问题。  
除却上述实践中遇到的困难，AIOS本身也具有理论上的困难。首先，为了使得大模型的执行结果尽可能的符合人们的期望，它需要十分庞大的
数据集进行训练，AIOS作为一个新兴技术，是否有充分的，可用的，开源的训练集值得怀疑；由本小组四人进行训练集的编写更是不具有可行性。
其次，就算寻找到了有效的训练集，本小组也需要充足的时间和合理的方法对其进行训练，以使得AIOS能够以趋近百分百概率对人的需求做出对应。  
AIOS在应用方面也具有一定的风险。操作系统本身作为管理硬件的程序，其对于计算机的重要程度不言而喻，以AI作为代理运行OS，在
安全性的方面既有优点也有缺点。虽然AI目前的智能程度已经很高程度上能保证数据安全和隐私、监控操作系统的活动并且具有一定的抗
欺诈能力，但是由于其自主性和黑盒性，本地的数据或文件是否真正安全仍然值得商榷。以先前调研过的AutoGPT为例——其具有高度
自主性，仅仅需要人给出目标和要求便可开始执行，但执行过程中完全不过问人类，人类也无法及时知晓其完成目标的手段，所以文件面临被
擅自篡改的风险，并且人类不知道。

### 5.3 工作方向

首先，本小组成员将尽可能快速地解决Linux环境下的VPN使用问题，否则之后的工作将无从谈起。同时本小组的工作重心会放在Linux环境上，
大概率不会再对Windows上的可行性进行探究。  
其次，本小组成员将会尽可能地讨论AIOS的训练问题以及优化的可能性和实施方法，为下一步的行动打好基础，做好铺垫。

<br>

## **6 结论和建议**

经过一个月的调研与讨论，我们发现了目前大模型和OS结合的前沿方向，并获得了前人宝贵的开发经验。在此基础上，我们认为我们可以通过更进一步的开发，增加OS的功能，尤其是文件系统的相关功能。我们设计了实验，打算从AIOS提供的基础版LLM+OS出发，优化一些SDK，并尝试新增一些syscall，来验证我们的工作是可行的，大模型是可以进一步融入文件系统的管理的，相关功能(文件自动归档、依靠大模型搜索文件)是有希望实现的。

<br>