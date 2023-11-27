from ImplClass.OpenWeather import OpenWeather
import pytz
from datetime import datetime, time, timedelta
import yaml


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
WEATHER_API_KEY = config["Weather"]["API_KEY"]
WEATHER_LAT = config["Weather"]["LAT"]
WEATHER_LON = config["Weather"]["LON"]
TIMEZONE = config["Basic"]["TIMEZONE"]


def get_weather(API_KEY):
    # 如果API_KEY不是一个32位的字符串，那么直接返回None
    if len(API_KEY) != 32:
        return None
    weather = OpenWeather(API_KEY, WEATHER_LAT, WEATHER_LON)
    weather_info = weather.getWeather()
    return weather_info


def handle_weather(bot, chat_id, API_KEY, message_id):
    weather_info = get_weather(API_KEY)
    weather_type = weather_info[0]
    temp = weather_info[1]
    feels_like = weather_info[2]
    humidity = weather_info[5]
    wind_speed = weather_info[6]
    city = weather_info[7]
    bot.send_message(
        chat_id=chat_id,
        text="""
        当当，{}的群u们🥳！<b>现在的天气🌤️是{}，体感温度 {} ℃，湿度 {} %</b>，详细情报如下捏！
        天气：{}
        温度：{} ℃
        体感温度：{} ℃
        湿度：{} %
        风速：{} m/s
        """.format(
            city,
            weather_type,
            feels_like,
            humidity,
            weather_type,
            temp,
            feels_like,
            humidity,
            wind_speed,
        ),
        parse_mode="HTML",
        reply_to_message_id=message_id,
    )
    AttachInfo = ""
    if feels_like > 30 and humidity > 60:
        AttachInfo = "真的离谱，什么蒸桑拿，又热又湿（"
    elif feels_like > 30:
        AttachInfo = "真的热死了，快去吹空调（"
    elif feels_like < 5 and wind_speed > 8:
        AttachInfo = "翻風咗，而家好凍㗎（"
    elif feels_like < 5:
        AttachInfo = "而家好凍㗎（"
    if AttachInfo != "":
        bot.send_message(
            chat_id=chat_id,
            text="""
            {}
            """.format(
                AttachInfo,
            ),
            reply_to_message_id=message_id,
        )


def get_forecast(API_KEY):
    # 如果API_KEY不是一个32位的字符串，那么直接返回None
    if len(API_KEY) != 32:
        return None
    weather = OpenWeather(API_KEY, WEATHER_LAT, WEATHER_LON)
    forecast_info = weather.getForecast()
    return forecast_info


def handle_forecast(bot, chat_id, API_KEY, TIMEZONE, message_id):
    forecast_info = get_forecast(API_KEY)
    timezone = pytz.timezone(TIMEZONE)
    tomorrow = datetime.now().date() + timedelta(days=1)
    tomorrow_eight_am = timezone.localize(datetime.combine(tomorrow, time(hour=8)))
    tomorrow_eight_am_ts = tomorrow_eight_am.astimezone(pytz.utc).timestamp()
    for forecast in forecast_info:
        forecast_time = forecast["dt"]
        if forecast_time == tomorrow_eight_am_ts:
            weather_type = forecast["weather"][0]["description"]
            temp = forecast["main"]["temp"]
            feels_like = forecast["main"]["feels_like"]
            humidity = forecast["main"]["humidity"]
            wind_speed = forecast["wind"]["speed"]
            bot.send_message(
                chat_id=chat_id,
                text="""
                群u们🥳！<b>明天早上 8 点的天气🌤️是 {}，体感温度 {} ℃，湿度 {} %</b>，详细情报如下捏！
        天气：{}
        温度：{} ℃
        体感温度：{} ℃
        湿度：{} %
        风速：{} m/s
                """.format(
                    weather_type,
                    feels_like,
                    humidity,
                    weather_type,
                    temp,
                    feels_like,
                    humidity,
                    wind_speed,
                ),
                parse_mode="HTML",
                reply_to_message_id=message_id,
            )
            break


def weather_command(update, context):
    handle_weather(
        context.bot,
        update.effective_chat.id,
        WEATHER_API_KEY,
        update.message.message_id,
    )


def forecast_command(update, context):
    handle_forecast(
        context.bot,
        update.effective_chat.id,
        WEATHER_API_KEY,
        TIMEZONE,
        update.message.message_id,
    )
