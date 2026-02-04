import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# ================= CONFIG =================
SHEET_NAME = "CROWN_SPAN_DATA"

# ================= GOOGLE AUTH =================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"],
    scope
)

client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# ================= UI =================
st.set_page_config(
    page_title="CROWN•SPAN Remote Monitoring",
    layout="wide"
)

st.title("🌉 CROWN•SPAN | Remote Monitoring")

# ================= READ DATA =================
data = sheet.get_all_records()
df = pd.DataFrame(data)

if df.empty:
    st.warning("No data available yet")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])

span = st.sidebar.selectbox("Select Span", [1, 2])
df = df[df["span"] == span]

latest = df.iloc[-1]

# ================= LIVE VALUES =================
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ax", f"{latest.ax:.2f}")
c2.metric("Ay", f"{latest.ay:.2f}")
c3.metric("Az", f"{latest.az:.2f}")
c4.metric("Flex (%)", f"{latest.flex:.1f}")

c5, c6, c7, c8 = st.columns(4)
c5.metric("Gx", f"{latest.gx:.2f}")
c6.metric("Gy", f"{latest.gy:.2f}")
c7.metric("Gz", f"{latest.gz:.2f}")
c8.metric("Humidity (%)", f"{latest.humidity:.1f}")

st.divider()

st.subheader("Acceleration")
st.line_chart(df[["ax", "ay", "az"]])

st.subheader("Gyroscope")
st.line_chart(df[["gx", "gy", "gz"]])

st.subheader("Flex & Humidity")
st.line_chart(df[["flex", "humidity"]])

with st.expander("Raw Data"):
    st.dataframe(df, use_container_width=True)
