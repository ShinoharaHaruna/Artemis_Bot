import yaml


def admin_command(update, context):
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    GROUP_ID = config["GroupChat"][0][0]
    MASTER_ID = config["Basic"]["MASTER_ID"]
    message = update.message
    if message.text is None:
        return
    if update.message.from_user.id != MASTER_ID:
        return
    context.bot.send_message(
        chat_id=GROUP_ID,
        text=message.text.replace("/admin ", ""),
        parse_mode="HTML",
    )


def anonymous_command(update, context):
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    GROUP_ID = config["GroupChat"][0][0]
    message = update.message
    if message.text is None:
        return
    if update.effective_chat.id == GROUP_ID:
        context.bot.delete_message(
            chat_id=update.effective_chat.id, message_id=update.message.message_id
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='私聊月神才可以匿名哦~发送"/anonymous + 消息"，即可匿名发送消息',
        )
        return
    context.bot.send_message(
        chat_id=GROUP_ID,
        text=message.text.replace("/anonymous ", "匿名消息："),
        parse_mode="MarkdownV2",
    )
