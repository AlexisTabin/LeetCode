import os

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title="Reservoir Data")

st.title("🏞️ Reservoir Data")

file_path = os.path.join("data", "reservoir_data_geocoded.csv")
if not os.path.exists(file_path):
    st.error("Geocoded reservoir dataset not found.")
else:
    # Load and clean data
    df = pd.read_csv(file_path)
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df = df.dropna(subset=["Datum", "Messwert", "lat", "lon"])

    # Get valid zone-parameter combinations
    valid_combinations = df.groupby(["Zone", "Parameter"])["Messwert"].count()
    valid_combinations = valid_combinations[valid_combinations > 0].reset_index(
    )

    st.sidebar.header("Filter")

    # Select zone
    valid_zones = valid_combinations["Zone"].dropna().unique()
    selected_zone = st.sidebar.selectbox("Zone", sorted(valid_zones))

    # Filter parameters based on selected zone
    filtered_params = valid_combinations[
        valid_combinations["Zone"] == selected_zone
    ]["Parameter"].unique()
    selected_param = st.sidebar.selectbox("Parameter", sorted(filtered_params))

    # Show map at the top
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

    # Filter main dataframe
    filtered_df = df[
        (df["Zone"] == selected_zone) & (df["Parameter"] == selected_param)
    ]

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
