# 🛠️ SweetSwap AI - Development Guide

> **Developer documentation and setup instructions**

For project overview and features, see [README.md](README.md).

This document contains technical setup instructions, architecture details, and development milestones for contributors.

---

## Overview

SweetSwap AI is an MVP AI nutrition assistant focused on diabetes-friendly drink substitutions. This repo contains the core scaffolding and implementation details.

### Repo layout
- `backend/` – FastAPI app, DB models, services, and requirements
- `frontend/` – placeholder for Streamlit/React UI work
- `data/` – CSV seeds, exports, and nutrition dumps
- `scrapers/` – ingestion scripts for cafe menus
- `notebooks/` – experimentation space (LLM prompting, EDA)

### Milestone cheat sheet
1. **Environment & repo setup**
   - `python -m venv .venv && .\.venv\Scripts\activate`
   - `pip install -r backend/requirements.txt`
   - Copy `.env.example` → `.env` and fill in values
   - Optional: `pip install pre-commit` for lint hooks
2. **Backend core API**
   - Run `uvicorn app.main:app --reload --port 8000 --app-dir backend`
   - Test `/substitute` via `httpie` or `curl`
3. **Database & cache**
   - Use Postgres locally (see instructions below)
   - Once DB URL is set, Alembic migrations can be added later
4. **Nutrition API integration**
   - Start with USDA FoodData Central (free, generous rate limits)
   - Wrap calls inside `app/services/nutrition.py`
5. **Scraper automation**
   - Build scripts in `scrapers/` that write into `data/` then DB
6. **Frontend chatbot UI**
   - Streamlit starter recommended for fastest iteration

### Database setup guide (PostgreSQL)
1. Install PostgreSQL (15+) locally via [https://www.postgresql.org/download/](https://www.postgresql.org/download/). Include pgAdmin or use CLI.
2. Create a database and user:
   ```ps1
   psql -U postgres -c "CREATE DATABASE sweetswap;"
   psql -U postgres -c "CREATE USER sweetswap_user WITH PASSWORD 'change-me';"
   psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE sweetswap TO sweetswap_user;"
   ```
3. Update `.env` with:
   ```
   DATABASE_URL=postgresql+psycopg2://sweetswap_user:change-me@localhost:5432/sweetswap
   ```
4. From the repo root run:
   ```ps1
   .\.venv\Scripts\activate
   python backend/app/db_init.py
   ```
   This script creates the tables defined in `app/models.py`.
5. (Optional) Install Redis locally or use Docker: `docker run -p 6379:6379 redis:7`.

### Nutrition API recommendation
- **USDA FoodData Central**: Free, detailed nutrient breakdown (sugar, caffeine, etc.). API key is instant. Ideal for MVP.
- **Nutritionix**: Natural-language endpoint with limited free tier. Great for later upgrades.
- **Edamam / Spoonacular**: Paid or restricted trials; defer unless coverage gaps appear.

### Color palette reference
Use these hex values in the frontend:
- Cardinal `#C52233`
- Madder `#A51C30`
- Auburn `#A7333F`
- Burgundy `#74121D`
- Chocolate Cosmos `#580C1F`

### Next steps
- Fill `data/seed_substitutions.csv` with 25–30 curated drinks.
- Implement substitution lookup + LLM fallback in `app/services/substitution.py`.
- Build a Streamlit UI in `frontend/` for quick demos; later migrate to React if needed.

