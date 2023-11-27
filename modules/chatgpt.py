import requests


def get_chatbot_response(message, API_KEY):
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
                "content": "你是阿尔忒弥斯，是群组的月神，并且你能回答群组成员的话。",
            },
            {"role": "user", "content": message},
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    chatbot_response = response_json["choices"][0]["message"]["content"]
    return chatbot_response


def handle_message(bot, chat_id, message, API_KEY):
    # 处理用户消息的逻辑
    chatbot_response = get_chatbot_response(message, API_KEY)
    # 发送ChatGPT的回复
    bot.send_message(
        chat_id=chat_id, text=chatbot_response, parse_mode='Markdown'
    )
