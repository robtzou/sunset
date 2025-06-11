import os
import json
import requests

"""
Rate past sunsets with locations and dates found online.
"""

def rate_sunset(data):
    cc = data['cloudcover']
    rh = data['relativehumidity_2m']
    ws = data['windspeed_10m']


    score = 0

        # Cloud cover
    if 30 <= cc <= 70:
        score += 40
    elif 20 <= cc < 30 or 70 < cc <= 80:
        score += 20
    elif 10 <= cc < 20 or 80 < cc <= 90:
        score += 10

    # Humidity
    if rh < 40:
        score += 25
    elif 40 <= rh < 60:
        score += 15
    elif 60 <= rh < 75:
        score += 5

    # Wind
    if 5 <= ws <= 20:
        score += 20
    elif 2 <= ws < 5 or 20 < ws <= 30:
        score += 10

    return min(score, 100)

# input variables

latitude  = 19.021558018606985
longitude = 72.83032473928857
date      = '2025-05-03'


response = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
    'latitude'  : latitude,
    'longitude' : longitude,
    'start_date': date,
    'end_date'  : date,
    'hourly': 'temperature_2m,cloudcover,windspeed_10m,relativehumidity_2m',
    'timezone': 'auto'
})

if response.status_code == 200:
    data = response.json()
    # Assume we want the current (first hour) data
    index = 0
    score_input = {
        'cloudcover': data['hourly']['cloudcover'][index],
        'relativehumidity_2m': data['hourly']['relativehumidity_2m'][index],
        'windspeed_10m': data['hourly']['windspeed_10m'][index],

    }

    score = rate_sunset(score_input)
    print("🌇 Sunset Vibrancy Score:", score)
    print("Data used:", score_input)
else:
    print("Error fetching data:", response.status_code)