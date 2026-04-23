# 🌍 Africa Remittance Cost Analysis

A end-to-end data pipeline and analytics project analyzing the cost of sending money to, from, and within Africa — using real World Bank data spanning 2016 to 2025.

---

## 📌 The Problem

Sending money across Africa is expensive. The UN Sustainable Development Goal 10.c targets remittance costs below **3% by 2030**. This project uses nearly a decade of quarterly data to ask: *how far off is Africa from that target — and who is responsible for the gap?*

**Key finding:** Intra-Africa transfers average **14.21%** in fees — more than double the cost of inbound transfers from the rest of the world (**6.56%**). Africa is nowhere near the 3% SDG target.

---

## 📊 Dashboard Preview

<img width="976" height="551" alt="dashboard_preview png" src="https://github.com/user-attachments/assets/520df42b-9818-412a-8ea2-6a5a61fb9a41" />

![Africa Remittance Cost Dashboard](dashboard_preview.png)

> Built in Power BI, connected live to PostgreSQL.

---

## 🏗️ Project Architecture

```
World Bank Excel (47,000+ rows)
        ↓
   clean_data.py         ← Python + Pandas (Extract, Transform)
        ↓
   PostgreSQL            ← africa_remittances table (Load)
        ↓
   main.py (FastAPI)     ← REST API serving analytics endpoints
        ↓
   Power BI Dashboard    ← Live visualization layer
```

---

## 📁 Repository Structure

```
africa-remittance-analysis/
│
├── clean_data.py              # Data cleaning & ingestion pipeline
├── check_sheets.py            # Data validation & column inspection
├── main.py                    # FastAPI application
├── africa_remittances_clean.csv  # Cleaned Africa-filtered dataset
├── requirements.txt           # Python dependencies
└── README.md
```

---

## ⚙️ Pipeline Breakdown

### 1. Ingestion & Cleaning (`clean_data.py`)
- Loads the World Bank Remittance Prices Worldwide dataset (Excel)
- Filters for all Africa-related corridors bidirectionally — rows where Africa is either the source or destination
- Classifies each transaction into one of three flow types:
  - `Intra-Africa` — both source and destination are African countries
  - `Outbound (Africa to World)` — African source, non-African destination
  - `Inbound (World to Africa)` — non-African source, African destination
- Cleans numeric columns (`fee_lcu`, `fx_margin_pct`, `total_cost_pct`)
- Renames columns to SQL-friendly format
- Pushes cleaned data to PostgreSQL using SQLAlchemy

### 2. Storage (`PostgreSQL`)
- Database: `remittance_db`
- Table: `africa_remittances`
- 47,269 rows | 9 columns | Quarterly data from Q2 2016 to Q1 2025

**Schema:**
| Column | Type | Description |
|---|---|---|
| period | text | Quarter (e.g. 2024_1Q) |
| source_country | text | Sending country |
| destination_country | text | Receiving country |
| flow_type | text | Intra-Africa / Inbound / Outbound |
| firm_name | text | Provider name |
| firm_type | text | Bank / MTO / Hybrid |
| fee_lcu | float | Fee in local currency |
| fx_margin_pct | float | FX margin percentage |
| total_cost_pct | float | Total cost as % of transfer amount |

### 3. API Layer (`main.py`)
Built with **FastAPI**. Four endpoints:

| Endpoint | Description |
|---|---|
| `GET /` | Health check |
| `GET /analytics/summary` | Average cost by flow type |
| `GET /cheapest/{country}` | Top 5 cheapest providers for a destination |
| `GET /analytics/firms-comparison` | All firms ranked by average fee |
| `GET /analytics/firm-type-deep-dive` | Banks vs MTOs vs Hybrids comparison |

### 4. Visualization (Power BI)
Three-page interactive dashboard connected live to PostgreSQL:

- **Page 1 — The Big Picture:** KPI cards, cost by flow type, 2016–2025 trend line
- **Page 2 — Who Is Charging What:** Firm type comparison, fee vs FX margin breakdown, firm pricing table
- **Page 3 — Corridor Explorer:** Interactive slicers, cheapest corridors table, corridor cost heatmap

---

## 🔑 Key Findings

- **Intra-Africa transfers (14.21%)** cost more than twice inbound transfers (6.56%) — despite shorter distances
- **Traditional Banks (avg ~16%)** consistently charge more than Digital MTOs
- **The SDG 10.c 3% target** remains far out of reach across all three flow types as of Q1 2025
- **Intra-Africa costs have not meaningfully declined** over the 9-year period, suggesting structural barriers beyond competition

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data Processing | Python, Pandas |
| Database | PostgreSQL, SQLAlchemy, psycopg2 |
| API | FastAPI, Uvicorn |
| Visualization | Power BI Desktop |
| Data Source | [World Bank Remittance Prices Worldwide](https://remittanceprices.worldbank.org/) |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas sqlalchemy psycopg2-binary fastapi uvicorn openpyxl
```

### 1. Set up PostgreSQL
Create a database called `remittance_db` in PostgreSQL.

### 2. Run the pipeline
```bash
python clean_data.py
```

### 3. Start the API
```bash
uvicorn main:app --reload
```

### 4. Open Power BI
Connect to PostgreSQL → `localhost` → `remittance_db` → `africa_remittances`

---

## 📌 Data Source

**World Bank Remittance Prices Worldwide**
> A global dataset tracking the cost of sending remittances across 365+ country corridors, published quarterly since 2008.

🔗 https://remittanceprices.worldbank.org/

City night scene. Retrieved from Freepik. Used for presentation purposes only.

---

## 👤 Author

**Emmanuel Balogun**
Data Analyst | Lagos, Nigeria
[LinkedIn](https://linkedin.com/in/emmanuel-balogun-kehinde) · [GitHub](https://github.com/BalogunEmmanuelKehinde)
