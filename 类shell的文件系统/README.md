# 根据5.30会议精神，该目录下为近期工作

##  1.动态能力--李岱峰

整个程序应该在一种全动态的情况下运行在系统底层，意味着每次增删改查都对应一系列操作。

在增删改的情况下，我们不可避免的会遇到documents的更改，意味着聚类的变化。新的聚类应该最大程度的避免旧文件的移动，我认为应该采取投放的方式，如果新文件符合原有的聚类，就将新文件投放到就聚类里，否则新建一个聚类，这样可以避免已经存在的聚类不断改变，减少开销。

我将程序改造为了shell的形式，命令行操作来展示增删改查的操作方式。


初始的情况下，可以设置5个聚类，但随着文档增多，聚类也可以变得更多。我设计为每个聚类中的信息必须相近度达到一定程度，否则可以新增一个聚类。这样来动态维护聚类，相应的，增加一个聚类意味着新的树根，而一个聚类里新的文件索引意味着一个新的树结点。

##  2.第一次文本学习能力--李岱峰

我在6.1更新--6.1update.py中为程序添加了第一次初始化前，对目标文件夹target_folder中的所有内容进行文本学习的能力，用于维护documents，完成了开会内容的第二部分。

所有大模型本地运行。支持文本文件测试，图片文件有待测试。

##  3.多层数据索引结构--李岱峰

6.2更新 6.2update.py中，我完成了多层聚类的设计，即在每个桶里加入更小的桶。输出的结构请看117行，155行。

## 4.输出对齐--李岱峰

6.13更新，6.13update.py中，我删除了不必要的io，添加了多核心并发处理程序，并将输出与刘明乐同学、杨柄权同学需要的输入对齐。修复图片内容提取失败的bug。

## 5.数据结构建立--刘明乐

6.27更新，李岱峰同学建立好聚类之后，由本人和杨柄权同学建立存储用的数据结构。经过前期讨论确定由本人建立
以聚类层级和关键字为依据的森林，森林中的每一棵树都代表一个Level1级别的聚类，树中的节点数据域存储
本层级的关键字和index。但仅有最下层的聚类中index为有效值。

## 6.27-bug修复-李岱峰

我修复了view和save的bug，目前每层输出都为全局index，并且有打印representative word。

## 6.28-ret添加-李岱峰

我添加了
![通用返回接口](./src/通用返回接口.png)
这是ret_clusters函数的返回值，其他人可以使用这个进行操作。


## 6.28-关键字树建立成功-刘明乐

本人成功使得关键字树的输入和李岱峰同学的输出对接，成功且正确地建立了关键字树
并且在树中加入了建立，遍历，销毁以及更新的功能。等待其余小组成员对我产生其他需求
目前进入待机状态。

## 6.28-基于AC自动机的文件查找-杨柄权

为了提供使用文件名查找对应文件的方法，我选择使用AC自动机算法：将目标文件名定为模式串，将当前所在文件夹中的所有文件定义为目标串，将模式串切分后建立Trie树，再将所有目标串与模式串进行比对，返回所有匹配成功的目标串。
目前已完成Trie树的初始化。待完成部分：字符串匹配。

## 6.29-时间和文本类型的添加--李岱峰

[[1, ['diagram', 'the', 'of'], [(0, 1713275347.023852, 'img', 'a computer tower with a blue light shining on it'), (2, 1714214477.0871334, 'img', 'a diagram of the system'), (8, 1714214477.097888, 'img', 'a diagram of a network with several dots'), (13, 1713275562.494238, 'img', 'the new interface in the new interface editor')]], [2, ['system', 'diagram', 'the'], [(8, 1714214477.097888, 'img', 'a diagram of a network with several dots')]], [2, ['sheets', 'background', 'paper'], [(13, 1713275562.494238, 'img', 'the new interface in the new interface editor')]], [2, ['shining', 'light', 'computer'], [(0, 1713275347.023852, 'img', 'a computer tower with a blue light shining on it')]], [2, ['gpa', 'this', 'test'], [(2, 1714214477.0871334, 'img', 'a diagram of the system')]], [1, ['you', 'iq', 'this'], [(10, 1717255847.0698338, 'txt', "This is a test for liumingle's IQ. If you think you have a high IQ, try this test.")]], [1, ['ich', 'nicht', 'die'], [(3, 1713275347.039931, 'img', 'a pile of paper sheets with a blue background'), (4, 1718022455.3486648, 'txt', '"Ich muss eine neue Jacke für das Jobinterview am Diestag kaufen"'), (5, 1718022455.3495991, 'txt', '"Ich brauche die Jeans für meinen Vater, und ich muss einen neue schuhe kaufen"'), (6, 1718022455.3495991, 'txt', '"Ich brauche die Jeans nicht. Ich brauches die jeans nicht" - Jürgen Schubert. Schulder: "Ich habe ein gutes Leben."'), (7, 1718022455.3495991, 'txt', '"Wir brauchen der stuhl nicht, denn wir haben drei Stühle"')]], [2, ['system', 'diagram', 'the'], [(5, 1718022455.3495991, 'txt', '"Ich brauche die Jeans für meinen Vater, und ich muss einen neue schuhe kaufen"')]], [2, ['gpa', 'this', 'test'], [(4, 1718022455.3486648, 'txt', '"Ich muss eine neue Jacke für das Jobinterview am Diestag kaufen"')]], [2, ['shining', 'light', 'computer'], [(3, 1713275347.039931, 'img', 'a pile of paper sheets with a blue background')]], [2, ['diestag', 'jacke', 'am'], [(7, 1718022455.3495991, 'txt', '"Wir brauchen der stuhl nicht, denn wir haben drei Stühle"')]], [2, ['sheets', 'background', 'paper'], [(6, 1718022455.3495991, 'txt', '"Ich brauche die Jeans nicht. Ich brauches die jeans nicht" - Jürgen Schubert. Schulder: "Ich habe ein gutes Leben."')]], [1, ['this', 'is', 'for'], [(1, 1717255895.5607598, 'txt', "This is a test for changsheng's GPA. this is atest for chang sheng's GDP. this will be a test to see how well they can manage their GPA."), (9, 1717255869.4116726, 'txt', "This is a test for lidaifeng's EQ. this is a tests for lidetefeng's quality of life. i.e. it's a test to see if we can live up to our expectations."), (11, 1713275347.0590267, 'img', 'a laptop with a red heart on the screen'), (14, 1717255955.6176527, 'txt', "This is a test for yangbingquan's score. this is a Test for yingbingquans score."), (15, 1717256551.3271585, 'txt', "This is a test for zhoubohan's homework. this is atest for z houbohan’s homework. This is a Test for ZHoubohan.")]], [2, ['system', 'diagram', 'the'], [(11, 1713275347.0590267, 'img', 'a laptop with a red heart on the screen')]], [2, ['sheets', 'background', 'paper'], [(14, 1717255955.6176527, 'txt', "This is a test for yangbingquan's score. this is a Test for yingbingquans score.")]], [2, ['gpa', 'this', 'test'], [(9, 1717255869.4116726, 'txt', "This is a test for lidaifeng's EQ. this is a tests for lidetefeng's quality of life. i.e. it's a test to see if we can live up to our expectations.")]], [2, ['diestag', 'jacke', 'am'], [(15, 1717256551.3271585, 'txt', "This is a test for zhoubohan's homework. this is atest for z houbohan’s homework. This is a Test for ZHoubohan.")]], [2, ['shining', 'light', 'computer'], [(1, 1717255895.5607598, 'txt', "This is a test for changsheng's GPA. this is atest for chang sheng's GDP. this will be a test to see how well they can manage their GPA.")]], [1, ['he', 'to', 'if'], [(12, 1718022455.3495991, 'txt', "This is a test for shixufei's wis adel to see if he can do it. If he fails, he will be sent to prison.")]]]

现在的ret标准返回。 --update0629.py