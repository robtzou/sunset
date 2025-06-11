import os
import json
import requests

"""
Save data points for future reference.
"""

# input variables

latitude  = 19.021558018606985
longitude = 72.83032473928857
date      = '2025-05-03'

CACHE_FILE = f"weather_{date}.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        data = json.load(f)
else:
    response = requests.get("https://archive-api.open-meteo.com/v1/archive", params={
        'latitude'  : latitude,
        'longitude' : longitude,
        'start_date': date,
        'end_date'  : date,
        'hourly': 'temperature_2m,cloudcover,windspeed_10m,relativehumidity_2m',
        'timezone': 'auto'
    })
    
    data = response.json()

    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

    print("Data saved. 200.")
