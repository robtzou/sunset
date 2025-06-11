import requests

"""
Rate the sunset visibility for a location based on daily and hourly data points.
"""

# coordinates 39.11488408061603, 36330776524 for 9701 Fields Road
latitude  =  39.114    
longitude = -77.199

parameters = {

    'latitude'  : latitude,
    'longitude' : longitude,
    'hourly': 'temperature_2m,cloudcover,windspeed_10m,relativehumidity_2m',
    'timezone': 'auto'

}

def rate_sunset():
    pass

response = requests.get("https://api.open-meteo.com/v1/forecast", params=parameters)

if response.status_code == 200:
    data = response.json()
    print("Temperature  (Celcius): ", data['hourly']['temperature_2m'][:5])
    print("Cloud Cover  (Percent): ", data['hourly']['cloudcover'][:5])
    print("Wind Speed   (km/h):    ", data['hourly']['windspeed_10m'][:5])
    print("Humidity     (Percent): ", data['hourly']['relativehumidity_2m'][:5])
else:
    print("Failed to fetch data:", response.status_code)