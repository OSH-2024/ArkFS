import queue
import string_storage
import os

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
                src.append(self.type)
                
            elif ref == 1:  # delete
                continue
            elif ref == 2:  # modify
                continue
            elif ref == 3:  # query
                continue
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
        
        return state
