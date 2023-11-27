from telegram import ParseMode
import modules.weather as weather
import pytz
from datetime import datetime, time, timedelta


def send_off_work_message(bot, chat_id, API_KEY, TIMEZONE):
    forecast_info = weather.get_forecast(API_KEY)
    timezone = pytz.timezone(TIMEZONE)
    tomorrow = datetime.now().date() + timedelta(days=1)
    tomorrow_eight_am = timezone.localize(datetime.combine(tomorrow, time(hour=8)))
    tomorrow_eight_am_ts = tomorrow_eight_am.astimezone(pytz.utc).timestamp()
    for forecast in forecast_info:
        forecast_time = forecast["dt"]
        if forecast_time == tomorrow_eight_am_ts:
            weather_type = forecast["weather"][0]["description"]
            feels_like = forecast["main"]["feels_like"]
            humidity = forecast["main"]["humidity"]
            notification = """
            <b>早该下班叻！</b>
        只要一息尚存，我便坚持不懈。
        <b>明天早上 8 点的天气🌤️是{}，体感温度 {} ℃，湿度 {} %</b>，请群u注意捏！今天也辛苦了，请务必好好休息捏！
            """.format(
                weather_type, feels_like, humidity
            )

            bot.send_message(
                chat_id=chat_id, text=notification, parse_mode=ParseMode.HTML
            )
            break
