"""
Base news source class.
"""

from typing import List
from article import Article
from config import MAXIMUM_LATEST_ARTICLES

class AbstractNewsSource:
    def get_latest_articles(max_n: int = MAXIMUM_LATEST_ARTICLES) -> List[Article]:
        raise NotImplementedError()
