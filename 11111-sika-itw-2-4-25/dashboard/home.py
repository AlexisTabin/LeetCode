import streamlit as st

st.set_page_config(page_title="Limmat Swim Watch",
                   page_icon="💧", layout="wide", initial_sidebar_state="collapsed")

st.title("When to Böötle on the Limmat? 🚢")
st.markdown("""
I built this dashboard to determine when we can finally go Böötle on the Limmat.\n
The different pages will showcase some data insights that will help you decide **when is the right time to jump into the Limmat**, or when maybe to stay on land.  
The data insights bring together **real-time data**, **historical trends**, and **water quality insights** from the city of Zurich.

---

### Explore the Limmat from four perspectives:
""")

st.markdown("""
#### Real-Time Data
Check the latest temperature and water flow from key stations.
            
#### Historical Flows & Temperatures
Dive into daily flow and temperature data from 2020 to 2024. Wondering how this April compares to last year?

#### Reservoir Water Quality
Zoom out and explore biological and chemical indicators from Zürich's reservoirs.

#### Water Treatment Plants
See what's happening upstream. Latest values from Moos, Lengg, and Hardhof treatment stations.

---

💡 *LifeProTip: The Limmat is most swim-friendly when the temperature is above 20°C and flow is below 100 m³/s.*
""")

st.divider()
# st.image("img/boeoetle.avif",
#          caption="The Limmat calling your name...", use_column_width=True)

st.caption(
    "Created with 💙 by Alexis — powered by Existenz API and Zürich Open Data.")
