# MoodFlix Architecture

## Overview

MoodFlix is an AI-first movie recommendation system where Flask provides the user interface and the core intelligence lives in the semantic recommendation pipeline.

The system is designed to understand natural language intent, emotion, and context from user text and match it against TMDB movie metadata using sentence embeddings and cosine similarity.

This document describes the repository structure, responsibilities for each folder and module, the startup lifecycle, the semantic data pipeline, the AI layer components, the request flow, and the explainable recommendation architecture.

---

## Repository Structure

```
Movie-Recommendation-System/
├── AGENTS.md
├── app.py
├── config.py
├── README.md
├── ARCHITECTURE.md
├── requirements.txt
├── .gitignore
├── assets/
├── dataset/
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│   └── cache/
│       └── movie_embeddings.pkl
├── docs/
│   └── IMPLEMENTATION_PLAN.md
├── models/
│   └── __init__.py
├── routes/
│   └── __init__.py
├── services/
│   └── __init__.py
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
├── tests/
├── utils/
│   └── __init__.py
└── TODO.md
```

---

## Folder Responsibilities

### `app.py`
- Pure Flask application entry point.
- Should remain extremely small.
- Responsible for application creation and blueprint registration only.
- Should not contain business logic, data pipeline logic, or AI logic.

### `config.py`
- Central application configuration.
- Reads environment variables via `python-dotenv` or equivalent.
- Exposes typed configuration values such as:
  - `TMDB_API_KEY`
  - `DATASET_PATH`
  - `EMBEDDINGS_CACHE_PATH`
  - `FLASK_DEBUG`
  - `MODEL_NAME`

### `routes/`
- Contains Flask route modules and blueprints.
- Responsible only for HTTP request routing, form processing, and template rendering.
- Should delegate processing to `services/`.
- Should never contain embedding, ranking, or dataset logic.

### `services/`
- Business logic and workflow coordination.
- Responsible for orchestrating the end-to-end request flow.
- Receives structured domain inputs and returns structured domain outputs.
- Should never manipulate `pandas.DataFrame` objects directly.
- Should delegate dataset loading, preprocessing, and embedding operations to `utils/` and `models/`.

### `models/`
- AI layer, containing inference and recommendation logic.
- Contains two logical components:
  - Embedding Engine
  - Recommendation Engine
- Responsible for semantic vector generation, embedding caching, similarity ranking, filtering, and explainability.
- Should remain separate from Flask request handling.

### `utils/`
- Shared helpers and dataset utilities.
- Responsible for dataset loading, metadata preprocessing, environment access, and TMDB API helpers.
- Supports the AI pipeline without containing core model logic.

### `templates/`
- Server-rendered HTML templates.
- Responsible for UI presentation and rendering recommendation results.
- Receives domain output from the service layer.

### `static/`
- Frontend assets only: CSS, JavaScript, images.
- No Python code.

### `dataset/`
- Holds the manually downloaded TMDB dataset files.
- Expected files:
  - `tmdb_5000_movies.csv`
  - `tmdb_5000_credits.csv`
- Includes a cache subfolder for serialized embeddings, for example:
  - `dataset/cache/movie_embeddings.pkl`
- No dataset fetch scripts should be added.

### `docs/`
- Documentation and planning artifacts.
- Contains architectural and implementation planning documents.

### `tests/`
- Unit tests and integration tests.
- Should validate the semantic recommendation pipeline, service orchestration, and route behavior.

---

## Application Startup Lifecycle

The application should initialize once at startup and keep movie embeddings ready for inference.

1. Application starts.
2. Load configuration.
3. Load TMDB dataset.
4. Preprocess movie metadata.
5. Load sentence-transformer model.
6. Load cached movie embeddings if available.
7. Otherwise generate movie embeddings.
8. Cache embeddings to disk.
9. Register Flask routes.
10. Application ready.

During requests, only user text should be embedded. Movie embeddings should already exist in memory or be loaded from a cache.

---

## Embedding Cache

A caching layer must exist so movie embeddings are generated once and reused across application launches.

Recommended cache structure:

```
dataset/
  tmdb_5000_movies.csv
  tmdb_5000_credits.csv
  cache/
    movie_embeddings.pkl
```

The cache should store:
- the movie embedding matrix,
- metadata identifiers for matching results,
- any preprocessing artifacts required to map results back to movie rows.

The embedding cache enables fast startup after the first run and avoids regenerating movie embeddings for every request.

---

## Data Pipeline

The TMDB dataset should be processed into a single semantic text representation per movie.

1. Load movie dataset from `dataset/`.
2. Handle missing values.
3. Combine useful fields:
   - `title`
   - `genres`
   - `keywords`
   - `overview`
4. Create a single semantic text representation.
5. Generate embeddings for movie text.
6. Cache embeddings.

This pipeline ensures movie metadata is normalized into a single vector space and that the corpus is ready for semantic similarity.

---

## AI Layer

The AI layer is logically split into two components inside `models/`.

### Embedding Engine

Responsible only for:
- loading the sentence-transformer model,
- generating embeddings for user text,
- loading cached movie embeddings,
- generating and serializing movie embeddings if needed.

The Embedding Engine should support:
- `load_transformer()`
- `embed_text(text: str) -> np.ndarray`
- `load_cached_embeddings(path: str)`
- `save_cached_embeddings(path: str, embeddings)`

### Recommendation Engine

Responsible only for:
- cosine similarity calculations,
- ranking movies,
- filtering results,
- explainability metadata.

The Recommendation Engine should support:
- `compute_similarity(query_embedding, movie_embeddings)`
- `rank_movies(similarity_scores, top_k)`
- `filter_by_rules(results, filters)`
- `build_explainability(recommendations, query_text)`

These two components may both live in `models/`, but are logically distinct.

---

## Semantic Intent Analysis

The system interprets user input as semantic intent, not simple mood keywords.

The architecture should reflect understanding of:
- emotion,
- intent,
- context.

Example user expressions:
- "I'm exhausted after exams."
- "I miss my childhood."
- "I want something inspiring."
- "I want to watch something with my family."

Semantic Intent Analysis is the process of converting natural language requests into an embedding that captures the user's intent and emotional context.

---

## Request Flow

1. User submits natural language text.
2. Flask route receives the request.
3. Flask route delegates to the service layer.
4. Service layer invokes Semantic Intent Analysis.
5. Semantic Intent Analysis generates a user embedding.
6. Service layer calls the Recommendation Engine.
7. Recommendation Engine performs movie ranking.
8. Recommendation Engine produces explainability metadata.
9. Service layer prepares domain output.
10. Template rendering returns the result page.

This flow ensures Flask remains the interface, services coordinate workflows, and models perform AI inference.

---

## Services Layer Responsibilities

The services layer should:
- orchestrate workflows,
- validate and normalize domain inputs,
- coordinate `models/` and `utils/`,
- format recommendation results for templates.

Important constraints:
- Services should never manipulate `pandas.DataFrame` objects directly.
- Dataset loading and preprocessing belong in `utils/` or `models/`.
- Services should operate on domain objects such as `UserRequest`, `RecommendationResult`, and `MovieRecommendation`.

---

## Explainable AI

The recommendation architecture should support explainability for each returned movie.

Each recommendation should eventually include:
- similarity score,
- matched semantic themes,
- explanation text.

Example explanation:

"Recommended because your request closely matches themes of hope, perseverance, and emotional recovery."

Explainability is a responsibility of the Recommendation Engine, not the Flask route.

---

## Dependencies

The core runtime dependencies should include:

- `Flask`
- `sentence-transformers`
- `scikit-learn`
- `pandas`
- `numpy`
- `requests`
- `python-dotenv`

Optional:
- `rich` or `loguru`
- `pytest`

---

## Notes on Current State

- The repository is scaffolded but contains no implementation.
- `app.py`, `routes/`, `services/`, `models/`, and `utils/` are currently empty scaffolds.
- `dataset/` is expected to hold manual TMDB files and a cache folder.
- `templates/` is currently empty.
- `requirements.txt` should be normalized before implementation, but no code changes are being made now.

---

## Recommended Next Steps

1. Confirm this architecture and the startup lifecycle.
2. Confirm the cache structure and dataset expectations.
3. Confirm the separation between Embedding Engine and Recommendation Engine.
4. After approval, proceed with Phase 0 implementation planning.

> This document is architecture-only. No application code is written here.
