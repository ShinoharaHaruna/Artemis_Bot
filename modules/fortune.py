import random
from time import sleep
import yaml
import pytz
from datetime import datetime


GUA = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}


def get_shichen():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    TIMEZONE = config["Basic"]["TIMEZONE"]
    timezone = pytz.timezone(TIMEZONE)
    current_time = datetime.now().astimezone(timezone)
    current_hour = current_time.hour
    if current_hour == 23:
        shichen = ("子", 1)
    elif current_hour == 0:
        shichen = ("子", 1)
    elif current_hour == 1:
        shichen = ("丑", 2)
    elif current_hour == 2:
        shichen = ("丑", 2)
    elif current_hour == 3:
        shichen = ("寅", 3)
    elif current_hour == 4:
        shichen = ("寅", 3)
    elif current_hour == 5:
        shichen = ("卯", 4)
    elif current_hour == 6:
        shichen = ("卯", 4)
    elif current_hour == 7:
        shichen = ("辰", 5)
    elif current_hour == 8:
        shichen = ("辰", 5)
    elif current_hour == 9:
        shichen = ("巳", 6)
    elif current_hour == 10:
        shichen = ("巳", 6)
    elif current_hour == 11:
        shichen = ("午", 7)
    elif current_hour == 12:
        shichen = ("午", 7)
    elif current_hour == 13:
        shichen = ("未", 8)
    elif current_hour == 14:
        shichen = ("未", 8)
    elif current_hour == 15:
        shichen = ("申", 9)
    elif current_hour == 16:
        shichen = ("申", 9)
    elif current_hour == 17:
        shichen = ("酉", 10)
    elif current_hour == 18:
        shichen = ("酉", 10)
    elif current_hour == 19:
        shichen = ("戌", 11)
    elif current_hour == 20:
        shichen = ("戌", 11)
    elif current_hour == 21:
        shichen = ("亥", 12)
    elif current_hour == 22:
        shichen = ("亥", 12)
    return shichen


def get_gua():
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
    upper_gua = GUA[upper_g_mod + 1]
    lower_gua = GUA[lower_g_mod + 1]
    return upper_gua, lower_gua, shichen, dongyao


def handle_fortune_message(bot, chat_id, message_id):
    upper_gua, lower_gua, shichen, dongyao = get_gua()
    response = f"求得复卦：上{upper_gua}下{lower_gua}，于{shichen[0]}时生，动爻为第{dongyao}爻。"
    bot.send_message(
        chat_id=chat_id,
        text=response,
        parse_mode="HTML",
        reply_to_message_id=message_id,
    )


def tell_fortune(update, context):
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
