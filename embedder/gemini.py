"""
Gemini Embedder
"""

from .base import AbstractEmbedder
from config import GEMINI_DIMENSION, GEMINI_API_KEY  # Not used directly, just makes sure it is present in the environment 
from google import genai
import numpy as np

class GeminiEmbedder(AbstractEmbedder):
    def __init__(self) -> None:
        self._client = genai.Client()
    
    def embed(self, i):
        resp = self._client.models.embed_content(
            model="gemini-embedding-001",
            contents=i,
            # config=genai.types.EmbedContentConfig(
            #     output_dimensionality=GEMINI_DIMENSION
            # )
        )
        
        return [np.array(_.values) for _ in resp.embeddings]

if __name__ == "__main__":
    embedder = GeminiEmbedder()
    
    print(embedder.embed(["Hello, World!"])[0])
