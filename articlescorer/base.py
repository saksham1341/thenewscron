"""
Abstract Article Scorer.
"""

from article import MergedArticle
from dataclasses import dataclass
from globals import StatefulObject
from typing import List

class AbstractArticleScorer(StatefulObject):
    def score_articles(self, articles: List[MergedArticle]) -> None:
        raise NotImplementedError()
