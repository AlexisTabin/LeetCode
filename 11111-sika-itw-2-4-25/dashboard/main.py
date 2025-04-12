import os
from enum import Enum

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st
from pyproj import Transformer


class DataType(Enum):
    REAL_TIME_DATA = "Real-Time data"
    HISTORICAL_DATA = "Historical data"
    NO_DATA = "No data available"


class Colors(Enum):
    GREEN = [0, 200, 0, 160]      # 🟩 green
    BLUE = [0, 100, 255, 160]     # 🔵 blue
    GRAY = [128, 128, 128, 160]   # ⬜ gray
    BLACK = [0, 0, 0, 160]        # fallback: black


def get_station_color(station_type_str):
    if station_type_str == DataType.REAL_TIME_DATA.value:
        return Colors.GREEN.value
    elif station_type_str == DataType.HISTORICAL_DATA.value:
        return Colors.BLUE.value
    elif station_type_str == DataType.NO_DATA.value:
        return Colors.GRAY.value
    else:
        return Colors.BLACK.value


def type_of_station(code):
    if isinstance(code, str) and code.isdigit():
        if int(code) == 2209:
            return DataType.NO_DATA.value
        return DataType.REAL_TIME_DATA.value
    elif code == 'ZH 578':
        return DataType.HISTORICAL_DATA.value
    else:
        return DataType.NO_DATA.value


def get_real_time_data(code, selected_station):
    st.subheader(f"Latest Measurements at {selected_station}")
    # https://api.existenz.ch/
    api_url = f"https://api.existenz.ch/apiv1/hydro/latest?locations={code}&parameters=temperature,flow&app=my.app.ch&version=1.0.42"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            result = response.json()
            payload = result.get("payload", [])
            if payload:
                df_api = pd.DataFrame(payload)
                df_api["timestamp"] = pd.to_datetime(
                    df_api["timestamp"], unit="s")
                df_api = df_api.sort_values("timestamp")

                col1, col2 = st.columns(2)
                latest_temp = df_api[df_api["par"] == "temperature"]
                latest_flow = df_api[df_api["par"] == "flow"]

                if not latest_temp.empty:
                    temp_val = latest_temp["val"].values[-1]
                    temp_time = latest_temp["timestamp"].dt.strftime(
                        "%Y-%m-%d %H:%M").values[-1]
                    col1.metric(label="Water Temperature",
                                value=f"{temp_val:.2f} °C", help=f"As of {temp_time}")
                else:
                    col1.warning("No temperature data available.")

                if not latest_flow.empty:
                    flow_val = latest_flow["val"].values[-1]
                    flow_time = latest_flow["timestamp"].dt.strftime(
                        "%Y-%m-%d %H:%M").values[-1]
                    col2.metric(
                        label="Water Flow", value=f"{flow_val:.2f} m³/s", help=f"As of {flow_time}")
                else:
                    col2.warning("No flow data available.")

                with st.expander("See raw API data"):
                    st.dataframe(df_api[["timestamp", "par", "val"]])
            else:
                st.warning("No data returned for this station.")
        else:
            st.error(
                f"API request failed with status code {response.status_code}")
    except Exception as e:
        st.error(f"Failed to fetch data from Existenz API: {e}")


def load_and_plot_limmat_temperature():
    st.subheader("📈 Limmat Water Temperature (2020–2025)")

    years = range(2020, 2026)
    dfs = []

    for year in years:
        file_path = os.path.join("data", "limmat_temperatures", f"{year}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["Date"] = pd.to_datetime(df["Date"])
            dfs.append(df)
        else:
            st.warning(f"Missing data for year {year}.")

    if not dfs:
        st.error("No temperature data found.")
        return

    full_df = pd.concat(dfs).sort_values("Date")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(full_df["Date"], full_df["Temperature (°C)"],
            color="blue", linewidth=1.5)
    ax.set_title(
        "Water Temperature in the Limmat River (2020–2025)", fontsize=14)
    ax.set_ylabel("Temperature (°C)")
    ax.set_xlabel("Date")
    ax.grid(True)

    st.pyplot(fig)


def load_and_plot_limmat_mean_temperature():
    st.subheader("📈 Average Monthly Water Temperature (2020–2025)")

    years = range(2020, 2026)
    monthly_avg_by_year = {}

    for year in years:
        file_path = os.path.join("data", "limmat_temperatures", f"{year}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Month"] = df["Date"].dt.month
            monthly_avg = df.groupby("Month")["Temperature (°C)"].mean()
            monthly_avg_by_year[year] = monthly_avg
        else:
            st.warning(f"Missing data for year {year}.")

    if not monthly_avg_by_year:
        st.error("No temperature data found.")
        return

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 5))
    month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for year, temps in monthly_avg_by_year.items():
        ax.plot(temps.index, temps.values, label=str(year), linewidth=2)

    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(month_labels)
    ax.set_ylabel("Avg. Temperature (°C)")
    ax.set_title(
        "Average Monthly Water Temperature in the Limmat River (2020–2025)")
    ax.legend(title="Year")
    ax.grid(True)

    st.pyplot(fig)


def load_and_plot_daily_limmat_temperature():
    st.subheader("📅 Daily Water Temperature (2020–2025)")

    years = range(2020, 2026)
    for year in years:
        file_path = os.path.join("data", "limmat_temperatures", f"{year}.csv")
        if not os.path.exists(file_path):
            st.warning(f"Missing data for year {year}.")
            continue

        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"])

        # Plot raw data
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df["Date"], df["Temperature (°C)"],
                label=f"{year}", color="steelblue")
        ax.set_title(f"Limmat Water Temperature in {year}")
        ax.set_ylabel("Temperature (°C)")
        ax.set_xlabel("Date")
        ax.grid(True)

        st.pyplot(fig)


if __name__ == "__main__":
    transformer = Transformer.from_crs(
        "EPSG:2056", "EPSG:4326", always_xy=True)

    directory = os.getcwd()
    data_path = os.path.join(
        directory, "data", "WB_HYDROMETRISCHE_STATIONEN_P.csv")
    df = pd.read_csv(data_path, sep=",", encoding="utf-8")

    stations = df[df["X_LV95"].notna() & df["Y_LV95"].notna()].copy()
    stations["is_limmat"] = stations["NAME"].str.lower(
    ).str.contains("limmat", na=False)

    stations["STATION_TYPE"] = stations["CODE_EINDEUTIG"].apply(
        type_of_station)
    stations["color"] = stations["STATION_TYPE"].apply(get_station_color)

    stations[["lon", "lat"]] = stations.apply(
        lambda row: pd.Series(transformer.transform(row["X_LV95"], row["Y_LV95"])), axis=1
    )

    st.subheader("Sample of Hydrometric Stations")
    st.dataframe(stations[["NAME", "GEWAESSERNAME", "ORGANISATION"]].head(10))

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=stations,
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius=150,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=stations["lat"].mean(),
        longitude=stations["lon"].mean(),
        zoom=12.5,
        pitch=0
    )

    left_col, right_col = st.columns([4, 1])

    with left_col:
        st.subheader("Map of Hydrometric Stations in Zurich")
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{NAME} - {GEWAESSERNAME}"}
        ))

    with right_col:
        st.subheader("Legend")
        st.markdown(f"""
        🟩 **{DataType.REAL_TIME_DATA.value}**  
        🔵 **{DataType.HISTORICAL_DATA.value}**  
        ⬜ **{DataType.NO_DATA.value}**
        """)

    stations = stations[stations["STATION_TYPE"] != DataType.NO_DATA.value]
    selected_station = st.selectbox(
        "Select a station to view current temperature and flow:", stations["NAME"].unique())
    station_row = stations[stations["NAME"] == selected_station].iloc[0]
    code = station_row["CODE_EINDEUTIG"]
    station_type = station_row["STATION_TYPE"]

    if station_type == DataType.REAL_TIME_DATA.value:
        get_real_time_data(code, selected_station)
    elif station_type == DataType.HISTORICAL_DATA.value:
        load_and_plot_limmat_temperature()
        load_and_plot_limmat_mean_temperature()
        load_and_plot_daily_limmat_temperature()
