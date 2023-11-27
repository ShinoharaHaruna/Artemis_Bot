from telegram import ParseMode

def send_drink_water_message(bot, chat_id):
    notification = """
    <b>月神的温馨提醒：</b>
    群u们，记得多喝水哦！💧🚰 每天喝足够的水对健康非常重要。请大家时刻保持饮水，保持健康！ 🌞
    """

    bot.send_message(chat_id=chat_id, text=notification, parse_mode=ParseMode.HTML)
