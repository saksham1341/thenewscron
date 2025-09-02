"""
Main executor script.
"""

from article.merged import MergedArticle
from articlescorer.gemini import GeminiArticleScorer
from config import STATE_FILE_NAME, STORED_ARTICLES_FILE_NAME, THREADS_FILE_NAME, FAISS_STORE_FILE_NAME, MAXIMUM_THREAD_COUNT
from dataclasses import asdict
import json
from os import remove
import pandas as pd
from threadgenerator.gemini import GeminiThreadGenerator

# Load data and delete it from disk for next cycle
print("Loading stored articles.")
try:
    stored_articles = pd.read_csv(STORED_ARTICLES_FILE_NAME)
except:
    print("Failed to load stored articles. Aborting.")
    exit()

# open state file
print("Loading state file.")
try:
    with open(STATE_FILE_NAME, "r") as f:
        state = json.load(f)
except:
    state = {}

print("Deleting state files for next cycle.")
remove(STORED_ARTICLES_FILE_NAME)
remove(STATE_FILE_NAME)
remove(FAISS_STORE_FILE_NAME)

# Generate merged articles
merged_articles = [
    MergedArticle(
        total_content="---".join(row["content"]),
        sources=row["link"],
    ) for _, row in stored_articles.groupby(by="duplication_id").agg(func=list).iterrows()
]
print(f"Generated {len(merged_articles)} merged articles.")

# Score the marged articles
print("Scoring the articles.")
scorer = GeminiArticleScorer(state)
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
thread_generator = GeminiThreadGenerator(state)
thread_generator.generate_threads(merged_articles)


# Clean articles that failed to generate
merged_articles = [
    article for article in merged_articles if article.title is not None and article.thread is not None
]
print(f"Final {len(merged_articles)} threads generated.")
if not merged_articles:
    exit()

# Append sources
for article in merged_articles:
    article.thread.append("Sources:" + "\n".join(f'[{_}]' for _ in article.sources))

try:
    stored_threads = pd.read_csv(THREADS_FILE_NAME)
    stored_threads["thread"] = stored_threads["thread"].map(json.loads)
except:
    stored_threads = pd.DataFrame(columns=asdict(merged_articles[0]).keys())

new_threads_df = pd.DataFrame([asdict(article) for article in merged_articles])
updated_threads = pd.concat(
    [stored_threads, new_threads_df],
    ignore_index=True
)
updated_threads["thread"] = updated_threads["thread"].map(json.dumps)

updated_threads.to_csv(THREADS_FILE_NAME)

# Save state
with open(STATE_FILE_NAME, "w") as f:
    json.dump(state, f)

print("Saved.")