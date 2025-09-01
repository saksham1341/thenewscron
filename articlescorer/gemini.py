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
You are an expert social media strategist. 
Given the following article, which is basically multiple articles separated by `---`, rate its potential performance if converted into an X (Twitter) thread on a scale of 0 to 100. 
Respond with JSON in the format: {"score": <float>}.

Article:
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
            text = text[7:] if text.startswith("```json") else text
            text = text[:-3] if text.endswith("```") else text

            article.score = json.loads(text)["score"]
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
