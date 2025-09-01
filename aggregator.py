"""
Aggregator script.
"""

import asyncio
from dataclasses import asdict
from embedder.gemini import GeminiEmbedder
import json
from newssource.newsdataio import NewsDataIO
import pandas as pd

# open state.json
try:
    with open("state.json", "r") as f:
        state = json.load(f)
except:
    state = {}

news_source = NewsDataIO(state)
latest_articles = asyncio.run(news_source.get_latest_articles())

# TODO:
# 1. Assign clusters to latest articles based on the articles already in vector store
# 2. Load the stored articles dataframe, update it, save it back.

# Generate embeddings of all articles

article_contents = [article.content for article in latest_articles]
embedder = GeminiEmbedder()
embeddings = embedder.embed(article_contents)
for idx, article in enumerate(latest_articles):
    article.embedding = embeddings[idx]

# Save state
with open("state.json", "w") as f:
    json.dump(state, f)
