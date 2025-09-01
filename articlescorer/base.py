"""
Abstract Article Scorer.
"""

from article import MergedArticle
from dataclasses import dataclass
from typing import List

class AbstractArticleScorer:
    def score_articles(self, articles: List[MergedArticle]) -> None:
        raise NotImplementedError()
