"""
Abstract Thread Generator
"""

from article import MergedArticle
from typing import List

class AbstractThreadGenerator:
    def generate_threads(self, articles: List[MergedArticle]) -> None:
        raise NotImplementedError()
