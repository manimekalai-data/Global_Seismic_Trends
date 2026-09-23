import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Global Seismic Trends",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# MySQL Connection
# -----------------------------
engine = create_engine(
    "mysql+pymysql://root:555555@localhost:3306/global_seismic_trends_db"
)

# Load data
df = pd.read_sql("SELECT * FROM earthquake", engine)

# -----------------------------
# Title
# -----------------------------
st.title("Global Seismic Trends: Data-Driven Earthquake Insights")
st.caption("Interactive analysis of global earthquake data")

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Earthquakes", f"{len(df):,}")
col2.metric("Average Magnitude", round(df["mag"].mean(), 2))
col3.metric("Maximum Magnitude", round(df["mag"].max(), 2))
col4.metric("Average Depth (km)", round(df["depth_km"].mean(), 2))
col5.metric("Tsunami Events", int(df["tsunami"].sum()))

# -----------------------------
# Filters
# -----------------------------
st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:
    selected_year = st.selectbox(
        "Select Year",
        ["All"] + sorted(df["year"].dropna().unique().tolist())
    )

with col2:
    selected_mag_type = st.selectbox(
        "Select Magnitude Type",
        ["All"] + sorted(df["magType"].dropna().unique().tolist())
    )

with col3:
    selected_type = st.selectbox(
        "Select Earthquake Type",
        ["All"] + sorted(df["type"].dropna().unique().tolist())
    )

min_mag = float(df["mag"].min())
max_mag = float(df["mag"].max())

selected_mag = st.slider(
    "Minimum Magnitude",
    min_mag,
    max_mag,
    min_mag
)

min_depth = float(df["depth_km"].min())
max_depth = float(df["depth_km"].max())

selected_depth = st.slider(
    "Minimum Depth (km)",
    min_depth,
    max_depth,
    min_depth
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["year"] == selected_year
    ]

if selected_mag_type != "All":
    filtered_df = filtered_df[
        filtered_df["magType"] == selected_mag_type
    ]

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]

filtered_df = filtered_df[
    (filtered_df["mag"] >= selected_mag)
    & (filtered_df["depth_km"] >= selected_depth)
]

st.info(f"Filtered Records: {len(filtered_df):,}")

# -----------------------------
# Earthquakes by Year
# -----------------------------
st.subheader("Earthquakes by Year")

yearly_data = (
    df.groupby("year")
    .size()
    .reset_index(name="Earthquake Count")
)

st.bar_chart(
    yearly_data.set_index("year")
)

# -----------------------------
# Earthquakes by Month
# -----------------------------
st.subheader("Earthquakes by Month")

monthly_data = (
    filtered_df.groupby("month")
    .size()
    .reset_index(name="Earthquake Count")
)

st.bar_chart(
    monthly_data.set_index("month")
)

# -----------------------------
# Magnitude Distribution
# -----------------------------
st.subheader("Magnitude Distribution")

magnitude_data = (
    filtered_df["mag"]
    .round(1)
    .value_counts()
    .sort_index()
)

st.bar_chart(magnitude_data)

# -----------------------------
# Depth Category
# -----------------------------
st.subheader("Earthquakes by Depth Category")

depth_data = filtered_df["depth_category"].value_counts()

st.bar_chart(depth_data)

# -----------------------------
# Magnitude Type
# -----------------------------
st.subheader("Earthquakes by Magnitude Type")

mag_type_data = filtered_df["magType"].value_counts()

st.bar_chart(mag_type_data)

# -----------------------------
# Alert Level
# -----------------------------
st.subheader("Earthquakes by Alert Level")

alert_data = (
    filtered_df["alert"]
    .fillna("No Alert")
    .value_counts()
)

st.bar_chart(alert_data)

# -----------------------------
# Tsunami Events
# -----------------------------
st.subheader("Tsunami Events by Year")

tsunami_data = (
    df[df["tsunami"] == 1]
    .groupby("year")
    .size()
    .reset_index(name="Tsunami Count")
)

st.bar_chart(
    tsunami_data.set_index("year")
)

# -----------------------------
# Earthquake Status
# -----------------------------
st.subheader("Earthquakes by Status")

status_data = filtered_df["status"].value_counts()

st.bar_chart(status_data)

# -----------------------------
# Geographic Analysis
# -----------------------------
st.subheader("Earthquake Locations")

map_data = filtered_df[
    ["latitude", "longitude"]
].dropna()

if not map_data.empty:
    st.map(map_data)
else:
    st.write("No location data available for the selected filters.")

# -----------------------------
# Data Table
# -----------------------------
st.subheader("Filtered Earthquake Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

# -----------------------------
# Key Insights
# -----------------------------
st.subheader("Key Insights")

if not filtered_df.empty:

    highest_mag = filtered_df.loc[
        filtered_df["mag"].idxmax()
    ]

    deepest = filtered_df.loc[
        filtered_df["depth_km"].idxmax()
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Highest Magnitude",
        round(highest_mag["mag"], 2)
    )

    col2.metric(
        "Deepest Earthquake (km)",
        round(deepest["depth_km"], 2)
    )

    col3.metric(
        "Filtered Earthquakes",
        f"{len(filtered_df):,}"
    )

else:
    st.warning("No earthquakes match the selected filters.")