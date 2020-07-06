import threading
from threading import Condition, Lock, Thread, current_thread
from time import sleep


# class APILock(Lock):
#     def __init__(self, timeout=-1):
#         super().__init__()
#         self.timeout = timeout
#
#         # values that are stored from the api request
#         self.values = {}
#
#     def acquire(self, blocking=True, timeout=-1):
#         is_acquired = super().acquire(blocking, self.timeout)
#         # do api stuff
#         self.do_api_stuff()
#         return is_acquired
#
#     def release(self):
#         return self.values
#
#     def do_api_stuff(self):
#         pass


class T(Thread):
    def __init__(self):
        super().__init__()
        self.parent = current_thread()

    def run(self):
        print("enter to ", self.name)
        sleep(10)
        print("exiting to ", self.parent)


t1 = T()
t2 = T()

t1.start()
sleep(2)
t2.start()

print(threading.enumerate())
