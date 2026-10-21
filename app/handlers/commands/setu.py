from telegram.ext import CommandHandler


async def setu_command(update, context):
    """
    处理 /setu 命令，发送一张涩图。
    Handles the /setu command, sending a setu image.
    """
    setu_service = context.bot_data.get("setu_service")
    if setu_service:
        await setu_service.send_setu(update, context)
    else:
        await update.message.reply_text("涩图服务未初始化，请联系管理员。")


def register(application):
    """
    注册 /setu 命令处理器。
    Registers the /setu command handler.
    """
    application.add_handler(CommandHandler("setu", setu_command))
