# 使用AC自动机完成多模式串与目标串的匹配，模式串为用户查询文件名，目标串为当前目录中所有文件名
import os
import numpy as np
import queue


class Trie_tree:
    def __init__(self):
        self.matrix = np.zeros((500, 26), dtype=int)
        self.count = np.zeros(500, dtype=int)
        self.nextp = np.zeros(500, dtype=int)
        self.nodenum = 0

    def insert(self, target): #AC自动机初始化
        index = 0
        for ch in target:
            ch_value = ord(ch) - ord('a')
            # print(index, ch_value)
            if self.matrix[index][ch_value] == 0:
                self.nodenum += 1
                self.matrix[index][ch_value] = self.nodenum
                
            index = self.matrix[index][ch_value]
        self.count[index] += 1
    
    def build(self):
        q = queue.Queue()
        for i in range(0, 26):
            if self.matrix[0][i] != 0:
                q.put(self.matrix[0][i])
        while q.empty() == False:
            element = q.get()
            for i in range(0, 26):
                node = self.matrix[element][i]
                if node:
                    self.nextp[node] = self.matrix[self.nextp[element]][i]
                    q.put(node)
                else:
                    self.matrix[element][i] = self.matrix[self.nextp[element]][i]
    
    def initialize(self, targets):
        for target in targets:
            # print(target)
            self.insert(target)
        self.build()
        # for i in range(50):
        #      for j in range(26):
        #          if self.matrix[i][j] != 0:
        #              print(i, j)
    
    def query(self, file_name):
        result = 0
        pointer = 0
        flist = []
        flist.append(file_name.lower())
        flist = string_divide(flist, '/')
        flist = string_divide(flist, '.')
        flist = string_divide(flist, '_')
        for fname in flist:
            # print(fname)
            for k in fname:
                j = ord(k) - ord('a')
                if j < 0 or j > 200:
                    break
                # print(k, j)
                pointer = self.matrix[pointer][j]
                j = pointer
                while j > 0 and self.count[j] != 0:
                    result += self.count[j]
                    j = self.nextp[j]

        return result

def string_divide(target_names, ch):
    targets = []
    for target_name in target_names:
        pos = target_name.find(ch)
        while pos != -1:
            targets.append(target_name[0: pos])
            target_name = target_name[pos + 1::]
            pos = target_name.find(ch)
        targets.append(target_name)
    return targets




def string_matching(target_name, file_paths):
    targets = []
    target_name = target_name.lower()
    pos = target_name.find(' ')
    while pos != -1:
        targets.append(target_name[0: pos])
        target_name = target_name[pos + 1::]
        pos = target_name.find(' ')
    targets.append(target_name)
    target_tree = Trie_tree()
    target_tree.initialize(targets)
    results = []
    for file_name in file_paths:
        if target_tree.query(file_name) > 0:
            results.append(file_name)
    return results


def main():
    target_name = input()
    folder_path = os.getcwd()
    file_list = [] 
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    results = string_matching(target_name, file_list)
    print(results)


if __name__ == "__main__":
    main()
