"""
Configuration file.
"""

from os import getenv

STATE_FILE_NAME = "state.json"
STORED_ARTICLES_FILE_NAME = "articles.csv"
THREADS_FILE_NAME = "threads.csv"

# Similarity threshold to classify two documents as same
SIMILARITY_THRESHOLD = 0.9

# Maximum latest articles to fetch from a news source.
MAXIMUM_LATEST_ARTICLES = 10

# newsdata.io API keys
NEWSDATAIO_API_KEYS = getenv("NEWSDATAIO_API_KEYS", "").split(",")
if len(NEWSDATAIO_API_KEYS) == 1 and NEWSDATAIO_API_KEYS[0] == "":
    raise ValueError("NEWSDATAIO_API_KEYS not found in the environment.")

# Gemini
GEMINI_API_KEY = getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY == "":
    raise ValueError("GEMINI_API_KEY not found in environment.")
GEMINI_DIMENSION = 3072

# Vector Store Config
VECTOR_STORE_DIMENSION = GEMINI_DIMENSION
VECTOR_SIMILAR_SEARCH_N = 1

# FAISS Specific config
FAISS_STORE_FILE_NAME="faiss_store"

# Final maximum thread count
MAXIMUM_THREAD_COUNT = 2