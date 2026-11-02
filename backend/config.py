"""
Configuration settings for Seekr: Privacy-First Intelligent Search Engine.
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SEEDS_DIR = DATA_DIR / "seeds"
INDEX_DIR = DATA_DIR / "index"

# Create directories if they do not exist
for p in [RAW_DATA_DIR, PROCESSED_DATA_DIR, SEEDS_DIR, INDEX_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Crawler Settings
DEFAULT_USER_AGENT = "SeekrBot/1.0 (+https://seekr-privacy.local/bot; respect robots.txt)"
DEFAULT_POLITENESS_DELAY = 1.0  # seconds between requests to same domain
DEFAULT_TIMEOUT = 8.0          # seconds
MAX_PAGE_SIZE_BYTES = 2 * 1024 * 1024  # 2MB
MAX_CRAWL_DEPTH = 2
MAX_PAGES_PER_DOMAIN = 30

# Inverted Index & BM25 parameters
BM25_K1 = 1.5
BM25_B = 0.75
TITLE_BOOST = 2.5
HEADING_BOOST = 1.6

# Vector & Semantic Settings
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
VECTOR_INDEX_FILE = INDEX_DIR / "faiss_index.bin"
VECTOR_METADATA_FILE = INDEX_DIR / "faiss_metadata.json"
INVERTED_INDEX_FILE = INDEX_DIR / "inverted_index.json"
DOCS_STORE_FILE = INDEX_DIR / "documents.json"

# Hybrid Ranking Settings
DEFAULT_HYBRID_ALPHA = 0.5  # Weight between BM25 and Semantic
RRF_K = 60                   # Reciprocal Rank Fusion constant

# Privacy Settings
ANALYTICS_EPSILON = 1.0     # Differential Privacy Laplace parameter
MIN_QUERY_COUNT_THRESHOLD = 3  # k-anonymity: do not show query in public autocomplete unless >= 3 searches
ENABLE_ZERO_IP_LOGGING = True

