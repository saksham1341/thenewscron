"""
News source using newsdata.io API
"""

from .base import AbstractNewsSource
from article import Article
import asyncio
from config import NEWSDATAIO_API_KEYS, MAXIMUM_LATEST_ARTICLES
import httpx
from newsdataapi import NewsDataApiClient
import trafilatura
from typing import List

class NewsDataIO(AbstractNewsSource):
    def __init__(self, state) -> None:
        super().__init__(state)
        
        self._api_clients = [
            NewsDataApiClient(
                apikey=_,
            ) for _ in NEWSDATAIO_API_KEYS
        ]
        self._current_client_index = self._state.get("newsdataio_current_client_index", 0)
    
    def get_api_client(self) -> NewsDataApiClient:
        """
        Return the api client at current client index and increment the index.
        """
        
        _ = self._api_clients[self._current_client_index]
        self._current_client_index += 1
        self._current_client_index %= len(self._api_clients)
        
        self._state["newsdataio_current_client_index"] = self._current_client_index
        
        return _
    
    async def get_article_content(self, url: str) -> str:
        """
        Fetch the cleaned article body given a url.
        """
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url)
            
            return trafilatura.extract(resp.text)
    
    async def get_latest_articles(self, max_n = MAXIMUM_LATEST_ARTICLES) -> List[Article]:
        """
        Fetch a maximum of max_n latest articles using the api client.
        """
        
        client = self.get_api_client()
        response = client.latest_api(
            size=max_n,
            language="en"  # TODO: Handle multilingual later
        )
        
        if response["status"] != "success":
            raise RuntimeError("Failed to fetch news from api.")
        
        results = response["results"]
        contents = await asyncio.gather(*[self.get_article_content(_["link"]) for _ in results], return_exceptions=True)
        
        return [
            Article(
                id=_["article_id"],
                title=_["title"],
                link=_["link"],
                content=contents[idx],
            ) for idx, _ in enumerate(results) if (not isinstance(contents[idx], BaseException)) and contents[idx] is not None 
        ]

if __name__ == "__main__":
    source = NewsDataIO()
    
    print(source.get_latest_articles())
