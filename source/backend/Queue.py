#based off queue class
#FIFO
#dequeue everything once clock signal comes in
#make program synchronous

class Queue:

    def __init__(self):
        self.Queue = []

    def enqueue(self, item):
        self.Queue.append(item)

    def dequeue(self):
        if len(self.Queue) < 1:
            return None
        return self.Queue.pop(0)

    def size(self):
        return len(self.Queue) 

    def isEmpty(self):
        return len(self.Queue) == 0
