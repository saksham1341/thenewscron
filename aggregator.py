"""
Aggregator script.
"""

import asyncio
from dataclasses import asdict
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

# Save state
with open("state.json", "w") as f:
    json.dump(state, f)
