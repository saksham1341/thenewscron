"""
Merged Article
"""

from dataclasses import dataclass
from typing import List

@dataclass
class MergedArticle:
    title: str = None
    total_content: str = None
    score: float = None
    thread: List[str] = None
    sources: List[str] = None
