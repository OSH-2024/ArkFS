# 使用AC自动机完成多模式串与目标串的匹配，模式串为用户查询文件名，目标串为当前目录中所有文件名
import os
import numpy as np

class Trie_tree:
    def __init__(self):
        pass

def Aho_Corasick(targets): #AC自动机构建Trie树
    target_tree = []
    return target_tree

def string_compare(target_tree, file_name):
    result = 0
    return result

def string_matching(target_name, file_paths):
    targets = []
    pos = target_name.find('_')
    while pos != -1:
        targets.append(target_name[0: pos])
        target_name = target_name[pos + 1::]
        pos = target_name.find('_')
    target_tree = Aho_Corasick(targets)
    results = []
    for file_name in file_paths:
        if string_compare(target_tree, file_name):
            results.append(file_name)
    return results

