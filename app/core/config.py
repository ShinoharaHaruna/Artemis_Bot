import yaml


def load_config():
    """
    从 config.yaml 加载配置。
    Load configuration from config.yaml.
    """
    with open("config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


# 加载配置 / Load configuration
config = load_config()

# 从配置中提取常量 / Extract constants from configuration
API_TOKEN = config["Basic"]["API_TOKEN"]
MASTER_ID = config["Basic"]["MASTER_ID"]
TIMEZONE = config["Basic"]["TIMEZONE"]
GROUP_CHAT_ID = config["GroupChat"][0][0]

OPENAI_API_KEY = config["OpenAI"]["OPENAI_API_KEY"]

WEATHER_API_KEY = config["Weather"]["API_KEY"]
WEATHER_LAT = config["Weather"]["LAT"]
WEATHER_LON = config["Weather"]["LON"]
