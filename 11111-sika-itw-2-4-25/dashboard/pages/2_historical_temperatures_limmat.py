import os
from functools import cache

import altair as alt
import pandas as pd
import streamlit as st


@cache
def load_yearly_data():
    years = range(2020, 2026)
    dfs = []
    for year in years:
        path = os.path.join("data", "limmat_temperatures", f"{year}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Year"] = year
            dfs.append(df)
        else:
            st.warning(f"Missing data for {year}")
    return dfs


def plot_facet_line_by_year():
    st.subheader("📈 Daily Temperatures – One Chart per Year")

    dfs = load_yearly_data()
    if not dfs:
        st.error("No data found.")
        return

    all_data = pd.concat(dfs)
    all_data["DayOfYear"] = all_data["Date"].dt.dayofyear

    chart = alt.Chart(all_data).mark_line().encode(
        x=alt.X("DayOfYear:Q", title="Day of Year"),
        y=alt.Y("Temperature (°C):Q", title="Temp (°C)"),
        facet=alt.Facet("Year:N", columns=2, title=None),
        tooltip=["Date", "Temperature (°C)"]
    ).properties(
        width=350,  # Increased width for each facet
        height=150
    ).configure_facet(
        spacing=10  # Adjust spacing between facets
    ).configure_view(
        stroke=None
    )

    # Center the chart using Streamlit's column layout
    # Adjusted column ratios for more width
    left, center, right = st.columns([1, 20, 1])
    with center:
        st.altair_chart(chart, use_container_width=False)


def plot_monthly_avg_altair():
    st.subheader("📊 Monthly Average Temperatures")

    dfs = load_yearly_data()
    if not dfs:
        st.error("No data found.")
        return

    data_list = []
    for df in dfs:
        year = df["Year"].iloc[0]
        df["Month"] = df["Date"].dt.month
        monthly_avg = df.groupby(
            "Month")["Temperature (°C)"].mean().reset_index()
        monthly_avg["Year"] = year
        data_list.append(monthly_avg)

    data = pd.concat(data_list)
    data["Month"] = data["Month"].apply(
        lambda m: pd.to_datetime(f"2023-{m:02d}-01").strftime("%b"))

    chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X("Month:N", sort=list(pd.date_range(
            "2023-01-01", periods=12, freq='M').strftime("%b"))),
        y=alt.Y("Temperature (°C):Q", title="Avg Temperature (°C)"),
        color=alt.Color("Year:N", scale=alt.Scale(scheme="viridis")),
        tooltip=["Year", "Month", "Temperature (°C)"]
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)


def plot_yearly_boxplots():
    st.subheader("📦 Temperature Distribution by Year")

    dfs = load_yearly_data()
    if not dfs:
        st.error("No data found.")
        return

    data = pd.concat(dfs)

    # Define colors
    box_fill_color = '#1f77b4'  # Blue fill for boxes
    box_border_color = 'black'  # Black border for boxes
    median_line_color = 'red'   # Red color for median line

    # Create the box plot
    chart = alt.Chart(data).mark_boxplot(
        size=40,  # Adjust box width
        color=box_fill_color,
        box=alt.MarkConfig(stroke=box_border_color),
        median=alt.MarkConfig(color=median_line_color)
    ).encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Temperature (°C):Q", title="Temperature (°C)")
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)


def main():
    st.title("🌊 Historical Limmat Water Temperatures (2020–2025)")

    st.markdown(
        "Explore temperature trends and distributions across years with aligned comparisons, monthly trends, and boxplots."
    )

    plot_facet_line_by_year()
    plot_monthly_avg_altair()
    plot_yearly_boxplots()


if __name__ == "__main__":
    main()
