from telegram.ext import CommandHandler


def list_help(update, context):
    """显示帮助信息。"""
    # display help message
    help_message = """
    <b>月神的温馨提示：</b>
    <b>1. 喝水提醒</b>
    月神会在每天的以下时间提醒大家喝水：
    08:50, 09:50, 11:00, 12:30, 14:50, 15:50, 17:00, 18:30, 20:50
    <b>2. 下班提醒</b>
    月神会在工作日晚上 22:30 提醒大家下班，并给出明天早上 8 点的天气情况。
    <b>3. 聊天功能</b>
    月神可以和大家聊天哦！只需要在群组中输入/chat+空格+你想说的话，月神就会回复你啦！
    例如：/chat 你好呀！
    <b>4. 生成图片</b>
    月神可以根据你输入的文字生成图片哦！只需要在群组中输入/draw+空格+你想说的话，月神就会生成图片并发送给你啦！
    <b>5. 天气查询</b>
    月神可以查询你的天气哦！只需要在群组中输入/weather，月神就会发送今日的天气情况给你啦！
    <b>6. 未来天气查询</b>
    月神可以查询你明早早八的天气哦！只需要在群组中输入/forecast，月神就会发送给你啦！
    <b>7. 随机Pixiv图片</b>
    月神可以发送随机的Pixiv图片哦！只需要在群组中输入/random_pixiv，月神就会发送给你啦！
    <b>8. 一言</b>
    月神可以给你一句箴言哦！只需要在群组中@月神+“你怎么看”，月神就会发送给你啦！
    <b>9. 答案之书</b>
    月神可以赐你回答！在群组中输入“/answer”，跟上你的问题，月神就会给你答案！
    <b>10. 学术查询</b>
    月神可以帮你在Google Scholar中查询哦！只需要在群组中输入/scholar+空格+你想查询的内容，月神就会发送给你啦！
    例如：/scholar 月神
    <b>11. 营养查询</b>
    月神可以帮你在FatSecret中查询哦！只需要在群组中输入/food+空格+你想查询的内容，月神就会发送给你啦！
    <b>12. 塔罗占卜</b>
    月神可以帮你进行塔罗占卜哦！只需要在群组中输入/tarot，后面可以选择跟上你想问的话题，月神就会为你用塔罗牌占卜！
    例如：/tarot 我想知道我明天的运势
    <b>13. 设置提醒</b>
    月神可以帮你设置提醒哦！只需要在私聊中输入/reminder YYYYMMDDHHMM <提醒内容>，月神就会在指定时间提醒你！
    例如：/reminder 202508281930 去看电影
    """

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_message,
        parse_mode="HTML",
        reply_to_message_id=update.message.message_id,
    )


def register(dispatcher):
    """注册 /help 命令处理器。"""
    # register /help command handler
    dispatcher.add_handler(CommandHandler("help", list_help))
