import streamlit as st

st.set_page_config(page_title="Limmat Swim Watch",
                   page_icon="💧", layout="centered")

st.title("🏊‍♀️ Limmat Swim Watch")
st.markdown("""
Welcome! This dashboard helps you decide **when and where to jump into the Limmat** — or when maybe to stay on land.  
We bring together **real-time data**, **historical trends**, and **water quality insights** from the city of Zurich.

---

### 📍 Explore the Limmat from four perspectives:
""")

st.markdown("""
#### 🌡️ [Real-Time Data](./Real-Time_Data)
Check the latest temperature and water flow from key stations — ideal for spontaneous swims.

#### 📈 [Historical Temperatures](./Historical_Temperatures)
Browse water temperature trends from 2020 to today. Wondering how this April compares to last year?

#### 🧪 [Reservoir Water Quality](./Reservoir_Water_Quality)
Zoom out and explore biological and chemical indicators from Zürich's reservoirs — across different zones.

#### 🚰 [Water Treatment Plants](./Water_Treatment_Plants)
See what's happening upstream. Real-time values from Moos, Lengg, and Hardhof treatment stations.

---

💡 *Tip: The Limmat is most swim-friendly when the temperature is above 20°C and flow is below 100 m³/s.*
""")

st.divider()
# st.image("img/boeoetle.avif",
#          caption="The Limmat calling your name...", use_column_width=True)

st.caption(
    "Created with 💙 by Alexis — powered by Existenz API and Zürich Open Data.")
