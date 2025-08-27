import requests
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler


def strip_blank(string):
    """去除字符串中的多余空格和换行符。"""
    # remove extra spaces and newlines from string
    return string.replace(" ", "").replace(",", ", ").replace("\n", " ")


def query_scholar(keyword):
    """在 Google Scholar 中查询并格式化结果。"""
    # query Google Scholar and format the results
    url = f"https://scholar.google.com/scholar?hl=zh-CN&q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all(class_="gs_ri")
        if not articles:
            return f"找不到关于“{keyword}”的学术结果。"

        result = "<b>在Google Scholar中的查询结果如下：</b>\n\n"
        count = 0
        for article in articles:
            if count >= 5:
                break
            if not (title_tag := article.find(class_="gs_rt")) or not title_tag.find(
                "a"
            ):
                continue

            count += 1
            title = title_tag.text
            author = article.find(class_="gs_a").text
            abstract = article.find(class_="gs_rs").text
            link = title_tag.find("a").get("href")
            result += (
                f"<b>{count}.</b> <b>Title:</b> {strip_blank(title).strip()}\n"
                f"        <b>Author:</b> {strip_blank(author).strip()}\n"
                f"        <b>Abstract:</b> {strip_blank(abstract).strip()}\n"
                f"        <b>Link:</b> {link.strip()}\n\n"
            )
        return result
    except requests.exceptions.RequestException as e:
        return f"查询学术文献失败: {e}"


def scholar_command(update, context):
    """处理 /scholar 命令。"""
    # handle /scholar command
    if not context.args:
        update.message.reply_text("请提供查询关键词。用法：/scholar <关键词>")
        return

    keyword = "+".join(context.args)
    result_text = query_scholar(keyword)
    update.message.reply_text(result_text, parse_mode="HTML")


def register(dispatcher):
    """注册 /scholar 命令处理器。"""
    # register /scholar command handler
    dispatcher.add_handler(CommandHandler("scholar", scholar_command))
