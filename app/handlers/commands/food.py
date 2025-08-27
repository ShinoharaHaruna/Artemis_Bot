import requests
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler


def strip_blank(string):
    """去除字符串中的空格和换行符。"""
    # remove blank and new line characters from string
    return string.replace(" ", "").replace(",", ", ").replace("\n", " ")


def get_food_info(keyword):
    """从 fatsecret.cn 获取食物信息。"""
    # get food info from fatsecret.cn
    base_url = "https://www.fatsecret.cn"
    url = "https://www.fatsecret.cn/%E7%83%AD%E9%87%8F%E8%90%A5%E5%85%BB/search?q={}".format(
        keyword
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    most_match = soup.find_all("td", class_="borderBottom")
    if not most_match:
        return None, None, None

    food_name = most_match[0].find("a").text
    food_url = base_url + most_match[0].find("a")["href"]
    response = requests.get(food_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    nut_summary_soup = soup.find_all("div", class_="factPanel")
    nut_summary_table = nut_summary_soup[0].find_all("table")
    tds = nut_summary_table[0].find_all("td")
    tds = [td for td in tds if td.text]
    summary = {"food_name": food_name, "food_url": food_url}
    for i in range(0, len(tds)):
        item, value = tds[i].text.split("\n")[1], tds[i].text.split("\n")[2]
        summary[item] = value
    description_soup = nut_summary_soup[0].find_all("table", class_="generic spaced")
    food_description = description_soup[1].find_all("td")[0].text
    calorie_description = (
        description_soup[1].find_all("td")[1].text.replace("热量分解：", "")
    )
    return (
        summary,
        strip_blank(food_description).strip(),
        strip_blank(calorie_description).strip(),
    )


def handle_basic_info(
    bot, chat_id, message_id, summary, food_description, calorie_description
):
    """处理基本信息并发送。"""
    # handle basic info and send
    mass_info = ""
    for t in summary:
        if "克" in summary[t]:
            mass_info += f"\n        {t}: {summary[t]}"
    mass_info += "\n"

    text_html = f"""<b>食物名称</b>: {summary['food_name']}
<b>食物描述</b>: {food_description}
<b>热量分布</b>: {calorie_description}
<b>营养摘要</b>: {mass_info}
<b>详细信息链接</b>: {summary['food_url']}
"""
    bot.send_message(
        chat_id=chat_id,
        text=text_html,
        parse_mode="HTML",
        reply_to_message_id=message_id,
    )


def food_command(update, context):
    """处理 /food 命令。"""
    # handle /food command
    if not context.args:
        update.message.reply_text("请提供食物名称。用法：/food <食物名称>")
        return
    keyword = " ".join(context.args)
    summary, food_description, calorie_description = get_food_info(
        urlparse.quote(keyword, safe="")
    )
    if not summary:
        update.message.reply_text(f"找不到关于“{keyword}”的信息。")
        return

    handle_basic_info(
        context.bot,
        update.effective_chat.id,
        update.message.message_id,
        summary,
        food_description,
        calorie_description,
    )


def register(dispatcher):
    """注册 /food 命令处理器。"""
    # register /food command handler
    dispatcher.add_handler(CommandHandler("food", food_command))
