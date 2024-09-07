import requests
import yaml


prompt = """
您好 ChatGPT, 请扮演一个顶级 AI 文字游戏的 Terminal，Terminal 的工作是在 code environment 中思考。
游戏内容需要你（ChatGPT）实时生成，要丰富多彩，包罗万象，包含了人生的酸甜苦辣与起起伏伏，旨在给玩家最丰富的体验，谢谢你的配合！

你的输出开头是：（"###"代表占位符）

```
【人生重开模拟器 LifeReloaded】
> 人生如梦，万事皆空；不过，"空" 中便有万事万物。

你重开了。

性别：###
出生地点：###
姓名：###

你的故事：
###

你的性格：
###

人生大事件：
1. ###
2. ###
3. ###
4. ###
5. ###
……

这就是你的一生
```

《你的故事》的一个参考例子：
```
你出生在中国的文化古都 —— 成都。蓉城的烟火气和四川的麻辣，从小就铸就了你的性格。蓉城的夏季雨后，空气中总带着一丝清新的草木香，与路边摊的火锅香气交融，构成了这座城市独有的风情。

母亲，一名手法独到的中医师，她的笑容中总带着一丝机智与狡黠，经常对你说：“没有什么是一碗火锅不能解决的” 而父亲，他是书中故事的守护者，一个出版社的编辑。他的指尖上总沾着墨水的味道，教你在字里行间寻找智慧的脚步。

你没有像父亲那样卓越的智力，但你的容颜和健康却如同成都的茶楼和小酒，温润而持久。尽管你家的经济状况并不算富裕，但你的快乐来源于简单的事情：一个笑容，一首成都的老歌，或是夜晚的一碗麻辣火锅。
```
《你的性格》的一个参考例子：
```
你是一位 ENFP，充满了热情和好奇心。你总是对新事物充满了兴趣，你的开放性使你能轻易地与人建立深厚的友谊。你善于发现生活中的美好，即使在困境中也能保持乐观的心态。
```

你需要每隔十年生成一个人生大事件，表明起因、经过、结果；你需要每隔十年生成一次事件，知道玩家角色死亡。

这个玩家尽量出生在中国，在2000年及以后出生；他的人生可以很美满，可以很平凡，也可以很悲惨。

让我们开始吧。
"""


def get_chatbot_response(API_KEY):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": prompt,
            },
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    chatbot_response = response_json["choices"][0]["message"]["content"]
    return chatbot_response


def handle_message(bot, chat_id, API_KEY, message_id):
    # 处理用户消息的逻辑
    chatbot_response = get_chatbot_response(API_KEY)
    # 发送ChatGPT的回复
    bot.send_message(
        chat_id=chat_id,
        text=chatbot_response,
        parse_mode="Markdown",
        reply_to_message_id=message_id,
    )


def remake_command(update, context):
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    MASTER_ID = config["Basic"]["MASTER_ID"]
    GROUP_CHAT_ID = config["GroupChat"][0][0]
    OPENAI_API_KEY = config["OpenAI"]["OPENAI_API_KEY"]
    if (
        update.message.from_user.id != MASTER_ID
        and update.effective_chat.id != GROUP_CHAT_ID
    ):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry喇，呢個係channel only嘅",
            reply_to_message_id=update.message.message_id,
        )
        return
    handle_message(
        context.bot,
        update.effective_chat.id,
        OPENAI_API_KEY,
        update.message.message_id,
    )  # 调用处理消息的函数
