"""
Abstract Thread Generator
"""

from article import MergedArticle
from globals import StatefulObject
from typing import List

class AbstractThreadGenerator(StatefulObject):
    def generate_threads(self, articles: List[MergedArticle]) -> None:
        raise NotImplementedError()
