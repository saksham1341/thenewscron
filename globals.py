"""
Collection of global variables.
"""

class StatefulObject:
    def __init__(self, state: dict) -> None:
        self._state = state
