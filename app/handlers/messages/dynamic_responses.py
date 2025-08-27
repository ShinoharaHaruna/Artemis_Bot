import random
from telegram.ext import Filters, MessageHandler
from app.core.config import BOT_NAME, MASTER_ID, MISS_MACAU_ID


def handle_dynamic_responses(update, context):
    """
    处理各种动态和随机的用户消息。
    Handles various dynamic and random user messages.
    """
    message = update.message
    if not message or not message.text:
        return

    # 服务获取
    # Service retrieval
    one_word_service = context.bot_data.get("one_word_service")
    canned_response_service = context.bot_data.get("canned_response_service")
    setu_service = context.bot_data.get("setu_service")

    # 特定用户和关键词的特殊处理
    # Special handling for specific users and keywords
    if message.from_user.id == MISS_MACAU_ID and "晚安" in message.text:
        message.reply_text("Good night, Miss Macau...")
        return

    # 精确匹配的回复
    # Exact match responses
    exact_responses = {
        "？": "？",
        "6": "7",
        "捏麻麻滴": "捏捏你的",
        "捏妈妈滴": "捏捏你的",
    }
    if message.text in exact_responses:
        message.reply_text(exact_responses[message.text])
        return

    # 包含关键词的回复
    # Keyword-based responses
    if BOT_NAME in message.text and "你怎么看" in message.text and one_word_service:
        message.reply_text(one_word_service.get_one_word())
    elif "是吧" in message.text:
        message.reply_text("是啊")
    elif "谁问你了" in message.text:
        message.reply_html(
            '<a href="https://www.bilibili.com/video/BV1Gc411u7s5">他问的</a>，怎么了？'
        )
    elif ("来点色图" in message.text or "来点涩图" in message.text) and setu_service:
        setu_service.send_setu(update, context)
        message.reply_text("来叻~别让等待，成为遗憾（")

    # 概率性回复
    # Probabilistic responses
    i = random.randint(1, 100)
    if i < 5:
        if message.from_user.id == MASTER_ID:
            message.reply_text("月神正在听从您的指令✶")
        elif canned_response_service:
            response = canned_response_service.get_random_response()
            if response:
                message.reply_text(response)
    elif i < 10 and one_word_service:
        message.reply_text(one_word_service.get_one_word())


def register(dispatcher):
    """
    注册动态响应消息处理器。
    Registers the dynamic response message handler.
    """
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_dynamic_responses)
    )
