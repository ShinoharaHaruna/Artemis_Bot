import requests


def get_a_setu(bot, chat_id, message_id):
    url = "https://api.nyan.xyz/httpapi/sexphoto?r18=true"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "}
    response = requests.get(url, headers=headers)
    response_json = response.json()
    bot.send_message(
        chat_id=chat_id,
        text=f'||[又看涩图！那，那……那就给你吧\~]({response_json["data"]["url"][0]})||',
        parse_mode="MarkdownV2",
        reply_to_message_id=message_id,
        disable_web_page_preview=True,
    )


def setu_command(update, context):
    get_a_setu(context.bot, update.effective_chat.id, update.message.message_id)
