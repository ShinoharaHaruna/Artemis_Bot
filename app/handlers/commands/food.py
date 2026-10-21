import urllib.parse as urlparse

import requests
from bs4 import BeautifulSoup, Tag
from telegram.ext import CommandHandler


def strip_blank(string):
    """去除字符串中的空格和换行符。"""
    # remove blank and new line characters from string
    return string.replace(" ", "").replace(",", ", ").replace("\n", " ")


def get_food_info(keyword):
    """从 fatsecret.cn 获取食物信息。"""
    # get food info from fatsecret.cn
    base_url = "https://www.fatsecret.cn"
    url = f"https://www.fatsecret.cn/%E7%83%AD%E9%87%8F%E8%90%A5%E5%85%BB/search?q={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
    except requests.exceptions.RequestException:
        # 网络请求失败时返回空结果 / Return empty result on network failure
        return None, None, None
    soup = BeautifulSoup(response.text, "html.parser")
    most_match = soup.find_all("td", class_="borderBottom")
    if not most_match:
        return None, None, None

    first_match = most_match[0]
    match_link = first_match.find("a") if isinstance(first_match, Tag) else None
    if not isinstance(match_link, Tag) or not match_link.get("href"):
        # 未找到匹配的链接时返回空结果 / Return empty result when no link found
        return None, None, None
    food_name = match_link.text
    food_url = base_url + str(match_link["href"])
    try:
        response = requests.get(food_url, headers=headers, timeout=15)
    except requests.exceptions.RequestException:
        # 网络请求失败时返回空结果 / Return empty result on network failure
        return None, None, None
    soup = BeautifulSoup(response.text, "html.parser")
    nut_summary_soup = soup.find_all("div", class_="factPanel")
    if not nut_summary_soup:
        # 未找到营养摘要面板时返回空结果 / Return empty result when summary panel missing
        return None, None, None
    panel = nut_summary_soup[0]
    if not isinstance(panel, Tag):
        # 营养摘要面板类型异常时返回空结果 / Return empty result on unexpected panel type
        return None, None, None
    nut_summary_table = panel.find_all("table")
    summary_table = nut_summary_table[0] if nut_summary_table else None
    if not isinstance(summary_table, Tag):
        # 未找到营养摘要表格时返回空结果 / Return empty result when summary table missing
        return None, None, None
    tds = summary_table.find_all("td")
    tds = [td for td in tds if isinstance(td, Tag) and td.text]
    summary = {"food_name": food_name, "food_url": food_url}
    for i in range(0, len(tds)):
        parts = tds[i].text.split("\n")
        if len(parts) < 3:
            # 跳过格式不完整的单元格 / Skip cells with incomplete format
            continue
        item, value = parts[1], parts[2]
        summary[item] = value
    description_soup = panel.find_all("table", class_="generic spaced")
    desc_table = description_soup[1] if len(description_soup) > 1 else None
    if not isinstance(desc_table, Tag):
        # 未找到描述表格时返回空结果 / Return empty result when description table missing
        return None, None, None
    description_tds = [
        td for td in desc_table.find_all("td") if isinstance(td, Tag)
    ]
    if len(description_tds) < 2:
        # 未找到描述单元格时返回空结果 / Return empty result when description cells missing
        return None, None, None
    food_description = description_tds[0].text
    calorie_description = description_tds[1].text.replace("热量分解：", "")
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
