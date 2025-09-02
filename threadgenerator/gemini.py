"""
Gemini Thread Generator.
"""

from .base import AbstractThreadGenerator
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import GEMINI_API_KEYS
import json
from globals import THREADING_LOCK
from google import genai

class GeminiThreadGenerator(AbstractThreadGenerator):
    def __init__(self, state):
        super().__init__(state)
        self._clients = [
            genai.Client(api_key=x) for x in GEMINI_API_KEYS
        ]
        self._thread_generation_prompt = """
You are an expert X (Twitter) thread writer skilled in maximizing reach and engagement. 
Transform the following article into a compelling X thread. 
Each tweet must be concise (≤280 characters). 
Avoid numbering/indexing (no “1/n”). 
Use a clear, engaging flow to keep readers hooked. 
Include high-reach, relevant hashtags in a natural way—at least in the first tweet. 
Make the thread feel conversational, insightful, and shareable. 

Return as JSON list: {"title": <string>, "thread": ["tweet1", "tweet2", ...]}.

Article:
%ARTICLE_TEXT%
"""
        self._max_workers = 5
    
    def _get_client(self):
        with THREADING_LOCK:
            self._state["gemini_current_client_idx"] = (self._state.get("gemini_current_client_idx", -1) + 1) % len(GEMINI_API_KEYS)
            _ = self._state["gemini_current_client_idx"]
        
        return self._clients[_]
    
    def _generate_single_thread(self, article):
        try:
            resp = self._get_client().models.generate_content_stream(
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
