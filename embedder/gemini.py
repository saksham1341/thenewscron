"""
Gemini Embedder
"""

from .base import AbstractEmbedder
from config import GEMINI_DIMENSION, GEMINI_API_KEYS 
from globals import THREADING_LOCK
from google import genai
import numpy as np

class GeminiEmbedder(AbstractEmbedder):
    def __init__(self, state) -> None:
        super().__init__(state)
        self._clients = [
            genai.Client(api_key=x) for x in GEMINI_API_KEYS
        ]
        
    def _get_client(self):
        with THREADING_LOCK:
            self._state["gemini_current_client_idx"] = (self._state.get("gemini_current_client_idx", -1) + 1) % len(GEMINI_API_KEYS)
            _ = self._state["gemini_current_client_idx"]
        
        return self._clients[_]
    
    def embed(self, i):
        resp = self._get_client().models.embed_content(
            model="gemini-embedding-001",
            contents=i,
            config=genai.types.EmbedContentConfig(
                output_dimensionality=GEMINI_DIMENSION
            )
        )
        
        return [np.array(_.values) for _ in resp.embeddings]

if __name__ == "__main__":
    embedder = GeminiEmbedder({})
    
    print(embedder.embed(["Hello, World!"])[0])
