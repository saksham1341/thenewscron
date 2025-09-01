"""
Main executor script.
"""

from article.merged import MergedArticle
from articlescorer.gemini import GeminiArticleScorer
from config import STATE_FILE_NAME, STORED_ARTICLES_FILE_NAME, FAISS_STORE_FILE_NAME, GEMINI_API_KEY, MAXIMUM_THREAD_COUNT
from os import remove
import pandas as pd
from threadgenerator.gemini import GeminiThreadGenerator

# Load data and delete it from disk for next cycle
print("Loading stored articles.")
stored_articles = pd.read_csv(STORED_ARTICLES_FILE_NAME)
print("Deleting state files for next cycle.")
remove(STORED_ARTICLES_FILE_NAME)
remove(STATE_FILE_NAME)
remove(FAISS_STORE_FILE_NAME)

# Generate merged articles
merged_articles = [
    MergedArticle(
        total_content="---".join(row["content"])
    ) for _, row in stored_articles.groupby(by="duplication_id").agg(func=list).iterrows()
]
print(f"Generated {len(merged_articles)} merged articles.")

# Score the marged articles
print("Scoring the articles.")
scorer = GeminiArticleScorer()
while True:
    try:
        scorer.score_articles(merged_articles)
    except:
        print("Error occured. Trying again.")
        continue
    else:
        break
    
# Take the best scoring articles
merged_articles.sort(key=lambda x: x.score, reverse=True)
merged_articles = merged_articles[:MAXIMUM_THREAD_COUNT]

# Generate X threads
print(f"Generating threads for best {len(merged_articles)} articles.")
thread_generator = GeminiThreadGenerator()
thread_generator.generate_threads(merged_articles)

# Clean articles that failed to generate
merged_articles = [
    article for article in merged_articles if article.title is not None and article.thread is not None
]
print(f"Final {len(merged_articles)} threads generated.")

for a in merged_articles:
    print("=" * 50)
    print(a.title)
    print("-" * 50)
    for x in a.thread:
        print(x)
    print()
    print()

# TODO: Publish threads to X