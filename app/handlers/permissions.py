"""统一的命令权限检查 / Shared command permission checks."""

from app.core.config import GROUP_CHAT_ID, MASTER_ID


def is_master(update) -> bool:
    """判断发起者是否为 MASTER / Check whether the sender is the master."""
    message = update.message
    if message is None or message.from_user is None:
        return False
    return message.from_user.id == MASTER_ID


def is_authorized(update) -> bool:
    """判断发起者是否为 MASTER 或处于指定群组 / Check master OR designated group."""
    if update.effective_chat is not None and update.effective_chat.id == GROUP_CHAT_ID:
        return True
    return is_master(update)


def require_master(update, silent: bool = False) -> bool:
    """
    要求 MASTER 权限，拒绝时回复提示（或静默返回）。
    Require master; on denial reply with the notice (or stay silent).
    """
    if is_master(update):
        return True
    if not silent and update.message is not None:
        update.message.reply_text("该命令仅限管理员使用。")
    return False


def require_authorized(update, context) -> bool:
    """
    要求 MASTER 或指定群组权限，拒绝时回复提示。
    Require master-or-group; on denial send the notice to the chat.
    """
    if is_authorized(update):
        return True
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="抱歉，此功能仅限特定群组或管理员使用。",
        reply_to_message_id=update.message.message_id if update.message else None,
    )
    return False
