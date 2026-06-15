import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Live Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Live Weather Dashboard")
st.write("Get the latest weather details for any city.")

# Read API key from Streamlit Secrets
API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# City input
city = st.text_input("Enter City Name", value="Bangalore")

if st.button("Get Weather"):

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:

        weather_data = {
            "City": city,
            "Temperature (°C)": data["main"]["temp"],
            "Feels Like (°C)": data["main"]["feels_like"],
            "Humidity (%)": data["main"]["humidity"],
            "Pressure (hPa)": data["main"]["pressure"],
            "Weather": data["weather"][0]["description"].title(),
            "Wind Speed (m/s)": data["wind"]["speed"],
            "Last Updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        st.success(f"Weather data retrieved successfully for {city}!")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🌡 Temperature", f"{weather_data['Temperature (°C)']} °C")

        with col2:
            st.metric("💧 Humidity", f"{weather_data['Humidity (%)']} %")

        with col3:
            st.metric("💨 Wind Speed", f"{weather_data['Wind Speed (m/s)']} m/s")

        st.subheader("Detailed Weather Report")
        st.write(weather_data)

        df = pd.DataFrame([weather_data])

        st.subheader("Weather Data Table")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Weather Report (CSV)",
            data=csv,
            file_name=f"{city.lower()}_weather_report.csv",
            mime="text/csv"
        )

    else:
        error_message = data.get("message", "Unable to fetch weather data.")
        st.error(f"Error: {error_message}")
