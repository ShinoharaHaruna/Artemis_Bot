import random
import yaml


class AnswerbookService:
    """
    答案之书服务，用于提供随机答案。
    Service for the Answer Book, providing random answers.
    """

    def __init__(self, data_path="app/data/answerbook.yaml"):
        """
        初始化答案之书服务并加载答案数据。
        Initializes the Answerbook service and loads the answers data.
        """
        self.answers = self._load_answers(data_path)

    def _load_answers(self, path):
        """
        从 YAML 文件加载答案数据。
        Loads answers data from a YAML file.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("answers", [])
        except FileNotFoundError:
            return []

    def get_random_answer(self):
        """
        获取一个随机答案。
        Gets a random answer.
        """
        if not self.answers:
            return "答案之书暂时无法回应。"
        return random.choice(self.answers)
