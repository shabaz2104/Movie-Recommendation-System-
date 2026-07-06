# AGENTS.md

## Project

MoodFlix - AI Mood-Based Movie Recommendation System

## Architecture Rules

- app.py should remain small.
- Flask routes belong in routes/.
- Business logic belongs in services/.
- Machine learning belongs in models/.
- Helper functions belong in utils/.
- Templates belong in templates/.
- CSS/JS belong in static/.

## Coding Style

- Python 3.13
- Follow PEP8
- Modular code
- Type hints
- No duplicated logic
- No hardcoded secrets
- Use .env

## Development Philosophy

Implement one feature at a time.

Every feature must:
- Work completely.
- Be tested.
- Be documented.

Never refactor unrelated code.

Never introduce unnecessary dependencies.

Explain architectural decisions before making major changes.