import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Tuple
from threading import RLock


class ScrapingCache(ABC):
    """
    Abstract base class for a scraping cache.
    """

    @abstractmethod
    def get(self, url: str) -> Optional[str]:
        """
        Retrieve the cached markdown for a given URL, or None if not present or expired.
        """
        pass

    @abstractmethod
    def set(self, url: str, markdown: str) -> None:
        """
        Store the markdown for a given URL in the cache.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clear the cache.
        """
        pass


class InMemoryScrapingCache(ScrapingCache):
    """
    In-memory implementation of ScrapingCache with time-based expiration.
    """

    def __init__(self, ttl_seconds: int = 120):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Tuple[str, float]] = {}  # url -> (markdown, timestamp)
        self._lock = RLock()

    def _clear_expired(self) -> None:
        """
        Obtain the lock before calling this method!
        """
        now = time.time()
        expired_keys = []
        for url, (markdown, timestamp) in self._cache.items():
            if now - timestamp > self.ttl_seconds:
                expired_keys.append(url)
        for url in expired_keys:
            del self._cache[url]

    def get(self, url: str) -> Optional[str]:
        with self._lock:
            self._clear_expired()
            entry = self._cache.get(url)
            if entry is None:
                return None
            markdown, timestamp = entry
            return markdown

    def set(self, url: str, markdown: str) -> None:
        with self._lock:
            self._cache[url] = (markdown, time.time())

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
