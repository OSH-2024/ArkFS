---
theme: default
background: https://cover.sli.dev
title: AIFS, Artificial Intelligence File System
info: 
  中期汇报
class: text-center
highlighter: shiki
drawings:
  persist: false
transition: slide-left
mdc: true
---

# AIFS: Artificial Intelligence File System

## 中期汇报

<br>

汇报人: 杨柄权     

汇报时间: 2024/4/22

<br>

<div style="font-size: 15px">
小组成员：杨柄权、常圣、李岱峰、刘明乐</div>


<div class="fixed bottom-0 right-0">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

---
layout: image-left
image: https://cover.sli.dev
---

# 目录

<Toc minDepth="1" maxDepth="1"></Toc>


--- 
layout: cover
background: https://cover.sli.dev
class: text-center
---

# 项目简介

---
transition: slide-down
level: 2
---

# 项目简介

传统文件系统的设计理念是基于文件的存储和管理，但是随着数据量的增长，文件系统的性能和可扩展性受到了严重的挑战。为了解决这一问题，研究人员提出了基于大模型的文件系统设计理念。大模型是一种基于深度学习的技术，可以对海量数据进行高效的处理和管理。大模型的引入为文件系统的设计提供了新的思路，可以有效地提高文件系统的性能和可扩展性。

最近，研究人员将大模型嵌入操作系统，研究出了AIOS（即大语言模型智能体操作系统），为操作系统的智能化提供了框架。

本小组拟在AIOS思想的基础上，在应用和内核层面优化文件索引技术、存储结构和数据备份及恢复技术，以提高文件系统的性能和可靠性。

--- 
layout: cover
background: https://cover.sli.dev
class: text-center
---

# 项目背景

---
transition: fade-out
level: 2
---


# 项目背景

近年来，大语言模型发展迅猛，已经在许多领域取得了广泛的应用。


<Transform :scale="0.8">

![AI](https://cioctocdo.com/sites/default/files/inline-images/2e8bfd65-5272-4cf1-8b86-954bab975bab_2400x1350.jpg)

</Transform>


--- 
layout: cover
background: https://cover.sli.dev
class: text-center
---

# 理论依据


---
layout: two-cols-header
image: https://cover.sli.dev
level: 2
---

# 理论依据

## Ext4文件系统

Ext4是第四代扩展文件系统，是Linux系统下的日志文件系统，是Ext3文件系统的后继版本。

::left::

ext4文件系统主要由以下几部分组成：

- 超级块（Super Block）：包含文件系统基本信息，例如文件系统类型、块大小、块组数量等。
- 块组描述符（Group Descriptor）：包含每个块组的信息，例如空闲块数量、已分配块数量等。
- 索引节点（Inode）：包含文件或目录的基本信息，例如文件大小、权限、数据块位置等。
- 数据块（Data Block）：存储文件或目录的实际数据。


::right::

<Transform :scale="1.1">

![ext4](https://github.com/OSH-2024/ArkFS/blob/main/pics/ext4.png?raw=true)

</Transform>


---
layout: image-right
image: https://cover.sli.dev
level: 2
---

# 理论依据

## Ext4文件系统

<v-click>

- 向后兼容性 

- 大文件系统 

- 分配方式改进 

- 无限制的子目录 

- 日志校验 

- 在线碎片整理 
  
</v-click>

---
layout: two-cols-header
transition: slide-left
level: 2
---

# 理论依据

## 深度学习

深度学习是机器学习的一个分支，是一种基于对数据进行表征学习的算法。深度学习的核心是神经网络，通过神经网络的层次化结构，可以对数据进行高效的表征学习。

::left::

<Transform :scale="0.9">

![layers](https://github.com/OSH-2024/ArkFS/blob/main/pics/layers.png?raw=true)

</Transform>

::right::

- 通过设计建立适量的神经元计算节点和多层运算层次结构，选择合适的输入层和输出层，通过网络的学习和调优，建立起从输入到输出的函数关系。

<br>

- 使用训练成功的网络模型，就可以实现我们对复杂事务处理的自动化要求。

--- 
layout: cover
background: https://cover.sli.dev
class: text-center
---

# 技术可行性

---
transition: slide-up
level: 2
---

# 技术可行性

## 大语言模型

<br>

#### 文本内容深度理解与分析

<br>

- 自动摘要


```python
[{'summary_text': ' America has changed dramatically during recent years . The '
                  'number of engineering graduates in the U.S. has declined in '
                  'traditional engineering disciplines such as mechanical, civil '
                  ', electrical, chemical, and aeronautical engineering . Rapidly '
                  'developing economies such as China and India, as well as other '
                  'industrial countries in Europe and Asia, continue to encourage '
                  'and advance engineering .'}]
```

---
level: 2
---

# 技术可行性

## 大语言模型

<br>

#### 文本内容深度理解与分析

<br>

- 智能回答
  

```python
from transformers import pipeline

question_answerer = pipeline("question-answering")
question_answerer(
    question="Where do I work?",
    context="My name is Sylvain and I work at Hugging Face in Brooklyn",
)
```

```python
{'score': 0.6385916471481323, 'start': 33, 'end': 45, 'answer': 'Hugging Face'}
```


---
level: 2
---

# 技术可行性

## 大语言模型

<br>

#### 文件管理智能化

<br>

- 文件组织与检索
  

```python
from transformers import pipeline

classifier = pipeline("zero-shot-classification")
classifier(
    "This is a course about the Transformers library",
    candidate_labels=["education", "politics", "business"],
)
```

```python
{'sequence': 'This is a course about the Transformers library',
 'labels': ['education', 'business', 'politics'],
 'scores': [0.8445963859558105, 0.111976258456707, 0.043427448719739914]}
```


---
level: 2
---

# 技术可行性

## 大语言模型

<br>

#### 文件管理智能化

<br>

- 文件安全与权限控制


````md magic-move

//step 1
```python {1-4|6}
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
classifier("I've been waiting for a HuggingFace course my whole life.")

[{'label': 'POSITIVE', 'score': 0.9598047137260437}]
```

//step 2
```python{1-4|6-8}
from transformers import pipeline

ner = pipeline("ner", grouped_entities=True)
ner("My name is Sylvain and I work at Hugging Face in Brooklyn.")

[{'entity_group': 'PER', 'score': 0.99816, 'word': 'Sylvain', 'start': 11, 'end': 18}, 
 {'entity_group': 'ORG', 'score': 0.97960, 'word': 'Hugging Face', 'start': 33, 'end': 45}, 
 {'entity_group': 'LOC', 'score': 0.99321, 'word': 'Brooklyn', 'start': 49, 'end': 57}
]
```
````

---
level: 2
---

# 技术可行性

## AIOS

<br>

AIOS是一种LLM智能体操作系统，将大语言模型嵌入操作系统（OS）作为OS的大脑，实现了``有灵魂''的操作系统，即能够独立运行、做出决策和执行任务而无需或需要最少的人工干预的系统。这些代理旨在理解指令、处理信息、做出决策并采取行动以实现自主状态。

<br>

<Transform :scale="0.8">

![AIOS](https://github.com/OSH-2024/ArkFS/blob/main/doc/feasibility_report/src/example.png?raw=true)

</Transform>



---
level: 2
---

# 技术可行性

## AIOS

<br>

此外，AIOS为用户提供了AIOS SDK，一个丰富的工具包来抽象较低级别系统功能的复杂性，从而允许开发代理应用程序。这使开发人员能够专注于其代理的基本逻辑和功能，从而促进更高效的开发过程。AIOS SDK组成了AIOS的Application Kernel，是用户与OS直接交互的接口。


<Transform :scale="0.6">

![sdk](https://github.com/OSH-2024/ArkFS/blob/main/doc/feasibility_report/src/sdk.png?raw=true)

</Transform>

---
level: 2
---

# 技术可行性

## AIOS

在实现文件存储方面，AIOS使用内存管理器和存储管理器分别处理短期快速存储和长期存储的文件管理。

<br>

- 内存管理器管理代理生命周期内的短期内存，确保只有在代理处于活动状态（等待执行或运行时）时才能存储和访问数据。
  
  未来可以考虑将更复杂的内存机制（如代理之间的共享内存池或分层缓存）集成到AIOS中。内存管理器实现了快速的数据检索和处理，有助于对用户查询和交互做出快速响应，而不会给AIOS的存储带来过重负担。

- 存储管理器负责数据的长期保存，监督需要无限期保留的信息的存储，这些信息超过了任何单个代理的活动寿命。
  
  AIOS中的这种永久存储是通过各种耐用介质实现的，如本地文件、数据库或基于云的解决方案，确保数据的完整性和可用性，以供未来参考或分析。存储管理器支持检索扩充。通过存储用户偏好和维护历史交互日志，存储管理器可以丰富代理知识更新，增强长期用户体验。


---
level: 2
---

# 技术可行性

## AIOS

<br>

目前，LLM内核中的LLM系统调用接口提供了基本的LLM调用操作功能，包括代理管理、上下文处理、内存和存储操作以及访问控制。这个接口充当了复杂代理请求和不同内核模块执行之间的桥梁。LLM系统调用列表将来可以进一步扩展，以支持更多操作。


<Transform :scale="0.45">

![syscall](https://github.com/OSH-2024/ArkFS/blob/main/doc/feasibility_report/src/syscall.png?raw=true)

</Transform>

--- 
layout: cover
background: https://cover.sli.dev
class: text-center
---

# 风险与挑战

---
transition: slide-down
level: 2
---

# 风险与挑战

### 眼下困境

<br>

- ip限制，无法获得预期结果


<Transform :scale="1.0">

![lockdown](https://github.com/OSH-2024/ArkFS/blob/main/pics/9d14a80eddd3d4ede70631adb6e3f7d4.png?raw=true)

</Transform>

---
transition: fade-out
layout: two-cols
level: 2
---

# 风险与挑战

### 中长期挑战

- 大模型训练集难以获得，训练成本较高

- 接口优化能否实现，如何实现

- 文件系统如何设计，如何优化

<br>

### 应用风险

- AI暂不能100%理解人类意图，执行结果差强人意  

- AI黑盒，人类不知晓执行过程，本地文件面临风险  

--- 
layout: cover
background: https://cover.sli.dev
class: text-center
---

# 进度与计划


---
transition: slide-up
level: 2
---

# 进度与计划

根据现实情况，我们设计了一系列验证实验，并将在接下来的几个月内进行验证。

### 已完成

<br>

配置好VMware，在合适的环境下使用API_Key编译AIOS提供的内核源代码。

---
level: 2
---

### 已完成

![res1](https://github.com/OSH-2024/ArkFS/blob/main/pics/fengli-4.20-4.png?raw=true)

---
level: 2
---

### 已完成

![res2](https://github.com/OSH-2024/ArkFS/blob/main/pics/fengli-4.20-5.png?raw=true)

---
level: 2
---

### 已完成

![res3](https://github.com/OSH-2024/ArkFS/blob/main/pics/fengli-4.20-6.png?raw=true)


---
level: 2
---

### 已完成

![res4](https://github.com/OSH-2024/ArkFS/blob/main/pics/fengli-4.20-7.png?raw=true)


---
level: 2
---

### 已完成

![res5](https://github.com/OSH-2024/ArkFS/blob/main/pics/fengli-4.20-8.png?raw=true)


---
level: 2
---

# 进度与计划

### 待完成

- 探索尝试


根据分析结果，选择一些关键的系统调用进行优化，我们将把精力集中在文件管理上，编写优化系统调用函数，以提高其性能和效率。

- 近期展望
  
编写简单的程序来测试新的系统调用，确保其可以正常调用并执行所需的功能。

比较优化前后的性能指标，包括系统调用的响应时间、吞吐量等。进行综合性的性能测试和评估，并根据测试结果调整和优化系统调用的实现。

- 远景目标
   
实现一个可以智能调用的，可以代替人工操作的，新一代文件管理系统。例如无需用户操作的自动存储，文件自动存储到用户指定位置或大模型认定的"文件相关"位置。

--- 
layout: cover
background: https://cover.sli.dev
class: text-center
---

# 结论

--- 
transition: slide-up
level: 2
---

# 结论

<br>

经过一个月的调研与讨论，我们发现了目前大模型和OS结合的前沿方向，并获得了前人宝贵的开发经验。在此基础上，我们可以通过更进一步的开发，增加OS的功能，尤其是文件系统的相关功能。

<br>
  
我们设计了实验，打算从AIOS提供的基础版LLM+OS出发，优化一些SDK，并尝试新增一些syscall，来验证我们的工作是可行的，大模型是可以进一步融入文件系统的管理的，相关功能(文件自动归档、依靠大模型搜索文件)是有希望实现的。同时，我们相信合理实现大模型的调用、正确使用其功能，对文件系统乃至整个操作系统都会带来性能的提升！

--- 
layout: cover
background: https://cover.sli.dev
class: text-center
level: 2
---

# Thanks for listening!
