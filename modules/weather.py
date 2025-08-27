import pytz
from datetime import datetime, time, timedelta
from telegram import Update
from telegram.ext import CallbackContext
from app.services.weather_service import weather_service
from app.core.config import TIMEZONE


def get_weather():
    """
    获取当前天气信息。
    Fetches the current weather information.
    """
    try:
        return weather_service.get_weather()
    except Exception as e:
        print(f"获取天气信息时出错: {e}")
        return None


def handle_weather(bot, chat_id, message_id):
    """
    处理并发送当前天气信息。
    Handles and sends the current weather information.
    """
    weather_info = get_weather()
    if not weather_info:
        bot.send_message(
            chat_id=chat_id,
            text="抱歉，无法获取当前天气信息。",
            reply_to_message_id=message_id,
        )
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
    bot.send_message(
        chat_id=chat_id, text=text, parse_mode="HTML", reply_to_message_id=message_id
    )

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
        bot.send_message(
            chat_id=chat_id, text=attach_info, reply_to_message_id=message_id
        )


def get_forecast():
    """
    获取天气预报。
    Fetches the weather forecast.
    """
    try:
        return weather_service.get_forecast()
    except Exception as e:
        print(f"获取天气预报时出错: {e}")
        return None


def handle_forecast(bot, chat_id, message_id):
    """
    处理并发送天气预报。
    Handles and sends the weather forecast.
    """
    forecast_info = get_forecast()
    if not forecast_info:
        bot.send_message(
            chat_id=chat_id,
            text="抱歉，无法获取天气预报。",
            reply_to_message_id=message_id,
        )
        return

    timezone = pytz.timezone(TIMEZONE)
    tomorrow = datetime.now(timezone).date() + timedelta(days=1)
    tomorrow_eight_am = timezone.localize(datetime.combine(tomorrow, time(hour=8)))
    target_ts = tomorrow_eight_am.timestamp()

    for forecast in forecast_info:
        if abs(forecast["dt"] - target_ts) < 1800:  # 寻找最接近早上8点的数据 (30分钟内)
            text = (
                f"群u们🥳！<b>明天早上 8 点的天气🌤️是 {forecast['weather'][0]['description']}，"
                f"体感温度 {forecast['main']['feels_like']:.1f} ℃，湿度 {forecast['main']['humidity']:.0f} %</b>，详细情报如下捏！\n"
                f"天气：{forecast['weather'][0]['description']}\n"
                f"温度：{forecast['main']['temp']:.1f} ℃\n"
                f"体感温度：{forecast['main']['feels_like']:.1f} ℃\n"
                f"湿度：{forecast['main']['humidity']:.0f} %\n"
                f"风速：{forecast['wind']['speed']:.1f} m/s"
            )
            bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML",
                reply_to_message_id=message_id,
            )
            return

    bot.send_message(
        chat_id=chat_id,
        text="抱歉，未能找到明天早上8点的天气预报。",
        reply_to_message_id=message_id,
    )


def weather_command(update: Update, context: CallbackContext):
    handle_weather(
        context.bot,
        update.effective_chat.id,
        update.message.message_id,
    )


def forecast_command(update: Update, context: CallbackContext):
    handle_forecast(
        context.bot,
        update.effective_chat.id,
        update.message.message_id,
    )
