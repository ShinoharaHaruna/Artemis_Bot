from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def timer_handler(update: Update, context: CallbackContext):
    """
    处理 /timer 命令，用于开始或停止计时器。
    Handles the /timer command to start or stop a timer.
    """
    chat_id = update.effective_chat.id

    # 从 context.chat_data 中获取计时器状态
    # Get timer status from context.chat_data
    timer_on = context.chat_data.get("timer_on", False)

    if timer_on:
        # 停止计时器 / Stop the timer
        timer_start_time = context.chat_data.get("timer_start_time")
        if timer_start_time:
            delta = datetime.now() - timer_start_time
            context.bot.send_message(
                chat_id=chat_id, text=f"计时结束！\n用时：{delta.seconds}秒"
            )
            # 清理状态 / Clean up state
            del context.chat_data["timer_on"]
            del context.chat_data["timer_start_time"]
        else:
            # 状态异常，重置 / Abnormal state, reset
            context.bot.send_message(
                chat_id=chat_id, text="计时器状态异常，已重置。请重新开始。"
            )
            context.chat_data["timer_on"] = False

    else:
        # 开始计时器 / Start the timer
        context.chat_data["timer_on"] = True
        context.chat_data["timer_start_time"] = datetime.now()
        context.bot.send_message(chat_id=chat_id, text="计时开始！")


def register(dispatcher):
    """
    注册 timer 命令处理器。
    Registers the timer command handler.
    """
    dispatcher.add_handler(CommandHandler("timer", timer_handler))
