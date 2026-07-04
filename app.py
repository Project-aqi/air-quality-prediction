import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Page config
st.set_page_config(
    page_title="Air Quality Predictor",
    page_icon="🌍",
    layout="wide"
)

# Title
st.title("🌍 Air Quality Index Predictor")
st.subheader("New Taipei City, Taiwan")
st.write("Enter pollution readings below to predict AQI")
st.write("---")

# Load model
model = joblib.load('best_model.pkl')

# Two columns layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Date & Time")
    month       = st.slider("Month",        1,  12,  6)
    day         = st.slider("Day",          1,  31, 15)
    hour        = st.slider("Hour",         0,  23, 12)
    day_of_week = st.slider("Day of Week",  0,   6,  3)
    is_weekend  = st.selectbox("Is Weekend?", [0, 1])

    st.subheader("📍 Location")
    longitude = st.number_input("Longitude", value=121.48)
    latitude  = st.number_input("Latitude",  value=25.07)
    status    = st.selectbox("Status", [0, 1, 2])

with col2:
    st.subheader("🏭 Pollution Readings")
    so2      = st.slider("SO2",        0.0, 100.0, 5.0)
    co       = st.slider("CO",         0.0,  10.0, 0.5)
    o3       = st.slider("O3",         0.0, 200.0, 30.0)
    o3_8hr   = st.slider("O3 8hr",     0.0, 200.0, 25.0)
    pm10     = st.slider("PM10",       0.0, 500.0, 50.0)
    pm25     = st.slider("PM2.5",      0.0, 300.0, 20.0)
    no2      = st.slider("NO2",        0.0, 200.0, 15.0)
    nox      = st.slider("NOx",        0.0, 200.0, 20.0)
    no       = st.slider("NO",         0.0, 100.0,  5.0)
    windspeed= st.slider("Windspeed",  0.0,  20.0,  2.0)
    winddirec= st.slider("Wind Dir",   0.0, 360.0,180.0)
    co_8hr   = st.slider("CO 8hr",     0.0,  10.0,  0.5)
    pm25_avg = st.slider("PM2.5 Avg",  0.0, 300.0, 20.0)
    pm10_avg = st.slider("PM10 Avg",   0.0, 500.0, 50.0)
    so2_avg  = st.slider("SO2 Avg",    0.0, 100.0,  5.0)

st.write("---")

# Predict button
if st.button("🔍 Predict AQI", use_container_width=True):
    input_data = pd.DataFrame([{
        'date'        : 0,
        'status'      : status,
        'so2'         : so2,
        'co'          : co,
        'o3'          : o3,
        'o3_8hr'      : o3_8hr,
        'pm10'        : pm10,
        'pm2.5'       : pm25,
        'no2'         : no2,
        'nox'         : nox,
        'no'          : no,
        'windspeed'   : windspeed,
        'winddirec'   : winddirec,
        'co_8hr'      : co_8hr,
        'pm2.5_avg'   : pm25_avg,
        'pm10_avg'    : pm10_avg,
        'so2_avg'     : so2_avg,
        'longitude'   : longitude,
        'latitude'    : latitude,
        'hour'        : hour,
        'day'         : day,
        'month'       : month,
        'day_of_week' : day_of_week,
        'is_weekend'  : is_weekend
    }])

    prediction = model.predict(input_data)[0]

    st.write("---")
    col3, col4 = st.columns(2)

    with col3:
        st.metric("Predicted AQI", round(prediction, 2))

    with col4:
        if prediction <= 50:
            st.success("🟢 Good — Air quality is satisfactory")
        elif prediction <= 100:
            st.warning("🟡 Moderate — Acceptable air quality")
        elif prediction <= 150:
            st.error("🟠 Unhealthy for Sensitive Groups")
        else:
            st.error("🔴 Unhealthy — Everyone may be affected")

st.write("---")
st.caption("Built with Machine Learning | New Taipei City Air Quality Data 2024")
