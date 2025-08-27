import random
from time import sleep
import pytz
from datetime import datetime
from telegram.ext import CommandHandler
from app.core.config import TIMEZONE

GUA = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}


def get_shichen():
    """根据当前时间获取时辰。"""
    # get shichen based on current time
    timezone = pytz.timezone(TIMEZONE)
    current_hour = datetime.now().astimezone(timezone).hour
    shichen_map = {
        (23, 0): ("子", 1),
        (1, 2): ("丑", 2),
        (3, 4): ("寅", 3),
        (5, 6): ("卯", 4),
        (7, 8): ("辰", 5),
        (9, 10): ("巳", 6),
        (11, 12): ("午", 7),
        (13, 14): ("未", 8),
        (15, 16): ("申", 9),
        (17, 18): ("酉", 10),
        (19, 20): ("戌", 11),
        (21, 22): ("亥", 12),
    }
    for hours, shichen_info in shichen_map.items():
        if current_hour in hours:
            return shichen_info
    return ("子", 1)  # Default case


def get_gua():
    """生成卦象。"""
    # generate gua
    RAND_MIN = 1
    RAND_MAX = 128
    upper_g = random.randint(RAND_MIN, RAND_MAX)
    lower_g = random.randint(RAND_MIN, RAND_MAX)
    upper_g_mod = upper_g % 8
    lower_g_mod = lower_g % 8
    shichen = get_shichen()
    dongyao = (shichen[1] + upper_g_mod + lower_g_mod) % 6
    if dongyao == 0:
        dongyao = 6
    upper_gua = GUA.get(upper_g_mod + 1, "未知")
    lower_gua = GUA.get(lower_g_mod + 1, "未知")
    return upper_gua, lower_gua, shichen, dongyao


def handle_fortune_message(bot, chat_id, message_id):
    """处理算卦消息。"""
    # handle fortune message
    upper_gua, lower_gua, shichen, dongyao = get_gua()
    response = f"求得复卦：上{upper_gua}下{lower_gua}，于{shichen[0]}时生，动爻为第{dongyao}爻。"
    bot.send_message(
        chat_id=chat_id,
        text=response,
        parse_mode="HTML",
        reply_to_message_id=message_id,
    )


def tell_fortune(update, context):
    """处理 /suangua 命令。"""
    # handle /suangua command
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="静心，想好问题，求得卦象。",
        parse_mode="HTML",
        reply_to_message_id=update.message.message_id,
    )
    sleep(6)
    handle_fortune_message(
        context.bot,
        update.effective_chat.id,
        update.message.message_id,
    )


def register(dispatcher):
    """注册 /suangua 命令处理器。"""
    # register /suangua command handler
    dispatcher.add_handler(CommandHandler("suangua", tell_fortune))
