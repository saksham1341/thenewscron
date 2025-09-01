"""
Configuration file.
"""

from os import getenv

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
VECTOR_NEAREST_SEARCH_N = 1
