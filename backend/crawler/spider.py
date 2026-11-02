"""
Web Crawler / Spider for Seekr Search Engine.
Discovers and extracts permitted web pages within ethical boundaries.
"""
import json
import logging
from typing import List, Set, Dict, Optional, Generator
from urllib.parse import urlparse
from collections import deque
from pathlib import Path

from backend.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MAX_CRAWL_DEPTH,
    MAX_PAGES_PER_DOMAIN,
    DEFAULT_POLITENESS_DELAY,
)
from backend.crawler.robots import RobotsManager
from backend.crawler.fetcher import RateLimitedFetcher, FetchResult
from backend.processing.parser import HTMLProcessor, ParsedPage
from backend.processing.cleaner import TextCleaner
from backend.processing.tokenizer import Tokenizer
from backend.processing.deduplicator import Deduplicator

logger = logging.getLogger(__name__)


class SeekrCrawler:
    """Polite, privacy-respecting crawler with queue frontier and deduplication."""

    def __init__(
        self,
        max_depth: int = MAX_CRAWL_DEPTH,
        max_pages: int = MAX_PAGES_PER_DOMAIN,
        politeness_delay: float = DEFAULT_POLITENESS_DELAY,
        allowed_domains: Optional[List[str]] = None,
    ):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.politeness_delay = politeness_delay
        self.allowed_domains = set(d.lower() for d in allowed_domains) if allowed_domains else None

        self.robots = RobotsManager()
        self.fetcher = RateLimitedFetcher()
        self.parser = HTMLProcessor()
        self.cleaner = TextCleaner()
        self.tokenizer = Tokenizer()
        self.deduplicator = Deduplicator()

        self.visited_urls: Set[str] = set()
        self.domain_page_counts: Dict[str, int] = {}

    def _is_domain_allowed(self, url: str) -> bool:
        domain = urlparse(url).netloc.lower()
        if not self.allowed_domains:
            return True
        return domain in self.allowed_domains or any(domain.endswith("." + d) for d in self.allowed_domains)

    def crawl(self, seed_urls: List[str]) -> List[Dict]:
        """Performs breadth-first crawling starting from seed URLs."""
        # Queue stores tuples of (url, current_depth)
        queue = deque([(url, 0) for url in seed_urls])
        crawled_documents: List[Dict] = []

        total_pages_crawled = 0

        while queue and total_pages_crawled < self.max_pages:
            url, depth = queue.popleft()

            if url in self.visited_urls:
                continue

            domain = urlparse(url).netloc.lower()
            if self.domain_page_counts.get(domain, 0) >= self.max_pages:
                continue

            if not self._is_domain_allowed(url):
                continue

            # 1. Check Robots.txt
            if not self.robots.is_allowed(url):
                logger.info(f"Skipping {url} (disallowed by robots.txt)")
                self.visited_urls.add(url)
                continue

            # 2. Fetch page with politeness delay
            crawl_delay = max(self.politeness_delay, self.robots.get_crawl_delay(url))
            fetch_res: FetchResult = self.fetcher.fetch(url, min_delay=crawl_delay)
            self.visited_urls.add(url)

            if not fetch_res.success:
                logger.warning(f"Failed to fetch {url}: {fetch_res.error}")
                continue

            # 3. Parse HTML
            parsed: ParsedPage = self.parser.parse(fetch_res.html, url)
            clean_body = self.cleaner.normalize_text(parsed.body_text)
            clean_body = self.cleaner.filter_boilerplate_sentences(clean_body)

            if len(clean_body) < 80:  # Skip empty or negligible content pages
                continue

            # 4. Check for duplicates / near-duplicates
            if self.deduplicator.is_exact_duplicate(clean_body):
                logger.info(f"Skipping duplicate content: {url}")
                continue

            tokens = self.tokenizer.tokenize(clean_body)
            if self.deduplicator.is_near_duplicate(tokens, url):
                logger.info(f"Skipping near-duplicate content: {url}")
                continue

            # 5. Record document
            doc_record = {
                "id": f"doc_{len(crawled_documents) + 1}",
                "url": url,
                "domain": domain,
                "title": parsed.title or url,
                "meta_description": parsed.meta_description,
                "headings": parsed.headings,
                "body_text": clean_body,
                "word_count": len(tokens),
                "depth": depth,
            }
            crawled_documents.append(doc_record)
            self.domain_page_counts[domain] = self.domain_page_counts.get(domain, 0) + 1
            total_pages_crawled += 1
            logger.info(f"Crawled ({total_pages_crawled}/{self.max_pages}): {parsed.title[:40]} [{url}]")

            # 6. Enqueue links if within depth limit
            if depth < self.max_depth:
                for link in parsed.links:
                    if link not in self.visited_urls and self._is_domain_allowed(link):
                        queue.append((link, depth + 1))

        # Save to raw data archive
        output_file = RAW_DATA_DIR / "crawled_pages.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(crawled_documents, f, indent=2, ensure_ascii=False)

        return crawled_documents

