import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st


@st.cache_data
def load_historical_data():
    temp_dfs, flow_dfs = [], []
    years = range(2020, 2025)

    for year in years:
        temp_path = os.path.join("data", "limmat_temperatures", f"{year}.csv")
        flow_path = os.path.join("data", "limmat_flows", f"{year}.csv")

        if os.path.exists(temp_path) and os.path.exists(flow_path):
            t = pd.read_csv(temp_path, parse_dates=["Date"])
            f = pd.read_csv(flow_path, parse_dates=["Date"])

            df = pd.merge(t, f, on="Date", suffixes=("_temp", "_flow"))
            df["Month"] = df["Date"].dt.month
            df["SwimmingPossible"] = (df["Temperature (°C)"] > 20) & (
                df["Flow (m³/s)"] < 100)
            temp_dfs.append(df)

    full_df = pd.concat(temp_dfs)
    return full_df


def display_monthly_summary(df):
    summary = df.groupby("Month")["SwimmingPossible"].mean().reset_index()
    summary["Swimming %"] = (summary["SwimmingPossible"] * 100).round(1)

    summary["MonthName"] = summary["Month"].apply(
        lambda m: pd.to_datetime(f"2023-{m:02d}-01").strftime("%B"))

    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    summary["MonthName"] = pd.Categorical(
        summary["MonthName"], categories=month_order, ordered=True)

    summary = summary.sort_values("MonthName")

    summary_display = summary[["MonthName",
                               "Swimming %"]].set_index("MonthName")
    st.subheader("Historical swimming possibility (%) by month")
    with st.expander("View Data", expanded=False):
        st.write(
            "This table shows the percentage of swimming-friendly days for each month.")
        st.dataframe(summary_display)

    # Plot using Altair for correct order
    import altair as alt
    chart = alt.Chart(summary).mark_bar().encode(
        x=alt.X("MonthName:N", sort=month_order, title="Month"),
        y=alt.Y("Swimming %:Q", title="Chance of Swimming Days"),
        tooltip=["Swimming %"]
    ).properties(width=700, height=400)

    st.altair_chart(chart, use_container_width=True)


def display_first_swimmable_day(df):
    st.subheader("Earliest historical swimming day")

    first = df[df["SwimmingPossible"]].sort_values("Date").head(1)
    if not first.empty:
        date = first["Date"].iloc[0].strftime("%d %B %Y")
        temp = first["Temperature (°C)"].iloc[0]
        flow = first["Flow (m³/s)"].iloc[0]
        st.info(
            f"The earliest recorded swimming-friendly day was **{date}** with a temperature of **{temp:.1f}°C** and flow of **{flow:.1f} m³/s**.")
    else:
        st.warning("No swim-friendly day found in the historical data.")


def get_real_time_temperature_and_flow(code="2160"):
    url = f"https://api.existenz.ch/apiv1/hydro/latest?locations={code}&parameters=temperature,flow&app=WhenToBootle&version=0.0.1"

    try:
        response = requests.get(url)
        data = response.json()["payload"]
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        print("DF : ", df)

        temp = df[df["par"] == "temperature"]["val"].iloc[-1]
        flow = df[df["par"] == "flow"]["val"].iloc[-1]
        return temp, flow
    except Exception as e:
        st.error(f"Could not fetch real-time data: {e}")
        return None, None


def display_today_message(temp, flow):
    st.subheader("🏊 Can You Swim Today?")
    if temp is None or flow is None:
        st.warning("Real-time data not available.")
    elif temp > 20 and flow < 100:
        st.success(f"Yes! Water is {temp:.1f}°C and flow is {flow:.1f} m³/s.")
    else:
        st.error(
            f"Not ideal: Water is {temp:.1f}°C and flow is {flow:.1f} m³/s.")


def main():
    st.title("Swimming Possibilities")

    df = load_historical_data()
    display_monthly_summary(df)

    st.divider()

    temp, flow = get_real_time_temperature_and_flow(2243)
    display_today_message(temp, flow)
    display_first_swimmable_day(df)


if __name__ == "__main__":
    main()
