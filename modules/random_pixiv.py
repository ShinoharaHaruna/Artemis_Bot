import requests


def random_pixiv_img(bot, chat_id, message_id):
    url = "https://pixiv-api.vercel.app/api"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "}
    response = requests.get(url, headers=headers)
    # Save the response as a jpg file
    with open("pixiv.jpg", "wb") as f:
        f.write(response.content)
    bot.send_photo(
        chat_id=chat_id, photo=open("pixiv.jpg", "rb"), reply_to_message_id=message_id
    )


def handle_random_pixiv(update, context):
    random_pixiv_img(context.bot, update.effective_chat.id, update.message.message_id)
