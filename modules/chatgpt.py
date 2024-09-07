import requests
import yaml


def get_chatbot_response(message, API_KEY, system_prompt = "你是阿尔忒弥斯，是群组的月神，并且你能回答群组成员的话。"):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": message},
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    chatbot_response = response_json["choices"][0]["message"]["content"]
    return chatbot_response


def handle_message(bot, chat_id, message, API_KEY, message_id):
    # 处理用户消息的逻辑
    chatbot_response = get_chatbot_response(message, API_KEY)
    # 发送ChatGPT的回复
    bot.send_message(
        chat_id=chat_id,
        text=chatbot_response,
        parse_mode="Markdown",
        reply_to_message_id=message_id,
    )


def chat_command(update, context, system_prompt = "你是阿尔忒弥斯，是群组的月神，并且你能回答群组成员的话。"):
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    MASTER_ID = config["Basic"]["MASTER_ID"]
    GROUP_CHAT_ID = config["GroupChat"][0][0]
    OPENAI_API_KEY = config["OpenAI"]["OPENAI_API_KEY"]
    if context.args is None:
        message = update.message.text
        print("AI is trying to respond to:", message)
    else:
        message = " ".join(context.args)  # 获取命令后的字符串作为message
    if (
        update.message.from_user.id != MASTER_ID
        and update.effective_chat.id != GROUP_CHAT_ID
    ):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry喇，呢個係channel only嘅",
            reply_to_message_id=update.message.message_id,
        )
        return
    handle_message(
        context.bot,
        update.effective_chat.id,
        message,
        OPENAI_API_KEY,
        update.message.message_id,
    )  # 调用处理消息的函数
