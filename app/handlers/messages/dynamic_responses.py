import asyncio
import random

from telegram.ext import MessageHandler, filters

from app.core.config import BOT_NAME, MASTER_ID, MISS_MACAU_ID


async def handle_dynamic_responses(update, context):
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
        await message.reply_text("Good night, Miss Macau...")
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
        await message.reply_text(exact_responses[message.text])
        return

    # 包含关键词的回复
    # Keyword-based responses
    if BOT_NAME in message.text and "你怎么看" in message.text and one_word_service:
        await message.reply_text(
            await asyncio.to_thread(one_word_service.get_one_word)
        )
        return
    elif "是吧" in message.text:
        await message.reply_text("是啊")
        return
    elif "谁问你了" in message.text:
        await message.reply_html(
            '<a href="https://www.bilibili.com/video/BV1Gc411u7s5">他问的</a>，怎么了？'
        )
        return
    elif ("来点色图" in message.text or "来点涩图" in message.text) and setu_service:
        await setu_service.send_setu(update, context)
        await message.reply_text("来叻~别让等待，成为遗憾（")
        return

    # 概率性回复
    # Probabilistic responses
    i = random.randint(1, 100)
    if i < 5:
        if message.from_user.id == MASTER_ID:
            await message.reply_text("月神正在听从您的指令✶")
        elif canned_response_service:
            response = canned_response_service.get_random_response()
            if response:
                await message.reply_text(response)
    elif i < 10 and one_word_service:
        await message.reply_text(
            await asyncio.to_thread(one_word_service.get_one_word)
        )


def register(application):
    """
    注册动态响应消息处理器。
    Registers the dynamic response message handler.
    """
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_dynamic_responses)
    )
