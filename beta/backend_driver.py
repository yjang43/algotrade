"""The code helps integration with the main program. It is a driver for
running session, controlling session, and communication with APIs
"""

from beta.communicator import Communicator


class BackendDriver:
    def __init__(self):
        self.communicator = Communicator()

    def start_session(self, session):
        pass

