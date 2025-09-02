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
GEMINI_API_KEYS = getenv("GEMINI_API_KEYS", "").split(",")
if len(GEMINI_API_KEYS) == 1 and GEMINI_API_KEYS[0] == "":
    raise ValueError("GEMINI_API_KEYS not found in the environment.")
GEMINI_DIMENSION = 3072

# Vector Store Config
VECTOR_STORE_DIMENSION = GEMINI_DIMENSION
VECTOR_SIMILAR_SEARCH_N = 1

# FAISS Specific config
FAISS_STORE_FILE_NAME="faiss_store"

# Final maximum thread count
MAXIMUM_THREAD_COUNT = 2

# X API
X_API_KEY = getenv("X_API_KEY", None)
X_API_KEY_SECRET = getenv("X_API_KEY_SECRET", None)
X_ACCESS_TOKEN = getenv("X_ACCESS_TOKEN", None)
X_ACCESS_TOKEN_SECRET = getenv("X_ACCESS_TOKEN_SECRET", None)
if None in [X_API_KEY, X_API_KEY_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]:
    raise ValueError("X API Credentials not found in the environment.")
