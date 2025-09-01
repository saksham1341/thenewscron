"""
Main executor script.
"""

from article.merged import MergedArticle
from articlescorer.gemini import GeminiArticleScorer
from config import STATE_FILE_NAME, STORED_ARTICLES_FILE_NAME, FAISS_STORE_FILE_NAME, GEMINI_API_KEY
from os import remove
import pandas as pd

# Load data and delete it from disk for next cycle
stored_articles = pd.read_csv(STORED_ARTICLES_FILE_NAME)
# remove(STORED_ARTICLES_FILE_NAME)
# remove(STATE_FILE_NAME)
# remove(FAISS_STORE_FILE_NAME)

# Generate merged articles
merged_articles = [
    MergedArticle(
        total_content="---".join(row["content"])
    ) for _, row in stored_articles.groupby(by="duplication_id").agg(func=list).iterrows()
]

# Score the marged articles
scorer = GeminiArticleScorer()
while True:
    try:
        scorer.score_articles(merged_articles)
    except:
        continue
    else:
        break
    
# Take the best scoring articles
merged_articles.sort(key=lambda x: x.score, reverse=True)
merged_articles = merged_articles[1:]

# Generate X thread


# TODO:
#   1. Take highest 5 score merged_articles
#   2. Generate X threads for them
#   3. Publish threads to X

for article in merged_articles:
    print(article.score)
