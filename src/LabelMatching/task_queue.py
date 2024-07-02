import queue

class task_queue:
    def __init__(self) -> None:
        self.queue = queue.Queue()

    def push_back(self, task):
        self.queue.put(task)
    
    def pop(self):
        return self.queue.get()

    def clear(self):
        return self.clear()

    def build(self, opcode, tasks):
        counter = 0
        for ch in opcode:
            ref = ord(ch) - ord('0')
            if ref == 0:    # delete
                self.push_back(tasks[counter])
                counter += 1
            elif ref == 1:  # modify
                continue
            elif ref == 2:  # append
                continue
            elif ref == 3:  # query
                continue
            else:
                continue
                
