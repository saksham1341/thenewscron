"""
Article module.
"""

from dataclasses import dataclass
import numpy as np

@dataclass
class Article:
    id: str = None
    title: str = None
    link: str = None
    conetnt: str = None
    embedding: np.ndarray = None
    
    def __repr__(self) -> str:
        return f"Article<{self.id}>"

if __name__ == "__main__":
    article = Article(
        id="dfjeicdl",
        title="Hello, World!",
    )
    
    print("Created article:", article)
