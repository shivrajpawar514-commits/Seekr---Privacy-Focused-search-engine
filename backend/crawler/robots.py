"""
Robots.txt parser and policy checker for ethical crawling.
Respects robots exclusion standard, politeness delays, and domain rules.
"""
import urllib.robotparser
from urllib.parse import urlparse
import logging
from typing import Dict, Optional
import httpx

logger = logging.getLogger(__name__)


class RobotsManager:
    """Manages robots.txt caching and permission checking across domains."""

    def __init__(self, user_agent: str = "SeekrBot"):
        self.user_agent = user_agent
        self._parsers: Dict[str, urllib.robotparser.RobotFileParser] = {}
        self._crawl_delays: Dict[str, float] = {}

    def _get_base_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def fetch_robots_txt(self, base_url: str, timeout: float = 5.0) -> None:
        """Fetches and parses robots.txt for the given domain."""
        if base_url in self._parsers:
            return

        robots_url = f"{base_url.rstrip('/')}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)

        try:
            with httpx.Client(timeout=timeout, follow_redirects=True) as client:
                resp = client.get(robots_url, headers={"User-Agent": self.user_agent})
                if resp.status_code == 200:
                    rp.parse(resp.text.splitlines())
                    logger.info(f"Loaded robots.txt for {base_url}")
                elif resp.status_code in (401, 403):
                    # Disallow all if explicitly forbidden
                    rp.disallow_all = True
                    logger.warning(f"Robots.txt returned {resp.status_code} for {base_url}; treating as disallow all.")
                else:
                    # 404 or other status: standard allows crawling
                    rp.allow_all = True
        except Exception as e:
            logger.warning(f"Failed to fetch robots.txt for {base_url} ({e}); defaulting to allow.")
            rp.allow_all = True

        self._parsers[base_url] = rp

        # Extract crawl delay if present
        try:
            delay = rp.crawl_delay(self.user_agent)
            if delay:
                self._crawl_delays[base_url] = float(delay)
        except Exception:
            pass

    def is_allowed(self, url: str) -> bool:
        """Checks if the given URL is permitted to be crawled by robots.txt."""
        base_url = self._get_base_url(url)
        if base_url not in self._parsers:
            self.fetch_robots_txt(base_url)

        rp = self._parsers.get(base_url)
        if rp is None:
            return True

        try:
            return rp.can_fetch(self.user_agent, url)
        except Exception as e:
            logger.error(f"Error checking permission for {url}: {e}")
            return True

    def get_crawl_delay(self, url: str, default: float = 1.0) -> float:
        """Gets recommended crawl delay for domain."""
        base_url = self._get_base_url(url)
        return self._crawl_delays.get(base_url, default)

