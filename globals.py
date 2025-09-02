"""
Collection of global variables.
"""

import threading

class StatefulObject:
    def __init__(self, state: dict) -> None:
        self._state = state

THREADING_LOCK = threading.Lock()
