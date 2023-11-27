from BaseClass.BaseWeather import BaseWeather
import requests


class OpenWeather(BaseWeather):
    def __init__(self, API_KEY, LAT, LON):
        super().__init__(API_KEY, LAT, LON)
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric&lang=zh_cn".format(
            LAT, LON, API_KEY
        )
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric&lang=zh_cn".format(
            LAT, LON, API_KEY
        )

    # 要的参数包括：
    # 1. 天气类型
    # 2. 温度
    # 3. 体感温度
    # 4. 最低气温
    # 5. 最高气温
    # 6. 湿度
    # 7. 风速
    # 8. 城市
    def getWeather(self):
        response = requests.get(self.weather_url)
        data = response.json()
        weather_info = []
        weather_info.append(data["weather"][0]["description"])  # 天气类型
        weather_info.append(data["main"]["temp"])  # 温度
        weather_info.append(data["main"]["feels_like"])  # 体感温度
        weather_info.append(data["main"]["temp_min"])  # 最低气温
        weather_info.append(data["main"]["temp_max"])  # 最高气温
        weather_info.append(data["main"]["humidity"])  # 湿度
        weather_info.append(data["wind"]["speed"])  # 风速
        weather_info.append(data["name"])  # 城市
        return weather_info

    def getForecast(self):
        response = requests.get(self.forecast_url)
        data = response.json()
        forecast_info = data["list"]
        return forecast_info
