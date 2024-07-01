# 使用AC自动机完成多模式串与目标串的匹配，模式串为用户查询文件名，目标串为当前目录中所有文件名
import os
import numpy as np
import queue

class Trie_tree:
    def __init__(self):
        matrix = np.empty((50, 26), dtype=int)
        count = np.empty(50, dtype=int)
        return [matrix, count] 

    def insert(self, target): #AC自动机初始化
        index = 0
        for ch in target:
            ch_value = ch - 'a'
            if self[0][index][ch_value] == 0:
                ch_value = index
                index += 1
            index = self[0][index][ch_value]
        self[1][index] += 1
    
    def build(self):
        q = queue.Queue()
        return_edge = np.empty(50, dtype=int)
        for i in range(0, 26):
            if self[0][0][i]:
                q.put(self[0][0][i])
        while q.empty() == False:
            element = q.get()
            for i in range(0, 26):
                node = self[0][element][i]
                if node:
                    return_edge[node] = self[0][return_edge[element]][i]
                    q.put(node)
                else:
                    self[0][element][i] = self[0][return_edge[element]][i]
    
    def initialize(self, targets):
        for target in targets:
            self.insert(target)
        self.build()
        


def string_compare(target_tree, file_name):
    result = 0
    return result

def string_matching(target_name, file_paths):
    targets = []
    pos = target_name.find(' ')
    while pos != -1:
        targets.append(target_name[0: pos])
        target_name = target_name[pos + 1::]
        pos = target_name.find('_')
    targets.append(target_name)
    target_tree = Trie_tree()
    target_tree.initialize(targets)
    results = []
    for file_name in file_paths:
        if string_compare(target_tree, file_name):
            results.append(file_name)
    return results

