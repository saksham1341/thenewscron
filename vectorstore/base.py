"""
Abstract Vector Store.
"""

from config import VECTOR_NEAREST_SEARCH_N
import numpy as np
from typing import List, Tuple

class AbstractVectorStore:
    def add_vectors(self, vectors: List[np.ndarray]) -> List[int]:
        """
        Adds vectors to the vector store and returns their indices.
        
        Args:
            vectors (List[np.ndarray]): The vectors to add to the store
        """
        
        raise NotImplementedError()
    
    def remove_vectors(self, idxs: List[int]) -> None:
        """
        Removes vectors from the vector store.
        
        Args:
            idxs (List[int]): Indices of the vectors to remove.
        """
        
        raise NotImplementedError()
    
    def reset(self) -> bool:
        """
        Empty out the vector store.
        """
        
        raise NotImplementedError()
    
    def get_nearest_vectors(self, query_vector: np.ndarray, n: int = VECTOR_NEAREST_SEARCH_N) -> List[Tuple[int, float]]:
        """
        Search the vector store and return maximum of n sorted nearest vector [indexes] to the query vector along with their distance.
        
        Args:
            query_vector (np.ndarray): Query vector.
            n (int): Maximum number of vectors to return.
        """
        
        raise NotImplementedError()
    