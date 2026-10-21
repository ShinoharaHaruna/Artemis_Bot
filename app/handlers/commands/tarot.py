import asyncio

from telegram.ext import CommandHandler

from app.handlers.permissions import require_authorized


async def tarot_command(update, context):
    """
    处理 /tarot 命令，执行塔罗牌占卜。
    Handles the /tarot command, performing a tarot reading.
    """
    if not await require_authorized(update, context):
        return

    tarot_service = context.bot_data.get("tarot_service")
    llm_service = context.bot_data.get("llm_service")

    if not tarot_service:
        await update.message.reply_text("塔罗牌服务未初始化，请联系管理员。")
        return

    if not llm_service:
        await update.message.reply_text("LLM 服务未配置，请联系管理员。")
        return

    topic = " ".join(context.args) if context.args else None

    try:
        cards = tarot_service.draw_cards(num_cards=3)
        if not cards:
            await update.message.reply_text("无法抽牌，牌堆为空。")
            return

        prompt = tarot_service.create_interpretation_prompt(cards, topic)

        # Let the user know the bot is thinking
        thinking_message = await update.message.reply_text("正在解读牌意，请稍候...")

        interpretation = await asyncio.to_thread(llm_service.get_response, prompt)

        # Edit the thinking message with the final interpretation
        await thinking_message.edit_text(interpretation)

    except Exception as e:
        await update.message.reply_text(f"占卜过程中出现错误: {e}")


def register(application):
    """
    注册 /tarot 命令处理器。
    Registers the /tarot command handler.
    """
    application.add_handler(CommandHandler("tarot", tarot_command))
