import pandas as pd

# 1. Load the specific sheet
print("Loading 'Dataset (from Q2 2016)'...")
file_path = 'world_bank_2025.xlsx'
df = pd.read_excel(file_path, sheet_name='Dataset (from Q2 2016)')

# 2. Define African countries list (Make sure these match the 'source_name'/'destination_name' style)
african_countries = [
    'Nigeria', 'Ghana', 'Kenya', 'South Africa', 'Egypt', 'Ethiopia',
    'Uganda', 'Rwanda', 'Senegal', 'Tanzania', 'Congo, Dem. Rep.', "Cote d'Ivoire",
    'Morocco', 'Tunisia', 'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso',
    'Cameroon', 'Cabo Verde', 'Central African Republic', 'Chad', 'Comoros',
    'Congo, Rep.', 'Djibouti', 'Equatorial Guinea', 'Eritrea', 'Eswatini',
    'Gabon', 'Gambia, The', 'Guinea', 'Guinea-Bissau', 'Lesotho', 'Liberia',
    'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius',
    'Mozambique', 'Namibia', 'Niger', 'Sao Tome and Principe', 'Seychelles',
    'Sierra Leone', 'Somalia', 'South Sudan', 'Sudan', 'Togo', 'Zambia', 'Zimbabwe'
]

# 3. Clean names to avoid spacing issues
df['source_name'] = df['source_name'].astype(str).str.strip()
df['destination_name'] = df['destination_name'].astype(str).str.strip()

# 4. THE BIG CHANGE: Bidirectional Filter
# We want rows where (Africa is Sender) OR (Africa is Receiver)
print("Filtering for all Africa-related corridors (Inbound, Outbound, and Intra-Africa)...")
africa_related_df = df[
    (df['source_name'].isin(african_countries)) | 
    (df['destination_name'].isin(african_countries))
].copy()

# 5. Clean numeric columns (using the exact names we found earlier)
cols_to_fix = ['cc1 lcu fee', 'cc1 fx margin', 'cc1 total cost %']
for col in cols_to_fix:
    if col in africa_related_df.columns:
        africa_related_df[col] = pd.to_numeric(africa_related_df[col], errors='coerce')

# 6. Tag the transactions for easier Analytics later
# This helps Power BI differentiate between types
def categorize_corridor(row):
    src_is_africa = row['source_name'] in african_countries
    dest_is_africa = row['destination_name'] in african_countries
    
    if src_is_africa and dest_is_africa:
        return 'Intra-Africa'
    elif src_is_africa:
        return 'Outbound (Africa to World)'
    else:
        return 'Inbound (World to Africa)'

africa_related_df['flow_type'] = africa_related_df.apply(categorize_corridor, axis=1)

# 7. Select final columns including the new 'flow_type'
final_cols = [
    'period', 'source_name', 'destination_name', 'flow_type', 'firm', 'firm_type', 
    'cc1 lcu fee', 'cc1 fx margin', 'cc1 total cost %'
]
africa_related_df = africa_related_df[final_cols]

# 8. Save the refined CSV
africa_related_df.to_csv('africa_remittances_full.csv', index=False)

print(f"Success! {len(africa_related_df)} rows saved.")
print(africa_related_df['flow_type'].value_counts())

# Rename columns to be SQL-friendly (no spaces or % signs)
africa_related_df = africa_related_df.rename(columns={
    'source_name': 'source_country',
    'destination_name': 'destination_country',
    'firm': 'firm_name',
    'cc1 lcu fee': 'fee_lcu',
    'cc1 fx margin': 'fx_margin_pct',
    'cc1 total_cost %': 'total_cost_pct' # Match the column name from your previous run
})

#posetgres

import pandas as pd
from sqlalchemy import create_engine

# --- PART 1: EXTRACT & TRANSFORM (What you already did) ---
df = pd.read_excel('world_bank_2025.xlsx', sheet_name='Dataset (from Q2 2016)')

# ... (All your filtering and cleaning code goes here) ...

# --- PART 2: THE "PUSH" TO SQL (Add this at the very bottom) ---

# 1. Database Credentials
DB_USER = 'postgres'
DB_PASS = 'elric' # Change to your actual pgAdmin password
DB_NAME = 'remittance_db'  # Ensure this database exists in pgAdmin

# 2. Create the Connection
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@localhost:5432/{DB_NAME}')

try:
    print("Connecting to PostgreSQL...")
    
    # 3. Clean column names so SQL likes them (removes spaces/symbols)
    africa_related_df.columns = [
        col.lower().replace(' ', '_').replace('%', 'pct').replace('cc1_', '') 
        for col in africa_related_df.columns
    ]
    
    # 4. The Magic Line: This creates the table AND moves the data
    africa_related_df.to_sql('africa_remittances', engine, if_exists='replace', index=False)
    
    print("🚀 Success! Data is now in PostgreSQL.")

except Exception as e:
    print(f"❌ Error: {e}")