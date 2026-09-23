import pandas as pd
from sqlalchemy import create_engine

# Load cleaned CSV
df = pd.read_csv("cleaned_earthquake.csv")

# Connect Python to MySQL
engine = create_engine(
    "mysql+pymysql://root:555555@localhost:3306/Global_Seismic_trends_db"
)

# Insert data into MySQL table
df.to_sql(
    "earthquake",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data inserted successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))