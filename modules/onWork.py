from telegram import ParseMode
import modules.weather as weather
from modules.one_word import get_one_word


def send_on_work_message(bot, chat_id, API_KEY):
    weather_info = weather.get_weather(API_KEY)
    weather_type = weather_info[0]
    feels_like = weather_info[2]
    humidity = weather_info[5]
    notification = """
        <b>早上好哇！今天也要元气满满地加油哦！</b>
        {}
        <b>今天早上 8 点的天气🌤️是{}，体感温度 {} ℃，湿度 {} %</b>，请群u注意捏！
        """.format(
        get_one_word(), weather_type, feels_like, humidity
    )

    bot.send_message(chat_id=chat_id, text=notification, parse_mode=ParseMode.HTML)
