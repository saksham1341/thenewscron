"""
FAISS Vector Store.
"""

from .base import AbstractVectorStore
from config import VECTOR_STORE_DIMENSION, VECTOR_SIMILAR_SEARCH_N, FAISS_STORE_FILE_NAME
import faiss
import numpy as np

class FAISS(AbstractVectorStore):
    def __init__(self) -> None:
        try:
            self._index = faiss.read_index(FAISS_STORE_FILE_NAME)
        except:
            self._index = faiss.IndexFlatIP(VECTOR_STORE_DIMENSION)
            self._index = faiss.IndexIDMap2(self._index)
        
        self._counter = self._index.ntotal
    
    def get_next_id(self) -> int:
        self._counter += 1
        
        return self._counter - 1
    
    def add_vectors(self, vectors):
        n = len(vectors)
        ids = np.array([self.get_next_id() for i in range(n)])
        vectors = np.array(vectors)
        
        self._index.add_with_ids(
            vectors,
            ids
        )
        
        return ids
    
    def remove_vectors(self, idxs):
        self._index.remove_ids(idxs)
        
    def reset(self):
        self._index.reset()
        self._counter = 0
    
    def get_similar_vectors(self, query_vector, n=VECTOR_SIMILAR_SEARCH_N):
        D, I = self._index.search(
            x=query_vector.reshape(1, VECTOR_STORE_DIMENSION),
            k=n
        )
        
        D = D.tolist()[0]
        I = I.tolist()[0]
        
        return list(zip(I, D))
    
    def save_to_disk(self) -> None:
        faiss.write_index(self._index, FAISS_STORE_FILE_NAME)

if __name__ == "__main__":
    store = FAISS()
    
    # Generate random vectors
    xb = np.random.rand(1000, VECTOR_STORE_DIMENSION)
    ids = store.add_vectors(xb)
    
    # Generate query vector
    xq = np.random.random(VECTOR_STORE_DIMENSION)
    
    # Search nearest five idxs
    result = store.get_nearest_vectors(
        xq,
        5
    )
    
    print(result)
