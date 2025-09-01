"""
Aggregator script.
"""

import asyncio
from config import STATE_FILE_NAME, STORED_ARTICLES_FILE_NAME, SIMILARITY_THRESHOLD
from dataclasses import asdict
from embedder.gemini import GeminiEmbedder
import json
from newssource.newsdataio import NewsDataIO
import pandas as pd
from uuid import uuid4
from vectorstore.faiss import FAISS

# open state file
try:
    with open(STATE_FILE_NAME, "r") as f:
        state = json.load(f)
except:
    state = {}

news_source = NewsDataIO(state)
latest_articles = asyncio.run(news_source.get_latest_articles())
if not latest_articles:
    exit()

# TODO:
# 1. Assign clusters to latest articles based on the articles already in vector store
# 2. Load the stored articles dataframe, update it, save it back.

# Load stored articles
try:
    stored_articles = pd.read_csv(STORED_ARTICLES_FILE_NAME)
except:
    stored_articles = pd.DataFrame(columns=asdict(latest_articles[0]).keys())

# filter out all articles that are already stored
latest_articles = [
    article for article in latest_articles if len(stored_articles[stored_articles["id"] == article.id]) == 0
]

# Generate embeddings of all articles
article_contents = [article.content for article in latest_articles]
embedder = GeminiEmbedder()
embeddings = embedder.embed(article_contents)
for idx, article in enumerate(latest_articles):
    article.embedding = embeddings[idx]

# Load the faiss store
vector_store = FAISS()
# hotfix article_id to duplication_id map
article_id_to_duplication_id = {
    row["id"]: row["duplication_id"] for idx, row in stored_articles.iterrows()
}
# Search for semantic duplicates in the vector store for each latest article
for article in latest_articles:
    resp = vector_store.get_similar_vectors(article.embedding)
    for article_id, sim in resp:
        if sim > SIMILARITY_THRESHOLD:
            article.duplication_id = article_id_to_duplication_id[article_id]
            article_id_to_duplication_id[article.id] = article.duplication_id
            
            # Add article to vector store
            article.vector_store_index = vector_store.add_vectors([article.embedding])[0]
            
            break
    
    # No similar article found
    article.duplication_id = uuid4()
    article_id_to_duplication_id[article.id] = article.duplication_id
    
    # Add article to vector store
    article.vector_store_index = vector_store.add_vectors([article.embedding])[0]

# Save vector store to disk
vector_store.save_to_disk()

# Append latest articles to stored_articles
latest_articles_df = pd.DataFrame([asdict(article) for article in latest_articles])
updated_articles = pd.concat(
    [stored_articles, latest_articles_df],
    ignore_index=True
)

# Save updated_articles
updated_articles.to_csv(STORED_ARTICLES_FILE_NAME, index=False)

# Save state
with open(STATE_FILE_NAME, "w") as f:
    json.dump(state, f)
