from datetime import datetime, time, timedelta
import pytz
from app.services.weather_service import WeatherService
from app.core.config import TIMEZONE


class OffWorkService:
    """
    处理下班提醒的服务。
    Service for handling off-work reminders.
    """

    def __init__(self, weather_service: WeatherService):
        """
        初始化服务。
        Initializes the service.

        Args:
            weather_service (WeatherService): 天气服务实例。
        """
        self.weather_service = weather_service

    def get_off_work_message(self) -> str:
        """
        获取下班提醒消息，包含天气预报。
        Gets the off-work reminder message, including the weather forecast.
        """
        try:
            forecast_info = self.weather_service.get_forecast()
        except Exception:
            return "<b>早该下班叻！</b>\n今天也辛苦了，请务必好好休息捏！(未能获取明日天气)"

        timezone = pytz.timezone(TIMEZONE)
        tomorrow = datetime.now(timezone).date() + timedelta(days=1)
        tomorrow_eight_am = timezone.localize(datetime.combine(tomorrow, time(hour=8)))
        target_ts = tomorrow_eight_am.timestamp()

        for forecast in forecast_info:
            if (
                abs(forecast["dt"] - target_ts) < 1800
            ):  # 寻找最接近早上8点的数据 (30分钟内)
                weather_type = forecast["weather"][0]["description"]
                feels_like = forecast["main"]["feels_like"]
                humidity = forecast["main"]["humidity"]
                return (
                    "<b>早该下班叻！</b>\n"
                    "只要一息尚存，我便坚持不懈。\n"
                    f"<b>明天早上 8 点的天气🌤️是{weather_type}，体感温度 {feels_like:.1f} ℃，湿度 {humidity:.0f} %</b>，"
                    "请群u注意捏！今天也辛苦了，请务必好好休息捏！"
                )

        return "<b>早该下班叻！</b>\n今天也辛苦了，请务必好好休息捏！(未能获取明日天气)"
