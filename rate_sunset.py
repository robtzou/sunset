import requests
from datetime import datetime

def compute_sunset_score(data):
    cc = data['cloudcover']
    rh = data['relativehumidity_2m']
    ws = data['windspeed_10m']
    pr = data['precipitation']

    score = 0

    if 30 <= cc <= 70:
        score += 40
    elif 20 <= cc < 30 or 70 < cc <= 80:
        score += 20
    elif 10 <= cc < 20 or 80 < cc <= 90:
        score += 10

    if rh < 40:
        score += 25
    elif 40 <= rh < 60:
        score += 15
    elif 60 <= rh < 75:
        score += 5

    if 5 <= ws <= 20:
        score += 20
    elif 2 <= ws < 5 or 20 < ws <= 30:
        score += 10

    if pr == 0:
        score += 15
    elif pr < 1:
        score += 5

    return min(score, 100)

# Location
latitude = 38.99
longitude = -76.94

# API request
params = {
    'latitude': latitude,
    'longitude': longitude,
    'hourly': 'cloudcover,windspeed_10m,relativehumidity_2m,precipitation',
    'daily': 'sunset',
    'timezone': 'auto'
}

response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)

if response.status_code == 200:
    data = response.json()

    # Get today's sunset time (e.g. "2025-06-10T20:31")
    sunset_time_str = data['daily']['sunset'][0]
    sunset_hour = datetime.fromisoformat(sunset_time_str).strftime('%Y-%m-%dT%H:00')

    # Find matching index in hourly time series
    time_list = data['hourly']['time']
    if sunset_hour in time_list:
        index = time_list.index(sunset_hour)
        score_input = {
            'cloudcover': data['hourly']['cloudcover'][index],
            'relativehumidity_2m': data['hourly']['relativehumidity_2m'][index],
            'windspeed_10m': data['hourly']['windspeed_10m'][index],
            'precipitation': data['hourly']['precipitation'][index]
        }

        score = compute_sunset_score(score_input)
        print("🌇 Sunset Vibrancy Score @", sunset_hour, "→", score)
        print("Data used:", score_input)
    else:
        print("Sunset hour not found in hourly data.")
else:
    print("API error:", response.status_code)
