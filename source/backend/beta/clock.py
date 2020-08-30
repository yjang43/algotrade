import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.beta.communicator import Communicator


class Clock(threading.Timer):
    def __init__(self, interval):
        super().__init__(interval, self.time_up)
        self.caller: Communicator = threading.current_thread()

    def time_up(self):
        # Set an alarm to run API feeder, and update since variable in Communicator
        print("clock time's up!")
        self.caller.alarm.set()


