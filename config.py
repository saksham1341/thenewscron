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
