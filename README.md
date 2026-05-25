# Hormuz Trade Analytics — Trade Analytics API with Visual Dashboard


---

## Project Structure

```
trade_analytics_project/
│
├── app/                          ← Engineer 2 & 3
│   ├── main.py                   ← FastAPI app entry point
│   ├── config.py                 ← Settings (pydantic-settings)
│   ├── database.py               ← SQLAlchemy engine + session
│   ├── models.py                 ← ORM models
│   ├── schemas.py                ← Pydantic request/response schemas
│   ├── crud.py                   ← DB operations
│   │
│   ├── routers/                  ← Engineer 3
│   │   ├── trade.py              ← GET /trade/top-countries, /trade/records
│   │   ├── analytics.py          ← GET /analytics/region-summary, /analytics/trade-trends
│   │   └── prediction.py         ← POST /ml/predict-growth
│   │
│   └── services/                 ← Engineer 3
│       ├── analytics_service.py  ← Business logic for analytics
│       └── ml_service.py         ← Linear regression inference
│
├── notebooks/                    ← Engineer 1
│   └── analysis.ipynb            ← PySpark + Plotly + Statsmodels + Sklearn
│
├── dataset/
│   └── hormuz_trade_tier_continental_2026.csv
│   └── (generated after running notebook):
│       ├── cleaned_trade_data.csv
│       ├── top_countries.csv
│       ├── region_summary.csv
│       ├── monthly_trend.csv
│       └── model_meta.json        ← model coefficients for prediction API
│
├── sql/
│   └── schema.sql
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## Engineer Division

| Engineer       | Responsibility                                                                                                              | Key Files                                                              |
| -------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **Engineer 1** | PySpark data analysis · Feature engineering · 5 Plotly visualisations · Linear Regression (PySpark MLlib + Statsmodels OLS) | `notebooks/analysis.ipynb`                                             |
| **Engineer 2** | PostgreSQL schema design · SQLAlchemy ORM models · SQL DDL/DML/DCL · Stored procedure · Views · CRUD layer                  | `sql/schema.sql` · `app/models.py` · `app/database.py` · `app/crud.py` |
| **Engineer 3** | FastAPI app · 4 API endpoints · Service layer · ML inference service · Swagger docs · Docker setup                          | `app/main.py` · `app/routers/` · `app/services/`                       |

---

## Quick Start

### Option A — Docker Compose (recommended)

```bash
# 1. Clone / unzip the project
cd trade_analytics_project

# 2. Start all services
docker compose up --build

# API          → http://localhost:8000/docs
# Google Colab → https://colab.research.google.com/drive/1q4QgPEhFLk6aR_jashTsjaXhxVEBoiAJ#scrollTo=FwdKdsAQ7Lgt
# Postgres     → localhost:5432/trade_analytics
```

### Option B — Local setup

```bash
# 1. Create virtual environment
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start PostgreSQL and apply schema
psql -U postgres -c "CREATE DATABASE trade_analytics;"
psql -U postgres -d trade_analytics -f sql/schema.sql

# 4. Copy .env and adjust credentials
cp .env .env.local

# 5. Run the notebook first (generates model_meta.json + CSVs)
jupyter notebook notebooks/analysis.ipynb

# 6. Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

> If you use a custom virtual environment folder such as `myen`, activate it first or run the exact interpreter:
>
> Windows (PowerShell):
> ```powershell
> .\myen\Scripts\Activate.ps1
> python -m pip install -r requirements.txt
> python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
> ```
>
> If you still see `ModuleNotFoundError: No module named 'jose'`, run:
> ```powershell
> .\myen\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
> ```
```

---

## API Endpoints

| Method | Endpoint                    | Description                           |
| ------ | --------------------------- | ------------------------------------- |
| `GET`  | `/`                         | Root info                             |
| `GET`  | `/health`                   | DB health check                       |
| `GET`  | `/trade/records`            | Paginated vessel records              |
| `GET`  | `/trade/records/{id}`       | Single record                         |
| `GET`  | `/trade/top-countries`      | Top countries by vessel volume        |
| `GET`  | `/analytics/region-summary` | Continent-wise trade distribution     |
| `GET`  | `/analytics/trade-trends`   | Monthly trend time-series             |
| `POST` | `/ml/predict-growth`        | Predict total transit cost (LR model) |
| `GET`  | `/ml/model-info`            | Model metadata / evaluation metrics   |

Full interactive docs at **`/docs`** (Swagger UI) or **`/redoc`**.

### Example: Predict transit cost

```bash
curl -X POST http://localhost:8000/ml/predict-growth \
  -H "Content-Type: application/json" \
  -d '{
    "toll_usd": 2000000,
    "insurance_cost_usd": 1000000,
    "days_delayed": 0,
    "extra_fuel_tonnes": 0,
    "reroute_penalty_usd": 0,
    "estimated_cargo_value_usd": 80000000,
    "trade_tier_label": 1,
    "is_rerouted": 0
  }'
```

---

## ML Model

**Algorithm:** Linear Regression (trained with PySpark MLlib, OLS diagnostics via Statsmodels)

**Target:** `total_transit_cost_usd`

**Features:**

- `toll_usd` — transit toll paid
- `insurance_cost_usd` — insurance cost for the voyage
- `days_delayed` — days held up
- `extra_fuel_tonnes` — additional fuel from rerouting
- `reroute_penalty_usd` — financial penalty from reroute
- `estimated_cargo_value_usd` — value of cargo
- `trade_tier_label` — encoded tier (0=Privileged, 1=Taxed, 2=Blocked)
- `is_rerouted` — binary flag

**Workflow:** Trained in notebook → coefficients serialised to `dataset/model_meta.json` → loaded by `ml_service.py` at API startup (no live Spark needed at runtime).

---

## Visualisations (generated in notebook)

| File                      | Type       | Content                                 |
| ------------------------- | ---------- | --------------------------------------- |
| `top_countries.png`       | Bar chart  | Top 15 flag nations by vessel count     |
| `region_distribution.png` | Dual pie   | Vessel count + cargo value by continent |
| `trade_trend.png`         | Line chart | Monthly vessel count + transit cost     |
| `correlation_heatmap.png` | Heatmap    | Pearson correlation of numeric features |
| `forecast_plot.png`       | Scatter    | Actual vs predicted transit cost        |

---

## Database Schema (PostgreSQL)

Three tables under the `trade` schema:

- **`trade_categories`** — lookup/reference table for commodity types, tiers, escort status
- **`country_summary`** — pre-aggregated country-level KPIs (refreshed via stored procedure)
- **`trade_records`** — main fact table with one row per vessel transit

Views provided:

- `v_top_countries` — ranked country leaderboard
- `v_region_summary` — continent aggregates
- `v_monthly_trend` — time-series aggregates
- `v_enriched_records` — joined fact + dimension view

DCL roles:

- `trade_readonly` → SELECT only (analyst_user)
- `trade_readwrite` → SELECT/INSERT/UPDATE/DELETE (api_user)
- `trade_admin` → ALL PRIVILEGES (admin_user)

---

## Checklist

- [x] PySpark data cleaning (missing values, duplicates, type correction)
- [x] Feature engineering (is_rerouted, cost_per_cargo, risk_ratio, year/month)
- [x] Summary statistics
- [x] Top trading countries analysis
- [x] Region-wise trade summary
- [x] Monthly trade trend analysis
- [x] 5 Plotly visualisations (3 mandatory + 2 optional)
- [x] Linear Regression (PySpark MLlib + Statsmodels OLS)
- [x] PostgreSQL DDL / DML / DCL / Constraints / Aggregations / Joins
- [x] SQLAlchemy ORM models + session management
- [x] FastAPI with 4+ endpoints
- [x] Pydantic v2 request/response schemas
- [x] Prediction API backed by trained LR model
- [x] Docker + docker-compose (bonus)
- [x] Logging (bonus)
- [x] Exception handling (bonus)
- [x] Clean modular structure (bonus)
