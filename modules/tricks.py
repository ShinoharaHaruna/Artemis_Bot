from modules.random_pixiv import random_pixiv_img
from modules.chatgpt import chat_command
import random
import yaml
from modules.one_word import get_one_word


my_dict = [
    "嗯……",
    #     "也就那样吧",
    #     "还行吧",
    #     "6",
    #     "666",
    #     "nb",
    "那确实",
    #     "哎不是",
    #     "呃呃",
    #     "真受不了",
    #     "有点无语了",
    #     "说实话有点无语了",
    "确实",
    #     "还可以吧",
    #     "急什么",
    #     "你先别急",
    #     "扎不多得勒",
    #     "我不好说",
    #     "你急什么",
    "还真是",
    "都什么年代了",
    #     "这是典型的gn",
]


def kanji_extract(text):
    kanji = []
    for char in text:
        if char >= "\u4e00" and char <= "\u9fff":
            kanji.append(char)
    return kanji


def handle_message(update, context):
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    BOT_NAME = config["Basic"]["BOT_NAME"]
    MASTER_ID = config["Basic"]["MASTER_ID"]
    MISS_MACAU_ID = config["Basic"]["MISS_MACAU_ID"]
    print("# Msg: ^", update.message, "$")
    if update.message.text is None:
        return
    if update.message.from_user.id == MISS_MACAU_ID:
        if "晚安" in update.message.text:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Good night, Miss Macau...",
                reply_to_message_id=update.message.message_id,
            )
            return
    message = update.message.text
    if "？" == message:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="？",
            reply_to_message_id=update.message.message_id,
        )
    if "6" == message:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="7",
            reply_to_message_id=update.message.message_id,
        )
    if "捏麻麻滴" == message or "捏妈妈滴" == message:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="捏捏你的",
            reply_to_message_id=update.message.message_id,
        )
    if BOT_NAME in message and "你怎么看" in message:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_one_word(),
            reply_to_message_id=update.message.message_id,
        )
    if "是吧" in message:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="是啊",
            reply_to_message_id=update.message.message_id,
        )
    #     elif "我都可以" in message:
    #         context.bot.send_message(
    #             chat_id=update.effective_chat.id,
    #             text="非常坏答案😡恨来自月神",
    #             reply_to_message_id=update.message.message_id,
    #         )
    elif "谁问你了" in message:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='<a href="https://www.bilibili.com/video/BV1Gc411u7s5">他问的</a>，怎么了？',
            parse_mode="HTML",
            reply_to_message_id=update.message.message_id,
        )
    elif "来点色图" in message or "来点涩图" in message:
        random_pixiv_img(
            context.bot, update.effective_chat.id, update.message.message_id
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="来叻~别让等待，成为遗憾（",
            reply_to_message_id=update.message.message_id,
        )

    i = random.randint(1, 100)
    if i < 5:
        if update.message.from_user.id == MASTER_ID:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="月神正在听从您的指令✶",
                reply_to_message_id=update.message.message_id,
            )
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=random.choice(my_dict),
                reply_to_message_id=update.message.message_id,
            )
    elif i < 10:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_one_word(),
            reply_to_message_id=update.message.message_id,
        )
    # elif i < 100:
    #     # Let's make a random AI reply
    #     # PROBABILTY = 1
    #     # if random.random() < PROBABILTY:
    #     print("Random AI reply")
    #     chat_command(
    #         update,
    #         context,
    #         system_prompt="你是 b 站的梗界扛把子，回复网友时要像开挂一样，疯狂融入各种互联网梗，语言风格要骚气冲天、笑果无敌，确保大家笑到打鸣：",
    #     )
    #     print("Random AI reply ends")
    #     # Random AI reply ends
