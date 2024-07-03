import queue
import string_storage
import os
import numpy as np
from search.file_add import my_add
from search.file_delete import my_delete
from search.file_search import my_search

index = "default"

class task_queue:
    def __init__(self, src) -> None:
        self.time = src[0]
        self.type = src[1]
        self.opcode = src[3]
        self.srcs = queue.LifoQueue()
        self.srcs.put(src[2][1])
        self.srcs.put(src[2][0])


    def push(self, src):
        self.srcs.put(src)
    
    def pop(self):
        return self.srcs.get()

    def clear(self):
        return self.srcs.empty()
    
      
    def execute(self):
        state = 0
        for ch in self.opcode:
            ref = ord(ch) - ord('0')    # operation code
            if ref == 0:    # append
                src = []
                src.append(self.pop())
                src.append(self.pop())
                if len(self.type) == 0:
                    src.append(1)
                else:
                    src.append(0)
                name = np.random.randint()
                src.append(str(name) + self.type)
                state = my_add(src) # Error code

            elif ref == 1:  # delete
                src = self.pop()
                state = my_delete(src)
            elif ref == 2:  # modify
                continue
            elif ref == 3:  # query
                src = []
                time = []
                for i in range(0,2):
                    if self.time[i] == 'NULL':
                        time.append(None)
                    else:
                        time.append(self.time[i])
                src.append(time)
                feature = self.pop()
                if feature == 'NULL':
                    src.append(None)
                else:
                    src.append(feature)
                src.append(index)   # <- 演示目录
                src_list = my_search(src)


            elif ref == 4:  # accurate query
                target_name = self.pop()
                folder_path = os.getcwd()       # or address input from user (haven't finished yet)
                file_list = [] 
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_list.append(file_path)
                results = string_storage.string_matching(target_name, file_list)
                if len(results) == 0:
                    state = 4   # Error code "4": No file matching
                    break
                self.push(results)
            else:
                continue
            if state != 0:
                break
        return state
