class DrinkWaterService:
    """
    处理喝水提醒的服务。
    Service for handling drink water reminders.
    """

    def get_drink_water_message(self) -> str:
        """
        获取喝水提醒消息。
        Gets the drink water reminder message.
        """
        return (
            "<b>月神的温馨提醒：</b>\n"
            "群u们，记得多喝水哦！💧🚰 每天喝足够的水对健康非常重要。请大家时刻保持饮水，保持健康！ 🌞"
        )
