"""
Base news source class.
"""

from article import Article
from config import MAXIMUM_LATEST_ARTICLES
from globals import StatefulObject
from typing import List

class AbstractNewsSource(StatefulObject):
    def get_latest_articles(max_n: int = MAXIMUM_LATEST_ARTICLES) -> List[Article]:
        raise NotImplementedError()
