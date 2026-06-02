import requests
import pandas as pd

# API Key
API_KEY = "daa329f1788d034843db5e63df7e1925"

# City
city = "Berlin"

# API URL
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# Get weather data
response = requests.get(url)
data = response.json()

# Check API response
if "main" in data:

    weather_data = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "cloud_coverage": data["clouds"]["all"],
        "wind_speed": data["wind"]["speed"]
    }

    df = pd.DataFrame([weather_data])

    # Save CSV
    df.to_csv("live_weather_data.csv", index=False)

    print("Weather data saved successfully!")
    print(df)

else:
    print("API Error:", data)