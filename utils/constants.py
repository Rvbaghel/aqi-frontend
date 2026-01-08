# utils/constants.py

AQI_LEVELS = {
    1: {"label": "Good", "color": "green"},
    2: {"label": "Fair", "color": "lightgreen"},
    3: {"label": "Moderate", "color": "orange"},
    4: {"label": "Poor", "color": "red"},
    5: {"label": "Very Poor", "color": "darkred"}
}

POLLUTANTS = [
    "pm2_5",
    "pm10",
    "co",
    "no2",
    "so2",
    "o3",
    "nh3"
]

CITIES = [
    "Delhi",
    "Mumbai",
    "Ahmedabad",
    "Bengaluru",
    "Kolkata",
    "Chennai"
]
