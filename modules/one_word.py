import requests


def get_one_word():
    url = "https://v1.hitokoto.cn/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "}
    response = requests.get(url, headers=headers)
    response_json = response.json()
    return response_json["hitokoto"]
