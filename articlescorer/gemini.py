"""
Gemini based article scorer.
"""

from .base import AbstractArticleScorer
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import GEMINI_API_KEY
from google import genai
import json
from time import sleep

class GeminiArticleScorer(AbstractArticleScorer):
    def __init__(self) -> None:
        self._client = genai.Client()
        self._scoring_prompt = """
You are an expert social media strategist specializing in high-impact X (Twitter) threads.
I will provide you with multiple articles on the same event, separated by "---".

Your task:

Analyze the overall event described across the articles.

Evaluate its potential impact and engagement value if turned into an X thread.

Consider factors such as relevance, timeliness, virality potential, emotional impact, controversy, uniqueness, and public interest.

Output only a single numeric score between 1 and 100, where:

1 = not worth writing about (low interest/impact)

100 = extremely worth writing about (high viral potential)

Do not provide explanations or text—only the numeric score.

Here is the content to evaluate:
%ARTICLE_BODY%
"""
        self._max_workers = 5
    
    def _score_single_article(self, article):
        if article.score is not None:
            return article

        try:
            resp = self._client.models.generate_content(
                model="gemini-2.5-flash",
                contents=self._scoring_prompt.replace("%ARTICLE_BODY%", article.total_content),
            )
            text = resp.text

            article.score = float(text)
        except Exception:
            article.score = 0

        return article

    def score_articles(self, articles):
        results = []
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = {executor.submit(self._score_single_article, a): a for a in articles}
            for future in as_completed(futures):
                results.append(future.result())
        return results
    
    # def score_articles(self, articles):
    #     for article in articles:
    #         if article.score is not None:
    #             continue
            
    #         resp = self._client.models.generate_content(
    #             model="gemini-2.5-flash",
    #             contents=self._scoring_prompt.replace("%ARTICLE_BODY%", article.total_content)
    #         )
            
    #         try:
    #             resp = resp.text
    #             resp = resp[7:] if resp.startswith("```json") else resp
    #             resp = resp[:-3] if resp.endswith("```") else resp
                
    #             article.score = json.loads(resp)["score"]
    #         except:
    #             article.score = 0
            
    #         sleep(20.5)
