import os
from functools import cache

import altair as alt
import pandas as pd
import streamlit as st


@cache
def load_yearly_data():
    years = range(2020, 2025)
    dfs = []
    for year in years:
        path = os.path.join("data", "limmat_flows", f"{year}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Year"] = year
            dfs.append(df)
        else:
            st.warning(f"Missing data for {year}")
    return dfs


def plot_facet_line_by_year():
    st.subheader("Daily flows (2020 - 2024)")

    dfs = load_yearly_data()
    if not dfs:
        st.error("No data found.")
        return

    all_data = pd.concat(dfs)
    all_data["DayOfYear"] = all_data["Date"].dt.dayofyear

    chart = alt.Chart(all_data).mark_line().encode(
        x=alt.X("DayOfYear:Q", title="Day of Year"),
        y=alt.Y("Flow (m³/s):Q", title="Flow (m³/s)"),
        facet=alt.Facet("Year:N", columns=2, title=None),
        tooltip=["Date", "Flow (m³/s)"]
    ).properties(
        width=350,
        height=150
    ).configure_facet(
        spacing=10
    ).configure_view(
        stroke=None
    )

    left, center, right = st.columns([1, 20, 1])
    with center:
        st.altair_chart(chart, use_container_width=False)


def plot_monthly_avg_altair():
    st.subheader("Monthly average flows")

    dfs = load_yearly_data()
    if not dfs:
        st.error("No data found.")
        return

    data_list = []
    for df in dfs:
        year = df["Year"].iloc[0]
        df["Month"] = df["Date"].dt.month
        monthly_avg = df.groupby(
            "Month")["Flow (m³/s)"].mean().reset_index()
        monthly_avg["Year"] = year
        data_list.append(monthly_avg)

    data = pd.concat(data_list)
    data["Month"] = data["Month"].apply(
        lambda m: pd.to_datetime(f"2023-{m:02d}-01").strftime("%b"))

    chart = alt.Chart(data).mark_line(point=True).encode(
        x=alt.X("Month:N", sort=list(pd.date_range(
            "2023-01-01", periods=12, freq='M').strftime("%b"))),
        y=alt.Y("Flow (m³/s):Q", title="Avg Flow (m³/s)"),
        color=alt.Color("Year:N", scale=alt.Scale(scheme="viridis")),
        tooltip=["Year", "Month", "Flow (m³/s)"]
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)


def plot_overall_monthly_average():
    st.subheader("Average flow per month")

    dfs = load_yearly_data()
    if not dfs:
        st.error("No data found.")
        return

    all_data = pd.concat(dfs)
    all_data["Month"] = all_data["Date"].dt.month
    monthly_avg = all_data.groupby("Month")["Flow (m³/s)"].mean().reset_index()
    monthly_avg["MonthName"] = monthly_avg["Month"].apply(
        lambda m: pd.to_datetime(f"2023-{m:02d}-01").strftime("%B"))

    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    monthly_avg["MonthName"] = pd.Categorical(
        monthly_avg["MonthName"], categories=month_order, ordered=True)
    monthly_avg = monthly_avg.sort_values("MonthName")

    chart = alt.Chart(monthly_avg).mark_bar().encode(
        x=alt.X("MonthName:N", sort=month_order, title="Month"),
        y=alt.Y("Flow (m³/s):Q", title="Average Flow (m³/s)"),
        tooltip=["MonthName", "Flow (m³/s)"]
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)


def plot_yearly_boxplots():
    st.subheader("Flow distribution by year")

    dfs = load_yearly_data()
    if not dfs:
        st.error("No data found.")
        return

    data = pd.concat(dfs)

    box_fill_color = '#1f77b4'
    box_border_color = 'black'
    median_line_color = 'red'

    chart = alt.Chart(data).mark_boxplot(
        size=40,
        color=box_fill_color,
        box=alt.MarkConfig(stroke=box_border_color),
        median=alt.MarkConfig(color=median_line_color)
    ).encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Flow (m³/s):Q", title="Flow (m³/s)")
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)


def main():
    st.title("Historical Limmat water flows (2020–2024)")

    st.markdown(
        "Overview of the flows in the Limmat river from 2020 to 2024. "
    )

    plot_facet_line_by_year()
    plot_monthly_avg_altair()
    plot_overall_monthly_average()
    plot_yearly_boxplots()

    st.markdown(
        """
        <div style="text-align: center;">
            Data provided by the <a href="https://www.hydrodaten.admin.ch/de/seen-und-fluesse/stationen-und-daten/2099" target="_blank">BAFU</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
