import requests
from telegram.ext import CommandHandler

from app.core import config
from app.core.config import GROUP_CHAT_ID, MASTER_ID

# DEPRECATED: OpenAI DALL·E image API 已被官方弃用，且功能所有者已不再使用 OpenAI
# DEPRECATED: the OpenAI DALL·E image API is deprecated and the feature owner dropped OpenAI.
# 保留此文件仅作历史参考，命令发现机制会跳过注册。
# Kept for historical reference only; command discovery skips registration.
DEPRECATED = True


def generate_image(prompt, api_key):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "size": "512x512",
    }
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response_json = response.json()
    image_url = response_json["data"][0]["url"]
    return image_url


def handle_image(bot, chat_id, message_id, prompt, api_key):
    image_url = generate_image(prompt, api_key)
    bot.send_photo(chat_id=chat_id, photo=image_url, reply_to_message_id=message_id)


def image_generator(update, context):
    prompt = " ".join(context.args)
    # This command is restricted to the master user or the designated group chat
    # 此命令仅限主用户或指定群组聊天使用
    if (
        update.message.from_user.id != MASTER_ID
        and update.effective_chat.id != GROUP_CHAT_ID
    ):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="抱歉，此命令仅限授权用户在指定群组中使用。",
            reply_to_message_id=update.message.message_id,
        )
        return

    if not prompt:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="请输入你想画的内容。用法: /draw <英文描述>",
            reply_to_message_id=update.message.message_id,
        )
        return

    handle_image(
        context.bot,
        update.effective_chat.id,
        update.message.message_id,
        prompt,
        # OPENAI_API_KEY 已从 config 移除；此模块已弃用且永不执行，此处惰性获取仅为保持代码完整
        # OPENAI_API_KEY was removed from config; lazily fetched here only to keep this
        # deprecated, never-executed module intact
        getattr(config, "OPENAI_API_KEY", None),
    )


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("draw", image_generator))
