"""
Ethical and rate-limited HTTP fetcher for web crawling.
"""
import time
import logging
from typing import Optional, Dict
from urllib.parse import urlparse
import httpx

from backend.config import DEFAULT_USER_AGENT, DEFAULT_TIMEOUT, MAX_PAGE_SIZE_BYTES

logger = logging.getLogger(__name__)


class FetchResult:
    def __init__(self, url: str, status_code: int, html: str = "", content_type: str = "", error: Optional[str] = None):
        self.url = url
        self.status_code = status_code
        self.html = html
        self.content_type = content_type
        self.error = error
        self.success = status_code == 200 and not error


class RateLimitedFetcher:
    """HTTP fetcher with per-domain politeness throttle and robots enforcement."""

    def __init__(self, user_agent: str = DEFAULT_USER_AGENT, timeout: float = DEFAULT_TIMEOUT):
        self.user_agent = user_agent
        self.timeout = timeout
        self.last_request_time: Dict[str, float] = {}
        self.headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    def _get_domain(self, url: str) -> str:
        return urlparse(url).netloc.lower()

    def fetch(self, url: str, min_delay: float = 1.0) -> FetchResult:
        """Fetches a single URL with polite per-domain delay."""
        domain = self._get_domain(url)
        now = time.time()
        last_time = self.last_request_time.get(domain, 0.0)
        elapsed = now - last_time

        if elapsed < min_delay:
            time.sleep(min_delay - elapsed)

        self.last_request_time[domain] = time.time()

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                resp = client.get(url, headers=self.headers)
                content_type = resp.headers.get("content-type", "")

                if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
                    return FetchResult(
                        url=str(resp.url),
                        status_code=resp.status_code,
                        content_type=content_type,
                        error=f"Unsupported content type: {content_type}",
                    )

                if len(resp.content) > MAX_PAGE_SIZE_BYTES:
                    return FetchResult(
                        url=str(resp.url),
                        status_code=resp.status_code,
                        content_type=content_type,
                        error=f"Page size exceeded {MAX_PAGE_SIZE_BYTES} bytes",
                    )

                return FetchResult(
                    url=str(resp.url),
                    status_code=resp.status_code,
                    html=resp.text,
                    content_type=content_type,
                )
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return FetchResult(url=url, status_code=0, error=str(e))

