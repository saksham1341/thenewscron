"""
Gemini Thread Generator.
"""

from .base import AbstractThreadGenerator
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import GEMINI_API_KEY
import json
from google import genai

class GeminiThreadGenerator(AbstractThreadGenerator):
    def __init__(self):
        self._client = genai.Client()
        self._thread_generation_prompt = """
You are a skilled thread writer for X (Twitter). 
Convert the following article into an engaging X thread. 
Break the content into clear tweets (max 280 chars each). 
Return as JSON list: {"title": <string>, "thread": ["tweet1", "tweet2", ...]}.

Article:
%ARTICLE_TEXT%
"""
        self._max_workers = 5
    
    def _generate_single_thread(self, article):
        try:
            resp = self._client.models.generate_content_stream(
                model="gemini-2.5-pro",
                contents=self._thread_generation_prompt.replace("%ARTICLE_TEXT%", article.total_content)
            )

            result = ""
            for chunk in resp:
                result += chunk.text

            # clean json formatting if fenced with ```json ... ```
            result = result[7:] if result.startswith("```json") else result
            result = result[:-3] if result.endswith("```") else result

            parsed = json.loads(result)
            article.title = parsed.get("title", None)
            article.thread = parsed.get("thread", None)
        except Exception as e:
            article.title = None
            article.thread = None

    def generate_threads(self, articles):
        results = []
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            futures = {executor.submit(self._generate_single_thread, a): a for a in articles}
            for future in as_completed(futures):
                pass
