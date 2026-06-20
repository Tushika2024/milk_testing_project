import pandas as pd
import os
from urllib.parse import quote_plus


from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# print(os.getenv("DB_HOST"))
# print(os.getenv("DB_USER"))
# print(os.getenv("DB_PASSWORD"))
# print(os.getenv("DB_NAME"))

password = quote_plus(os.getenv("DB_PASSWORD"))
# Read Excel
df = pd.read_excel(
    "ComplaintsData.xlsx"
)

# Clean columns
df.columns = df.columns.str.strip()

# Convert dates
df["LogedDate"] = pd.to_datetime(
    df["LogedDate"],
    errors="coerce"
)

df["resolveDate"] = pd.to_datetime(
    df["resolveDate"],
    errors="coerce"
)

# Create engine
engine = create_engine(
    f"mysql+mysqlconnector://"
    f"{os.getenv('DB_USER')}:{password}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)

# Upload table
df.to_sql(
    name="complaints",
    con=engine,
    if_exists="replace",
    index=False
)

print(
    f"{len(df)} rows loaded successfully"
)