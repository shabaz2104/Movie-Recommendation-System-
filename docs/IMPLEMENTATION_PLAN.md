# MoodFlix Implementation Plan

This document defines a phase-by-phase roadmap for implementing the MoodFlix recommendation system.

Each phase is intentionally limited in scope, with a clear objective, the files involved, responsibilities, and expected output.

---

## Phase 1: Project Bootstrap

### Objective
Create the minimal application scaffolding and confirm the architecture without adding recommendation logic.

### Deliverables
- `app.py` remains small.
- `config.py` defines config variables.
- `routes/` contains route blueprints.
- `services/` exposes workflow entry points.
- `models/` and `utils/` remain scaffolded packages.
- `templates/` contains a basic landing page.

### Files Involved
- `app.py`
- `config.py`
- `routes/__init__.py`
- `services/__init__.py`
- `models/__init__.py`
- `utils/__init__.py`
- `templates/index.html`
- `static/css/`
- `static/js/`

### Responsibilities
- App initialization must stay small.
- Flask routes must only render templates and call services.
- Services must define domain workflows.
- No ML or embedding logic yet.

### Expected Output
- A working Flask scaffold.
- Clear separation between interface, services, and model boundaries.
- Project ready for AI pipeline implementation.

---

## Phase 2: Dataset Pipeline

### Objective
Implement dataset ingestion and preprocessing for TMDB movie metadata.

### Deliverables
- Load `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`.
- Clean missing values.
- Combine `title`, `genres`, `keywords`, and `overview` into a single semantic text field.
- Prepare the movie metadata for embedding.

### Files Involved
- `utils/` (dataset helpers)
- `models/` or `utils/` for preprocessing utilities
- `dataset/` files

### Responsibilities
- `utils/` loads and preprocesses dataset files.
- Preprocessing handles missing values and text combination.
- Services do not directly manipulate DataFrames.

### Expected Output
- A clean dataset object with a combined semantic text field.
- A documented dataset schema.

---

## Phase 3: Embedding Engine

### Objective
Implement the embedding lifecycle and caching layer.

### Deliverables
- Load `all-MiniLM-L6-v2` model.
- Generate embeddings for the combined movie text.
- Store embeddings in `dataset/cache/movie_embeddings.pkl`.
- Load cached embeddings on startup.

### Files Involved
- `models/` for embedding engine logic
- `dataset/cache/`
- `config.py`

### Responsibilities
- Embedding Engine loads the transformer and generates embeddings.
- Embedding generation happens once and is cached.
- Discovery and loading of cached embeddings happen on startup.

### Expected Output
- A reusable embedding engine.
- Movie embeddings cached on disk.
- Startup lifecycle documented in architecture.

---

## Phase 4: Recommendation Engine

### Objective
Build the semantic recommendation engine with similarity ranking and explainability.

### Deliverables
- Cosine similarity ranking between user query embedding and movie embeddings.
- Top-N movie selection.
- Explainability metadata for each recommendation.

### Files Involved
- `models/` for recommendation engine logic
- `services/` to orchestrate query flow

### Responsibilities
- Recommendation Engine performs similarity, ranking, filtering, and explainability.
- Services coordinate the workflow and return domain objects.

### Expected Output
- Semantic recommendations generated from query embeddings and cached movie embeddings.
- Explainability support for each recommendation.

---

## Phase 5: Semantic Intent Analysis

### Objective
Implement semantic intent analysis for user text.

### Deliverables
- Convert user text into semantic intent embeddings.
- Reflect emotion, intent, and context in the recommendation input.
- Replace any keyword-based mood detection language.

### Files Involved
- `services/` for input handling
- `models/` for embedding inference

### Responsibilities
- Semantic Intent Analysis converts user requests into embeddings.
- Services treat analysis output as domain intent representation.

### Expected Output
- User text is understood semantically.
- The system recommends movies based on user intent and emotional context.

---

## Phase 6: Frontend

### Objective
Build the user-facing interface for submitting requests and viewing recommendations.

### Deliverables
- Server-rendered templates with recommendation results.
- Form submission for natural language input.
- Display of movie title, poster, summary, and explainability.

### Files Involved
- `templates/`
- `static/css/`
- `static/js/`
- `routes/`
- `services/`

### Responsibilities
- Templates must render domain results from services.
- UI must be responsive and user-friendly.
- No REST API unless requested later.

### Expected Output
- A polished server-rendered UI for MoodFlix.
- Clear display of semantic recommendations.

---

## Phase 7: TMDB Integration

### Objective
Add TMDB poster and movie detail enrichment.

### Deliverables
- TMDB API helper functions.
- Poster URLs and metadata enrichment.
- Configured secure API key usage.

### Files Involved
- `utils/` for TMDB API helpers
- `config.py`
- `services/` for enrichment workflow

### Responsibilities
- TMDB helpers manage external API calls.
- Services integrate TMDB metadata into recommendations.
- No API keys should be hardcoded.

### Expected Output
- Recommended movies include TMDB poster images and extra metadata.
- TMDB API key loaded from environment.

---

## Phase 8: Testing

### Objective
Add tests that validate the recommendation flow and architecture.

### Deliverables
- Unit tests for the embedding engine.
- Unit tests for the recommendation engine.
- Tests for service orchestration.
- Optional route-level tests for template rendering.

### Files Involved
- `tests/`
- `services/`
- `models/`

### Responsibilities
- Tests validate AI logic and workflow separation.
- Services should be tested using domain objects.

### Expected Output
- Reliable test coverage for core components.
- Confidence in architecture and behavior.

---

## Phase 9: Deployment

### Objective
Prepare the app for local deployment and developer use.

### Deliverables
- Run instructions in `README.md`.
- Optional development scripts or simple `run` command.
- Checklist for dataset placement and environment setup.

### Files Involved
- `README.md`
- `config.py`
- `docs/`

### Responsibilities
- Ensure developers can run MoodFlix locally.
- Document environment variables and dataset expectations.

### Expected Output
- A complete developer-ready application.
- Clear deployment and setup documentation.

---

## Phase Sequencing and Constraints

- Each phase is isolated and small.
- No application code should be added until approved for that phase.
- The proposed plan follows the architecture rules: no training scripts, no dataset fetch scripts, no REST API unless requested, and no code in `app.py` beyond bootstrap.

> This implementation plan is intentionally code-free and architecture-first.
