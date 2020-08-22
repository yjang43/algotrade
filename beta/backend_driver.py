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
        self.session_count = 0

    @staticmethod
    def start_session(session):
        session.start()

    def create_session(self, class_name, options: List):
        # get Session class that was mapped in algorithm_session_map
        session_class = self.algorithm_session_map[class_name]
        session_id = str(self._session_number_generator())
        session = session_class(session_id, self.order_queue, *options)
        self.session_container[session.session_id] = session
        return session

    def kill_session(self, session_id):
        # TODO: kill_session function of Session class needs to be updated
        #       and uncomment the line under
        # self.session_container[session_id].kill_session()
        self.session_container.pop(session_id)
        pass

    def _session_number_generator(self):
        # generate un-repetitive value
        session_number = self.session_count
        self.session_count += 1
        return session_number
