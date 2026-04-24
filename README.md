# 🌍 Africa Remittance Cost Analysis

An end-to-end data pipeline and investigative analytics project examining the true cost of sending money to, from, and within Africa — using real World Bank data spanning 2016 to 2025.

---

## 📌 The Finding That Started Everything

> A Tanzanian bank charges **91%** to send money to Uganda.
> Western Union charges **8%** on the exact same route.
> Same corridor. Same quarter. 10x the price.

This project was built to understand why — and whether Africa is on track to meet the UN SDG 10.c target of **3% remittance costs by 2030**.

**Spoiler: The trend is going the wrong direction.**

---

## 📊 Dashboard Preview

### Page 1 — The Big Picture
<img width="976" height="551" alt="dashboard_preview png" src="https://github.com/user-attachments/assets/afc2e9de-f1fe-430d-abec-c2a937667492" />

![Africa Remittance Cost Dashboard](dashboard_preview.png)

### Page 4 — The Deep Dive
<img width="888" height="498" alt="dashb board page 4" src="https://github.com/user-attachments/assets/e720f26b-d2c7-42f3-863a-d61e4b0df739" />

![Deep Dive](deep_dive_preview.png)

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
   Power BI Dashboard    ← 4-page live visualization layer
```

---

## 📁 Repository Structure

```
africa-remittance-analysis/
│
├── clean_data.py                  # Data cleaning & ingestion pipeline
├── check_sheets.py                # Data validation & column inspection
├── main.py                        # FastAPI application
├── queries.sql                    # Key analytical queries
├── africa_remittances_clean.csv   # Cleaned Africa-filtered dataset
└── README.md
```

---

## ⚙️ Pipeline Breakdown

### 1. Ingestion & Cleaning (`clean_data.py`)
- Loads the World Bank Remittance Prices Worldwide dataset (Excel)
- Filters for all Africa-related corridors bidirectionally — rows where Africa is either the source or destination
- Removes promotional noise (negative cost percentages) that would distort analysis
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
Built with **FastAPI**. Five endpoints:

| Endpoint | Description |
|---|---|
| `GET /` | Health check |
| `GET /analytics/summary` | Average cost by flow type |
| `GET /cheapest/{country}` | Top 5 cheapest providers for a destination |
| `GET /analytics/firms-comparison` | All firms ranked by average fee |
| `GET /analytics/firm-type-deep-dive` | Banks vs MTOs vs Hybrids comparison |

### 4. Visualization (Power BI)
Four-page interactive dashboard connected live to PostgreSQL:

- **Page 1 — The Big Picture:** KPI cards (14.21% / 6.56% / 14.98%), cost by flow type, 2016–2025 trend line
- **Page 2 — Who Is Charging What:** Firm type comparison, fee vs FX margin breakdown, full firm pricing table
- **Page 3 — Corridor Explorer:** Interactive slicers, cheapest corridors table, corridor cost heatmap
- **Page 4 — The Deep Dive:** Tanzania → Uganda provider comparison, 2023–2025 quarterly trend

---

## 🔑 Key Findings

### Finding 1 — The Headline Gap
Sending money **into** Africa from the world (6.56%) costs less than half of sending money **within** Africa (14.21%). Despite shorter distances, intra-Africa transfers are dramatically more expensive.

### Finding 2 — Costs Are Getting Worse, Not Better
When drilling into recent quarterly data, Intra-Africa costs are **rising**:

| Period | Intra-Africa | Inbound | Outbound |
|---|---|---|---|
| 2023_1Q | 15.41% | 6.66% | 12.10% |
| 2024_1Q | 14.41% | 5.84% | 16.76% |
| 2024_4Q | 15.37% | 6.08% | 15.14% |
| 2025_1Q | **17.14%** | 6.02% | 15.12% |

The UN SDG 10.c target is **3% by 2030**. Every flow type remains 2–5x above that target with 4 years remaining.

### Finding 3 — The Smoking Gun (Tanzania → Uganda, Q1 2025)
| Provider | Type | Avg Cost |
|---|---|---|
| National Bank of Commerce (NBC) | Bank | 91% |
| Stanbic Bank | Bank | 76% |
| CRDB Bank | Bank | 73% |
| NMB Bank | Bank | 70% |
| Western Union | MTO | 8% |
| MoneyGram | MTO | 8% |

MTOs operate profitably at 8% on the exact corridors where banks charge 70–91%. **This is not a structural cost problem. It is a competition and consumer awareness problem.**

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

**Dashboard Background Image**
> City night scene. Retrieved from [Freepik](https://www.freepik.com). Used for presentation purposes only.

---

## ⚠️ Disclaimer
This project is for educational and portfolio purposes only. 
All data is sourced from the World Bank Remittance Prices Worldwide 
public dataset. Findings reflect dataset averages and should not be 
used as financial advice. Individual transfer costs may vary by 
provider, amount, and time of transaction.

---

## 👤 Author

**Emmanuel Balogun**
Data Analyst | Lagos, Nigeria
[LinkedIn](https://linkedin.com/in/) · [GitHub](https://github.com/BalogunEmmanuelKehinde)
