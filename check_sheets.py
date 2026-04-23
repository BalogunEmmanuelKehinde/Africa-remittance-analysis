import pandas as pd

# Load just the first few rows to save time
df = pd.read_excel('world_bank_2025.xlsx', sheet_name='Dataset (from Q2 2016)', nrows=5)

print("The actual column names in your file are:")
print(df.columns.tolist())
import pandas as pd

# Load just the first few rows to save time
df = pd.read_excel('world_bank_2025.xlsx', sheet_name='Dataset (from Q2 2016)', nrows=5)

print("The actual column names in your file are:")
print(df.columns.tolist())