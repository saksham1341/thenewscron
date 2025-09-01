"""
Base embedder class.
"""

import numpy as np
from typing import List

class AbstractEmbedder:
    def embed(self, i: List[str]) -> List[np.ndarray]:
        """
        Embed the given strings.
        
        Args:
            i (List[str]): Strings to embed.
        """
        
        raise NotImplementedError()
