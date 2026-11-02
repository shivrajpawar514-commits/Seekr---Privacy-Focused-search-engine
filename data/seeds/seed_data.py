"""
Curated seed educational documents to provide immediate out-of-the-box search results
for machine learning, python development, information retrieval, and privacy topics.
"""

INITIAL_KNOWLEDGE_BASE = [
    {
        "id": "doc_ml_01",
        "url": "https://scikit-learn.org/stable/tutorial/basic/tutorial.html",
        "domain": "scikit-learn.org",
        "title": "An Introduction to Machine Learning with scikit-learn",
        "meta_description": "Comprehensive tutorial introducing supervised and unsupervised learning algorithms with Python.",
        "headings": [
            "Machine Learning: The Problem Setting",
            "Loading an Example Dataset",
            "Learning and Predicting with Estimators",
            "Model Persistence and Best Practices"
        ],
        "body_text": (
            "Machine learning is a method of data analysis that automates analytical model building. "
            "It is a branch of artificial intelligence based on the idea that systems can learn from data, "
            "identify patterns and make decisions with minimal human intervention. Scikit-learn is one of the "
            "best resources to learn machine learning in Python. It features various classification, regression "
            "and clustering algorithms including support-vector machines, random forests, gradient boosting, "
            "k-means and DBSCAN, and is designed to interoperate with the Python numerical and scientific libraries "
            "NumPy and SciPy. Beginners starting in machine learning are encouraged to practice hands-on projects, "
            "evaluate models using cross-validation, and understand training versus test data splits."
        ),
        "word_count": 128
    },
    {
        "id": "doc_ml_02",
        "url": "https://pytorch.org/tutorials/beginner/basics/intro.html",
        "domain": "pytorch.org",
        "title": "Learn the Basics of Deep Learning with PyTorch",
        "meta_description": "Official PyTorch beginner guide to neural networks, tensors, automatic differentiation, and GPU acceleration.",
        "headings": [
            "Tensors and Autograd",
            "Building Neural Network Architectures",
            "Optimizing Model Parameters",
            "Saving and Loading Trained Models"
        ],
        "body_text": (
            "PyTorch is an optimized tensor library for deep learning using GPUs and CPUs. "
            "It is widely regarded as one of the best resources to learn modern deep learning and neural networks. "
            "Students and researchers use PyTorch to build state-of-the-art computer vision and natural language "
            "processing systems. Key foundational concepts include tensors, dynamic computational graphs, forward "
            "and backward propagation, loss functions, and stochastic gradient descent optimizers. Hands-on tutorials "
            "provide step-by-step guidance from linear regression to transformer architectures."
        ),
        "word_count": 115
    },
    {
        "id": "doc_ml_03",
        "url": "https://developers.google.com/machine-learning/crash-course",
        "domain": "developers.google.com",
        "title": "Google Machine Learning Crash Course with TensorFlow APIs",
        "meta_description": "Fast-paced, practical introduction to machine learning featuring video lectures, real-world case studies, and hands-on exercises.",
        "headings": [
            "Framing Machine Learning Problems",
            "Descending into Gradient Descent",
            "Feature Engineering and Representation",
            "Neural Networks and Embeddings"
        ],
        "body_text": (
            "Google's Machine Learning Crash Course is considered among the top online resources for mastering "
            "machine learning fundamentals. The course covers supervised learning, regression models, classification metrics "
            "such as ROC curves and AUC, fairness in machine learning systems, and dense vector embeddings. Exercises use "
            "interactive Colab notebooks to demonstrate how gradient descent converges and how feature crosses improve "
            "non-linear problem solving. Ideal for software engineers transitioning to applied AI."
        ),
        "word_count": 105
    },
    {
        "id": "doc_ir_01",
        "url": "https://nlp.stanford.edu/IR-book/html/htmledition/scoring-term-weighting-and-the-vector-space-model-1.html",
        "domain": "nlp.stanford.edu",
        "title": "Information Retrieval: Inverted Indexes, BM25, and Vector Space Scoring",
        "meta_description": "Stanford reference guide on inverted index construction, term frequency, inverse document frequency, and ranking.",
        "headings": [
            "Inverted Index Architecture",
            "Term Frequency and Weighting",
            "The Okapi BM25 Probabilistic Relevance Model",
            "Dense Vector Embeddings vs Sparse Keyword Indices"
        ],
        "body_text": (
            "Search engines rely on inverted indexes to retrieve relevant documents rapidly from massive web collections. "
            "An inverted index maintains a vocabulary of terms mapped to postings lists containing document IDs, frequencies, "
            "and token positions. The Okapi BM25 algorithm improves upon raw TF-IDF by incorporating document length normalization "
            "and term frequency saturation parameters k1 and b. Modern hybrid search engines combine BM25 keyword matching with "
            "dense semantic embeddings to solve both exact terminology matching and vocabulary mismatch problems."
        ),
        "word_count": 118
    },
    {
        "id": "doc_web_01",
        "url": "https://docs.scrapy.org/en/latest/intro/tutorial.html",
        "domain": "scrapy.org",
        "title": "Scrapy Tutorial: Building Web Crawlers and Spiders in Python",
        "meta_description": "Learn how to build asynchronous web scrapers that respect robots.txt, extract clean HTML, and follow links.",
        "headings": [
            "Creating a Spider Project",
            "Following Links and Crawl Depth",
            "Handling Robots.txt and Rate Limits",
            "Item Pipelines and Data Processing"
        ],
        "body_text": (
            "Scrapy is an open source and collaborative framework for extracting the data you need from websites in a fast, "
            "simple, yet extensible way. Built on Twisted asynchronous networking, Scrapy spiders navigate web pages, obey "
            "robots exclusion protocol guidelines, throttle requests to avoid server overloading, and extract structured data "
            "using CSS and XPath selectors. It pairs naturally with BeautifulSoup for delicate HTML cleaning and normalization."
        ),
        "word_count": 98
    },
    {
        "id": "doc_priv_01",
        "url": "https://privacyguides.org/en/basics/search-engines/",
        "domain": "privacyguides.org",
        "title": "Privacy-Respecting Search Engines and Zero-Tracking Technologies",
        "meta_description": "Overview of privacy-first search architectures, client-side re-ranking, and differential privacy.",
        "headings": [
            "Why Search Privacy Matters",
            "Zero IP Logging and Sessionless Architecture",
            "Client-Side Personalized Ranking",
            "Differential Privacy in Aggregate Analytics"
        ],
        "body_text": (
            "Traditional search engines construct comprehensive behavioral profiles by tracking user IP addresses, search queries, "
            "and click telemetry across sessions. Privacy-first search engines implement zero-knowledge architectures: they do not log "
            "IP addresses, store search histories, or emit persistent tracking cookies. Furthermore, user personalization can be "
            "performed strictly on the client side inside the browser, allowing individuals to customize their relevance preferences "
            "without transmitting sensitive interests to centralized servers. Aggregate analytics are safeguarded using differential privacy."
        ),
        "word_count": 112
    },
    {
        "id": "doc_priv_02",
        "url": "https://differentialprivacy.org/primer/",
        "domain": "differentialprivacy.org",
        "title": "A Friendly Primer on Differential Privacy and the Laplace Mechanism",
        "meta_description": "Mathematical foundations of differential privacy, epsilon parameters, and privacy-preserving query aggregation.",
        "headings": [
            "The Formal Definition of Differential Privacy",
            "Adding Calibrated Laplace Noise",
            "The Privacy Budget Epsilon",
            "K-Anonymity and Frequency Suppression"
        ],
        "body_text": (
            "Differential privacy provides mathematically provable guarantees against individual identification in aggregate datasets. "
            "By injecting noise drawn from a Laplace distribution calibrated to the global sensitivity of the query, analysts can "
            "publish population-level statistics while guaranteeing that the presence or absence of any single individual cannot be inferred. "
            "In search systems, differential privacy ensures that trending search topics reflect genuine community interest without "
            "revealing the queries of individual users."
        ),
        "word_count": 104
    },
    {
        "id": "doc_fastapi_01",
        "url": "https://fastapi.tiangolo.com/tutorial/first-steps/",
        "domain": "fastapi.tiangolo.com",
        "title": "FastAPI Framework: High Performance Modern Python Web APIs",
        "meta_description": "Build production-ready, asynchronous REST APIs with automatic OpenAPI docs and Pydantic validation.",
        "headings": [
            "Async Request Handling with Starlette",
            "Pydantic Data Models and Validation",
            "Interactive OpenAPI and Swagger Docs",
            "Deploying with Uvicorn and Docker"
        ],
        "body_text": (
            "FastAPI is a modern, fast (high-performance) web framework for building APIs with Python based on standard Python type hints. "
            "It runs on top of Starlette and Uvicorn, delivering speeds comparable to NodeJS and Go. Features include automatic data "
            "serialization, interactive documentation via Swagger UI, dependency injection, and native async support. It is the ideal "
            "backend framework for search APIs requiring concurrent index queries and low-latency retrieval."
        ),
        "word_count": 92
    }
]

