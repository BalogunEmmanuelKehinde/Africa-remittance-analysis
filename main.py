from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Database connection helper
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="remittance_db", 
        user="postgres",         
        password="your-password" 
    )

@app.get("/")
def home():
    return {"message": "Africa Remittance API is Online"}

# 1. Summary Endpoint
@app.get("/analytics/summary")
def get_summary():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = """
    SELECT flow_type, 
           ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_cost,
           COUNT(*) as total_observations
    FROM africa_remittances
    GROUP BY flow_type
    ORDER BY avg_cost DESC;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# 2. Cheapest Endpoint
@app.get("/cheapest/{country}")
def get_cheapest(country: str):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = """
    SELECT firm_name, total_cost_pct, flow_type, source_country
    FROM africa_remittances
    WHERE destination_country ILIKE %s 
    AND total_cost_pct > 0 
    ORDER BY total_cost_pct ASC
    LIMIT 5;
    """
    cur.execute(query, (f"%{country}%",))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# 3. Firm Comparison Endpoint
@app.get("/analytics/firms-comparison")
def get_firm_comparison():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = """
    SELECT 
        firm_name, 
        flow_type, 
        ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_fee_pct,
        COUNT(*) as record_count
    FROM africa_remittances
    WHERE total_cost_pct > 0 
    GROUP BY firm_name, flow_type
    ORDER BY firm_name ASC, avg_fee_pct ASC;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# 4. Firm Type Deep Dive Endpoint
@app.get("/analytics/firm-type-deep-dive")
def get_firm_type_deep_dive():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """
    SELECT 
        CASE 
            WHEN firm_type ILIKE '%Bank%' AND firm_type ILIKE '%Operator%' THEN 'Hybrid (Bank + MTO)'
            WHEN firm_type ILIKE '%Bank%' THEN 'Traditional Bank'
            WHEN firm_type ILIKE '%MTO%' OR firm_type ILIKE '%Operator%' THEN 'Digital/MTO'
            ELSE 'Other'
        END as simplified_type,
        flow_type,
        ROUND(CAST(AVG(total_cost_pct) AS numeric), 2) as avg_fee_pct,
        COUNT(*) as record_count
    FROM africa_remittances
    WHERE total_cost_pct > 0
    GROUP BY 1, 2 
    ORDER BY simplified_type ASC, flow_type ASC;
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results