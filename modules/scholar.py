import requests
from bs4 import BeautifulSoup


def strip_blank(string):
    return string.replace(" ", "").replace(",", ", ").replace("\n", " ")


def query(keyword):
    url = "https://scholar.google.com/scholar?hl=zh-CN&q={}".format(keyword)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # pages = soup.find_all(id="gs_nml")    # 以后用得上
    articles = soup.find_all(class_="gs_ri")
    result = "<b>在Google Scholar中的查询结果如下：</b>\n\n"
    i = 0
    for article in articles:
        if i >= 5:
            break
        if article.find(class_="gs_rt").find("a") == None:
            continue
        i = i + 1
        title = article.find(class_="gs_rt").text
        author = article.find(class_="gs_a").text
        abstract = article.find(class_="gs_rs").text
        link = article.find(class_="gs_rt").find("a").get("href")
        result += "<b>{}.</b>     <b>Title:</b> {}\n        <b>Author:</b> {}\n        <b>Abstract:</b> {}\n        <b>Link:</b> {}\n\n".format(
            i,
            title.replace("\n", " ").strip(),
            author.replace("\n", " ").strip(),
            abstract.replace("\n", " ").strip(),
            link.strip(),
        )
    return result


def handle_scholar_query(bot, chat_id, message):
    bot.send_message(
        chat_id=chat_id,
        text=query(message),
        parse_mode="HTML",
    )


def scholar_command(update, context):
    handle_scholar_query(context.bot, update.effective_chat.id, "+".join(context.args))
