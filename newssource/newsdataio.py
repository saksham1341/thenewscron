"""
News source using newsdata.io API
"""

from .base import AbstractNewsSource
from article import Article
from config import NEWSDATAIO_API_KEYS, MAXIMUM_LATEST_ARTICLES
from newsdataapi import NewsDataApiClient
from typing import List

class NewsDataIO(AbstractNewsSource):
    def __init__(self) -> None:
        self._api_clients = [
            NewsDataApiClient(
                apikey=_,
            ) for _ in NEWSDATAIO_API_KEYS
        ]
        self._current_client_index = 0
    
    def get_api_client(self) -> NewsDataApiClient:
        """
        Return the api client at current client index and increment the index.
        """
        
        _ = self._api_clients[self._current_client_index]
        self._current_client_index += 1
        self._current_client_index %= len(self._api_clients)
        
        return _
    
    def get_latest_articles(self, max_n = MAXIMUM_LATEST_ARTICLES) -> List[Article]:
        """
        Fetch a maximum of max_n latest articles using the api client.
        """
        
        client = self.get_api_client()
        response = client.latest_api(
            size=max_n
        )
        
        if response["status"] != "success":
            raise RuntimeError("Failed to fetch news from api.")
        
        results = response["results"]
        
        return [
            Article(
                id=_["article_id"],
                title=_["title"],
                link=_["link"],
            ) for _ in results
        ]

if __name__ == "__main__":
    source = NewsDataIO()
    
    print(source.get_latest_articles())
