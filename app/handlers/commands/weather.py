from datetime import datetime, time, timedelta

import pytz
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler

from app.core.config import TIMEZONE


def weather_command(update: Update, context: CallbackContext):
    """
    处理 /weather 命令，发送当前天气信息。
    Handles the /weather command, sending current weather information.
    """
    weather_service = context.bot_data.get("weather_service")
    if not weather_service:
        update.message.reply_text("天气服务未初始化，请联系管理员。")
        return

    try:
        weather_info = weather_service.get_weather()
    except Exception as e:
        update.message.reply_text(f"抱歉，获取当前天气信息失败: {e}")
        return

    text = (
        f"当当，{weather_info['city']}的群u们🥳！<b>现在的天气🌤️是{weather_info['description']}，"
        f"体感温度 {weather_info['feels_like']:.1f} ℃，湿度 {weather_info['humidity']:.0f} %</b>，详细情报如下捏！\n"
        f"天气：{weather_info['description']}\n"
        f"温度：{weather_info['temp']:.1f} ℃\n"
        f"体感温度：{weather_info['feels_like']:.1f} ℃\n"
        f"湿度：{weather_info['humidity']:.0f} %\n"
        f"风速：{weather_info['wind_speed']:.1f} m/s"
    )
    update.message.reply_text(text, parse_mode=ParseMode.HTML)

    # 附加提醒 / Additional reminders
    feels_like = weather_info["feels_like"]
    humidity = weather_info["humidity"]
    wind_speed = weather_info["wind_speed"]
    attach_info = ""
    if feels_like > 30 and humidity > 60:
        attach_info = "真的离谱，什么蒸桑拿，又热又湿（"
    elif feels_like > 30:
        attach_info = "真的热死了，快去吹空调（"
    elif feels_like < 5 and wind_speed > 8:
        attach_info = "翻風咗，而家好凍㗎（"
    elif feels_like < 5:
        attach_info = "而家好凍㗎（"
    if attach_info:
        update.message.reply_text(attach_info)


def forecast_command(update: Update, context: CallbackContext):
    """
    处理 /forecast 命令，发送天气预报。
    Handles the /forecast command, sending the weather forecast.
    """
    weather_service = context.bot_data.get("weather_service")
    if not weather_service:
        update.message.reply_text("天气服务未初始化，请联系管理员。")
        return

    try:
        forecast_info = weather_service.get_forecast()
    except Exception as e:
        update.message.reply_text(f"抱歉，获取天气预报失败: {e}")
        return

    timezone = pytz.timezone(TIMEZONE)
    tomorrow = datetime.now(timezone).date() + timedelta(days=1)
    tomorrow_eight_am = timezone.localize(datetime.combine(tomorrow, time(hour=8)))
    target_ts = tomorrow_eight_am.timestamp()

    for forecast in forecast_info:
        if abs(forecast["dt"] - target_ts) < 1800:  # 寻找最接近早上8点的数据 (30分钟内)
            text = (
                f"群u们🥳！<b>明天早上 8 点的天气🌤️是 {forecast['weather'][0]['description']}，"
                f"体感温度 {forecast['main']['feels_like']:.1f} ℃，湿度 "
                f"{forecast['main']['humidity']:.0f} %</b>，详细情报如下捏！\n"
                f"天气：{forecast['weather'][0]['description']}\n"
                f"温度：{forecast['main']['temp']:.1f} ℃\n"
                f"体感温度：{forecast['main']['feels_like']:.1f} ℃\n"
                f"湿度：{forecast['main']['humidity']:.0f} %\n"
                f"风速：{forecast['wind']['speed']:.1f} m/s"
            )
            update.message.reply_text(text, parse_mode=ParseMode.HTML)
            return

    update.message.reply_text("抱歉，未能找到明天早上8点的天气预报。")


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("weather", weather_command))
    dispatcher.add_handler(CommandHandler("forecast", forecast_command))
