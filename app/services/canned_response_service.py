import random
import yaml


class CannedResponseService:
    """
    提供预设回复的服务。
    Service for providing canned responses.
    """

    def __init__(self, data_path="app/data/canned_responses.yaml"):
        """
        初始化服务并加载回复数据。
        Initializes the service and loads the response data.
        """
        self.responses = self._load_responses(data_path)

    def _load_responses(self, path):
        """
        从 YAML 文件加载回复数据。
        Loads response data from a YAML file.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("responses", [])
        except FileNotFoundError:
            return []

    def get_random_response(self):
        """
        获取一个随机的预设回复。
        Gets a random canned response.
        """
        if not self.responses:
            return None
        return random.choice(self.responses)
