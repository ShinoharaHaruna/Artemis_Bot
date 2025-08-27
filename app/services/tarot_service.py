import random
import yaml

POSITIVE = 0
REVERSE = 1


class TarotService:
    """
    塔罗牌服务，用于处理塔罗牌占卜相关逻辑。
    Tarot service for handling tarot divination logic.
    """

    def __init__(self, deck_path="app/data/tarot_deck.yaml"):
        """
        初始化塔罗牌服务并加载牌组数据。
        Initializes the Tarot service and loads the deck data.
        """
        self.deck = self._load_deck(deck_path)

    def _load_deck(self, path):
        """
        从 YAML 文件加载塔罗牌数据。
        Loads tarot deck data from a YAML file.
        """
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # In a real application, you might want to log this error
            # or handle it more gracefully.
            return []

    def draw_cards(self, num_cards=3):
        """
        抽取指定数量的塔罗牌，并随机确定正逆位。
        Draws a specified number of tarot cards and randomly determines if they are upright or reversed.
        """
        if not self.deck:
            return []

        cards = random.sample(self.deck, num_cards)
        results = []
        for card in cards:
            orientation = random.choice([POSITIVE, REVERSE])
            results.append({"card": card, "orientation": orientation})

        # 如果所有牌都是逆位，则重新抽牌
        # If all cards are reversed, redraw.
        if all(result["orientation"] == REVERSE for result in results):
            return self.draw_cards(num_cards)

        return results

    def create_interpretation_prompt(self, cards, topic=None):
        """
        为塔罗牌解读创建一个发送给 ChatGPT 的 prompt。
        Creates a prompt for ChatGPT to interpret the tarot reading.
        """
        prompt = "你是个专业的塔罗牌占卜师，"
        if topic:
            prompt += f"我正在对以下问题进行塔罗牌占卜：\n{topic}\n"
        else:
            prompt += "我正在进行塔罗牌占卜，并且已经想好了问题。\n"

        prompt += f"我抽了{len(cards)}张牌，得到结果如下：\n```\n"
        for item in cards:
            card_name = item["card"]["name"]
            orientation = "正位" if item["orientation"] == POSITIVE else "逆位"
            prompt += f"{card_name} ({orientation})\n"
        prompt += "```\n请结合牌意和我的问题，为我解读这次占卜的结果。"
        return prompt
