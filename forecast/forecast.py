# import required modules
from datetime import datetime

import requests
import pgeocode
import credentials


class Forecast:
    def __init__(self, data):
        self.current = Current(data['current'])
        self.hourly = [Hourly(hourly_data) for hourly_data in data['hourly']]
        self.daily = [Daily(daily_data) for daily_data in data['daily']]


class Current:
    def __init__(self, data):
        self.standouts = []
        self.dt = datetime.fromtimestamp(data['dt'])
        self.sunrise = datetime.fromtimestamp(data['sunrise']).strftime("%I:%M %p")
        self.sunset = datetime.fromtimestamp(data['sunset']).strftime("%I:%M %p")
        self.temp = data['temp']
        self.feels_like = data['feels_like']
        self.pressure = data['pressure']
        self.humidity = data['humidity']
        self.dew_point = data['dew_point']
        self.uvi = data['uvi']
        self.clouds = data['clouds']
        self.visibility = data['visibility']
        self.wind_speed = data['wind_speed']
        self.wind_deg = data['wind_deg']
        self.weather = [Weather(weather_data) for weather_data in data['weather']]

    def __str__(self):
        return "Today" ": " + str(self.weather[0])

class Hourly:
    def __init__(self, data):
        self.dt = datetime.fromtimestamp(data['dt']).strftime("%a %I %p")
        self.temp = int(data['temp'])
        self.feels_like = int(data['feels_like'])
        self.pressure = data['pressure']
        self.humidity = data['humidity']
        self.dew_point = int(data['dew_point'])
        self.uvi = data['uvi']
        self.clouds = str(data['clouds']) + '%'
        self.visibility = data['visibility']
        self.wind_speed = data['wind_speed']
        self.wind_deg = data['wind_deg']
        self.wind_gust = data['wind_gust']
        self.weather = [Weather(weather_data) for weather_data in data['weather']]
        self.pop = data['pop']

    def __str__(self):
        return self.dt + ": " + str(self.weather[0])


class Daily:
    def __init__(self, data):
        self.dt = datetime.fromtimestamp(data['dt'])
        self.sunrise = datetime.fromtimestamp(data['sunrise']).strftime("%I:%M %p")
        self.sunset = datetime.fromtimestamp(data['sunset']).strftime("%I:%M %p")
        self.moonrise = datetime.fromtimestamp(data['moonrise']).strftime("%I:%M %p")
        self.moonset = datetime.fromtimestamp(data['moonset']).strftime("%I:%M %p")
        self.moon_phase = data['moon_phase']
        self.summary = data['summary']
        self.temp = {
            'day': data['temp']['day'],
            'min': data['temp']['min'],
            'max': data['temp']['max'],
            'night': data['temp']['night'],
            'eve': data['temp']['eve'],
            'morn': data['temp']['morn']
        }
        self.feels_like = {
            'day': data['feels_like']['day'],
            'night': data['feels_like']['night'],
            'eve': data['feels_like']['eve'],
            'morn': data['feels_like']['morn']
        }
        self.pressure = data['pressure']
        self.humidity = data['humidity']
        self.dew_point = data['dew_point']
        self.wind_speed = data['wind_speed']
        self.wind_deg = data['wind_deg']
        self.wind_gust = data['wind_gust']
        self.weather = [Weather(weather_data) for weather_data in data['weather']]
        self.clouds = data['clouds']
        self.pop = data['pop']
        self.rain = data.get('rain', None)
        self.snow = data.get('snow', None)
        self.uvi = data['uvi']

    def __str__(self):
        result = ""
        if self.dt.date() != datetime.today().date() and \
                self.dt.strftime("%a") == datetime.today().strftime("%a"):
            result += "Next "
        return result + self.dt.strftime("%a") + ": " + str(self.weather[0])


class Weather:
    def __init__(self, data):
        self.id = data['id']
        self.main = data['main']
        self.description = data['description']
        self.icon = data['icon']

    def __str__(self):
        return self.description


nomi = pgeocode.Nominatim('us')
query = nomi.query_postal_code("11360")

data = {
    "lat": query["latitude"],
    "lon": query["longitude"]
}

api_key = credentials.api_key


def get_forecast(zipcode):
    """
    Gets the full forecast at the specified zip code and returns it in one
    Forecast object. This function makes an API Call to OpenWeather

    :param zipcode: The zipcode of the location for the forecast
    :return forecast: A Forecast object containing the results of the API Call
    """
    # base_url variable to store url
    base_url = "https://api.openweathermap.org/data/3.0/onecall?"
    lat = "lat=" + str(data["lat"])
    long = "&lon=" + str(data["lon"])
    units = "&units=" + "imperial"
    appid = "&appid=" + api_key

    complete_url = base_url + lat + long + units + appid

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    return Forecast(x)
