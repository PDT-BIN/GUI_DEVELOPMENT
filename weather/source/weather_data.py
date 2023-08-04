import requests
from settings import *


def get_weather(latitude: float, longitude: float, units: str, period: str):
    # GET DATA FROM API.
    url = f'{BASE_URL}&lat={latitude}&lon={longitude}&appid={API_KEY}&units={units}'
    respone = requests.get(url)
    # STORE DATA.
    today_data = {}
    forecast_data = {}
    if respone.status_code == 200:
        data = respone.json()
        # TODAY.
        for index, data_entry in enumerate(data['list']):
            if index == 0:
                today_data['temp'] = int(
                    round(data_entry['main']['temp'], 0))
                today_data['feels_like'] = int(
                    round(data_entry['main']['feels_like'], 0))
                today_data['weather'] = data_entry['weather'][0]['main']
                today = data_entry['dt_txt'].split(' ')[0]
            else:
                if data_entry['dt_txt'].split(' ')[0] != today:
                    milestone = index + 4
                    break
        # FORECAST.
        for index in range(milestone, len(data['list']), 8):
            forecast_entry = data['list'][index]
            forecast_data[forecast_entry['dt_txt'].split(' ')[0]] = {
                'temp': round(forecast_entry['main']['temp'], 0),
                'feels_like': round(forecast_entry['main']['temp'], 0),
                'weather': forecast_entry['weather'][0]['main']
            }
    # RETURN DATA.
    return today_data if period == 'today' else forecast_data
