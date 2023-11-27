import requests
import yaml


def generate_image(prompt, OPENAI_API_KEY):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": "Bearer " + OPENAI_API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "size": "512x512",
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    image_url = response_json["data"][0]["url"]
    return image_url


def handle_image(bot, chat_id, message_id, prompt, API_KEY):
    image_url = generate_image(prompt, API_KEY)
    bot.send_photo(chat_id=chat_id, photo=image_url, reply_to_message_id=message_id)


def image_generator(update, context):
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    MASTER_ID = config["Basic"]["MASTER_ID"]
    GROUP_CHAT_ID = config["GroupChat"][0][0]
    OPENAI_API_KEY = config["OpenAI"]["OPENAI_API_KEY"]
    prompt = " ".join(context.args)
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
    handle_image(
        context.bot,
        update.effective_chat.id,
        update.message.message_id,
        prompt,
        OPENAI_API_KEY,
    )
