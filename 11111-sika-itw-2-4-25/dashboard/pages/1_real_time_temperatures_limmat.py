from enum import Enum

import pandas as pd
import pydeck as pdk
import requests
import streamlit as st


def get_real_time_data(code, selected_station):
    print("Code : ", code)
    st.subheader(f"📈 Latest Measurements at {selected_station}")
    url = f"https://api.existenz.ch/apiv1/hydro/latest?locations={code}&parameters=temperature,flow&app=WhenToBootle&version=0.0.1"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.DataFrame(response.json().get("payload", []))
            if df.empty:
                st.warning("No real-time data available.")
                return

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            df = df.sort_values("timestamp")

            col1, col2 = st.columns(2)
            temp = df[df["par"] == "temperature"]
            flow = df[df["par"] == "flow"]

            if not temp.empty:
                col1.metric("Water Temperature", f"{temp['val'].iloc[-1]:.2f} °C",
                            help=f"As of {temp['timestamp'].dt.strftime('%Y-%m-%d %H:%M').iloc[-1]}")
            else:
                col1.metric("Water Temperature", "No data available",
                            help="No temperature data available.")
            if not flow.empty:
                col2.metric("Water Flow", f"{flow['val'].iloc[-1]:.2f} m³/s",
                            help=f"As of {flow['timestamp'].dt.strftime('%Y-%m-%d %H:%M').iloc[-1]}")

            with st.expander("Raw API Data"):
                st.dataframe(df[["timestamp", "par", "val"]])
        else:
            st.error(f"API error: {response.status_code}")
    except Exception as e:
        st.error(f"API request failed: {e}")


def get_date_range_data(code, selected_station):
    st.subheader(f"📊 Historical Data for {selected_station} (Last 30 Days)")
    url = f"https://api.existenz.ch/apiv1/hydro/daterange?locations={code}&parameters=temperature,flow&startdate=-30 days&enddate=now&app=my.app.ch&version=1.0.42"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.DataFrame(response.json().get("payload", []))
            if df.empty:
                st.warning("No historical data available.")
                return

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            df["date"] = df["timestamp"].dt.date

            temp_df = df[df["par"] == "temperature"].groupby("date")[
                "val"].mean()
            flow_df = df[df["par"] == "flow"].groupby("date")["val"].mean()

            col1, col2 = st.columns(2)

            with col1:
                st.write("🌡️ Average Temperature °C")
                st.line_chart(temp_df)

            with col2:
                st.write("💧 Average Flow m³/s")
                st.line_chart(flow_df)

            with st.expander("Raw daily averages"):
                daily = df.groupby(["date", "par"])["val"].mean().unstack()
                st.dataframe(daily)

        else:
            st.error(f"API error: {response.status_code}")
    except Exception as e:
        st.error(f"API request failed: {e}")


@st.cache_data(ttl=3600)
def fetch_station_metadata():
    url = "https://api.existenz.ch/apiv1/hydro/locations?app=my.app.ch&version=1.0.42"
    response = requests.get(url)
    payload = response.json().get("payload", [])
    if not payload:
        st.error("No station metadata available.")
        raise ValueError("No station metadata available.")
    else:
        result = []
        for station in payload:
            current_station = payload[station]['details']
            print("Current : ", current_station)
            if "water-body-name" in current_station:
                if "limmat" in current_station["water-body-name"].lower():
                    result.append({
                        "id": current_station["id"],
                        "name": current_station["name"],
                        "river": current_station["water-body-name"],
                        "lat": current_station["lat"],
                        "lon": current_station["lon"],
                        "historical": current_station.get("historical"),
                        "realtime": current_station.get("realtime")
                    })
        return pd.DataFrame(result)


def main():
    st.title("🏞️ Swimming in the Limmat — Real-Time Water Station Data")

    df = fetch_station_metadata()
    df = df[df["lat"].notna() & df["lon"].notna()].copy()

    df.rename(columns={"lat": "latitude", "lon": "longitude"}, inplace=True)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[longitude, latitude]",
        get_fill_color="[200, 30, 0, 160]",
        get_radius=150,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom=10.5
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{name} ({river})"}
    ))

    selected = st.selectbox("Select a real-time station", df["name"])
    station_code = df[df["name"] == selected]["id"].values[0]

    get_real_time_data(station_code, selected)
    get_date_range_data(station_code, selected)


if __name__ == "__main__":
    main()
