"""
Merged Article
"""

from dataclasses import dataclass

@dataclass
class MergedArticle:
    title: str = None
    total_content: str = None
    score: float = None
    thread: str = None
