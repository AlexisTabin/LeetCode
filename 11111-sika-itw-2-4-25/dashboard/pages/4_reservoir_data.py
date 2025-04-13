import os

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Reservoir Data")

st.title("🏞️ Reservoir Data")

# Load geocoded dataset
file_path = os.path.join("data", "reservoir_data_geocoded.csv")
if not os.path.exists(file_path):
    st.error("Geocoded reservoir dataset not found.")
    st.stop()

# Load and clean data
df = pd.read_csv(file_path)
df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
df = df.dropna(subset=["Datum", "Messwert", "lat", "lon"])

# Sidebar filter
st.sidebar.header("Filter")
valid_zones = df["Zone"].dropna().unique()
selected_zone = st.sidebar.selectbox("Zone", sorted(valid_zones))

# Filter parameters based on selected zone
zone_df = df[df["Zone"] == selected_zone]
valid_params = zone_df["Parameter"].dropna().unique()
selected_param = st.sidebar.selectbox("Parameter", sorted(valid_params))

# Show map
st.subheader("🗺️ Reservoir Locations Map")
map_df = df[["Zone", "Standort", "lat", "lon"]].drop_duplicates()
map_df["color"] = map_df["Zone"].apply(
    lambda z: [255, 0, 0] if z == selected_zone else [0, 100, 255]
)
map_df["radius"] = map_df["Zone"].apply(
    lambda z: 200 if z == selected_zone else 100
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position="[lon, lat]",
    get_radius="radius",
    get_fill_color="color",
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=map_df["lat"].mean(),
    longitude=map_df["lon"].mean(),
    zoom=11
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{Standort}"}
))

# Plot selected parameter
filtered_df = zone_df[zone_df["Parameter"] == selected_param]

if filtered_df.empty:
    st.warning("No data found for selected filters.")
else:
    st.write(f"### {selected_param} in {selected_zone}")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(filtered_df["Datum"], filtered_df["Messwert"], s=10)
    ax.set_xlabel("Date")
    ax.set_ylabel(f"{selected_param} ({filtered_df['Einheit'].iloc[0]})")
    ax.set_title(f"{selected_param} over Time")
    ax.grid(True)
    st.pyplot(fig)
    st.dataframe(filtered_df)

# Correlation Matrix for Limmatzone
if selected_zone == "Limmatzone":
    st.write("## 📊 Correlation Matrix for Limmatzone")

    limmat_df = df[df["Zone"] == "Limmatzone"]

    pivot_df = limmat_df.pivot_table(
        index="Datum",
        columns="Parameter",
        values="Messwert",
        aggfunc="mean"
    )

    st.write("Shape of pivoted data (dates x parameters):", pivot_df.shape)

    if pivot_df.shape[1] < 2:
        st.warning(
            "Not enough parameters with overlapping dates to compute correlations.")
    else:
        corr_matrix = pivot_df.corr(method="pearson", min_periods=10)
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Parameter Correlation Matrix in Limmatzone")
        st.pyplot(fig)
        st.markdown("""
        **Variable descriptions:**
        - **Wassertemperatur**: Water temperature, a key indicator for recreational suitability and microbial growth.
        - **iATP (intrazelluläres Adenosintriphosphat)**: Measures biological activity (living biomass) in the water.
        - **Intakte Zellen**: Count of intact microbial cells, used to assess microbiological quality.
        - **Gesamte Zellzahl**: Total cell count (including live and damaged), indicating overall microbial load.
        """)
        st.markdown("""
        ### Correlation matrix interpretation
        - No strong correlation: The four parameters represent different biological aspects (complements).\n
        - This makes sense for multi-dimensional water quality monitoring.
        """)
        st.dataframe(corr_matrix)
