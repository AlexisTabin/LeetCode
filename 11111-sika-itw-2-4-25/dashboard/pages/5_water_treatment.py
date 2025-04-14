import os

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title="Water Treatment Data")

st.title("Water treatment data")

file_path = os.path.join("data", "water_treatment_data_geocoded.csv")
if not os.path.exists(file_path):
    st.error("Geolocated water treatment dataset not found.")
else:
    df = pd.read_csv(file_path)
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df = df.dropna(subset=["Datum", "Messwert", "lat", "lon"])

    valid_combinations = df.groupby(["Standort", "Parameter"])[
        "Messwert"].count()
    valid_combinations = valid_combinations[valid_combinations > 0].reset_index(
    )

    st.sidebar.header("Filter")

    valid_locations = valid_combinations["Standort"].unique()
    selected_location = st.sidebar.selectbox(
        "Location", sorted(valid_locations))

    filtered_params = valid_combinations[
        valid_combinations["Standort"] == selected_location
    ]["Parameter"].unique()
    selected_param = st.sidebar.selectbox("Parameter", sorted(filtered_params))

    st.subheader("Water treatment locations map")
    map_df = df[["Standort", "lat", "lon"]].drop_duplicates()
    map_df["color"] = map_df["Standort"].apply(
        lambda x: [255, 0, 0] if x == selected_location else [0, 100, 255]
    )
    map_df["radius"] = map_df["Standort"].apply(
        lambda x: 200 if x == selected_location else 100
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

    filtered_df = df[
        (df["Standort"] == selected_location) & (
            df["Parameter"] == selected_param)
    ]

    if filtered_df.empty:
        st.warning("No data found for selected filters.")
    else:
        st.write(f"### {selected_param} at {selected_location}")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.scatter(filtered_df["Datum"], filtered_df["Messwert"], s=10)
        ax.set_xlabel("Date")
        ax.set_ylabel(f"{selected_param} ({filtered_df['Einheit'].iloc[0]})")
        ax.set_title(f"{selected_param} over Time")
        ax.grid(True)
        st.pyplot(fig)
        st.dataframe(filtered_df)
