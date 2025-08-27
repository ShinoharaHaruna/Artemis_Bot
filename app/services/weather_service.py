import requests
from app.core.config import WEATHER_API_KEY, WEATHER_LAT, WEATHER_LON


class WeatherService:
    """
    天气服务，用于获取天气信息。
    Weather service for fetching weather information.
    """

    def __init__(self, api_key=WEATHER_API_KEY, lat=WEATHER_LAT, lon=WEATHER_LON):
        """
        初始化天气服务。
        Initializes the weather service.

        Args:
            api_key (str): OpenWeatherMap API 密钥。
            lat (str): 纬度。
            lon (str): 经度。
        """
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=zh_cn"
        self.forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=zh_cn"

    def get_weather(self):
        """
        获取当前天气信息。
        Fetches the current weather information.

        Returns:
            dict: 包含天气信息的字典。
                  Returns a dictionary containing weather information.
        """
        response = requests.get(self.weather_url)
        response.raise_for_status()  # 如果请求失败则抛出异常 / Raise an exception for a failed request
        data = response.json()
        return {
            "description": data["weather"][0]["description"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "city": data["name"],
        }

    def get_forecast(self):
        """
        获取天气预报。
        Fetches the weather forecast.

        Returns:
            list: 包含天气预报信息的列表。
                  Returns a list containing weather forecast information.
        """
        response = requests.get(self.forecast_url)
        response.raise_for_status()  # 如果请求失败则抛出异常 / Raise an exception for a failed request
        data = response.json()
        return data["list"]


# 创建一个单例 / Create a singleton instance
weather_service = WeatherService()
