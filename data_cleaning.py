import pandas as pd

# 1. Load raw data
df = pd.read_csv("raw_earthquake.csv")

print(df.head())
print(df.columns)

print("Original Shape:", df.shape)


# 2. Check Missing  / Null Values
print("/nMissing Values:")
print(df.isnull().sum())


# 3. Handle Missing Values
numeric_columns = ["nst", "dmin", "rms", "gap"]

for col in numeric_columns:
    df[col] = df[col].fillna(df[col].median())


# 4. Handle text/catagorical missing values
text_columns = ["alert", "felt", "cdi", "mmi"]

for col in text_columns:
    df[col] = df[col].fillna("Unknow")

print("/nRemaining Missing Values:")
print(df.isnull().sum())


# 5. Remove Duplicate Rows
df.drop_duplicates(inplace=True)

# 6. Removing invalid negative depth values
df = df[df["depth_km"] >= 0]

print(df.shape)

# 7. Convert Date & Time
df["time"] = pd.to_datetime(df["time"], errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], errors="coerce")


# 8. Correct Numeric Data Types
numeric_columns = [
    "latitude", "longitude", "depth_km", "mag",
    "sig", "nst", "dmin", "rms", "gap"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# 9. Check Outliers or unusally high/low
print("\nOutlier Check:")

for col in ["nst", "dmin", "rms", "gap"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = ((df[col] < lower) | (df[col] > upper)).sum()

    print(col, "Outliers:", outliers)



# 10. Final Missing Value Check
print("\nFinal Missing Values:")
print(df.isnull().sum())


#11. Final Shape
print("\nFinal Shape:", df.shape)

# 12. Save cleaned data
df.to_csv("cleaned_earthquake.csv", index=False)

print("\nCleaned data saved successfully!")


# ADD DERIVED COLUMNS:

df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

df["depth_category"] = df["depth_km"].apply(
    lambda x: "Shallow" if x < 70 else "Deep"
)

df["magnitude_category"] = df["mag"].apply(
    lambda x: "Strong" if x >= 5 else "Normal"
)

print("Derived Columns Added")
print(df.columns)
print(df.shape)


# Save final cleaned data
df.to_csv("cleaned_earthquake.csv", index=False)

print("Final Shape:", df.shape)
print("Cleaned data saved successfully!")