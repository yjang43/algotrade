"""The code helps integration with the main program. It is a driver for
running session, controlling session, and communication with APIs
"""

import queue
from typing import List

from beta.communicator import Communicator
from source.backend.emaSession import EmaSession


# TODO: Long and painful integration process is needed
#       More general Session class needs to be designed
#       What about order_queue and others for param?
class BackendDriver:
    def __init__(self):
        self.communicator = Communicator()
        self.session_container = {}
        self.order_queue = queue.Queue()
        self.algorithm_session_map = {
            'ema': EmaSession,
            # ...
        }

    @staticmethod
    def start_session(session):
        session.run()

    def remove_session(self):
        pass

    def create_session(self, class_name, options: List):
        # get Session class that was mapped in algorithm_session_map
        session_class = self.algorithm_session_map[class_name]
        session = session_class(*options)
        self.session_container[session.session_id] = session
        return session

