<p align="center">
    <img src="https://s2.loli.net/2023/11/27/Y7vrmTKx2GQeOHk.png" width="200" height="200">
</p>
<div align="center">

# Artemis Bot

一个使用`Python`开发的Telegram群组机器人罢了。

</div>
<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="python" />
    <img src="https://img.shields.io/badge/Telegram-26A5E4.svg?style=for-the-badge&logo=Telegram&logoColor=white" alt="telegram" />
    <img src="https://img.shields.io/badge/OpenAI-412991.svg?style=for-the-badge&logo=OpenAI&logoColor=white" alt="openai" />
</p>

## 简介

早就想给和朋友们组的telegram群组加个bot了，可惜实在太忙了。最开始只是想做一个提醒喝水bot，直接原因是数媒早八课真的无聊，于是花了一节课的时间写了个。

~~因为真的很简单所以我觉得是个人都能指点一番我就不费力解释代码了。~~

另外，没有使用v20的新API，总之就是老版顺手，就拿来用了，如果要`pip install`的话记得指定版本。

> Update @ 2025-08-28：诈尸更新，之前土法手搓 Python 的代码确实很丑，现在狠狠重构了 😎

## 人设

其实也没什么人设，直接搬Wikipedia：

> 阿耳忒弥斯（古希腊语：Ἄρτεμις；拉丁语：Artemis；也译阿尔忒弥斯）对应神是罗马神话中的狄阿娜（拉丁语：Diana），是古希腊神话中象征纯洁的女神，奥林匹斯十二主神之一。她是众神之王宙斯和女神勒托的女儿，也是太阳神阿波罗的双胞胎姐姐。阿尔忒弥斯主要被认为是月亮的守护女神。

至于为什么是这个神明，这和群的名称有关（

人设图/头图是`DALL-E 2`生成的，可爱滴捏。

## 技能

1. **喝水提醒**
    月神会在每天的以下时间提醒大家喝水：
    08:50, 09:50, 11:00, 12:30, 14:50, 15:50, 17:00, 18:30, 20:50

2. **下班提醒**
    月神会在工作日晚上 22:30 提醒大家下班，并给出明天早上 8 点的天气情况。

3. **聊天功能**
    月神可以和大家聊天哦！只需要在群组中输入`/chat`+你想说的话，月神就会回复你啦！
    例如：`/chat 你好呀！`

4. **生成图片**
    月神可以根据你输入的文字生成图片哦！只需要在群组中输入`/draw`+你想说的话，月神就会生成图片并发送给你啦！

5. **天气查询**
    月神可以查询你的天气哦！只需要在群组中输入`/weather`，月神就会发送今日的天气情况给你啦！

6. **未来天气查询**
    月神可以查询你明早早八的天气哦！只需要在群组中输入`/forecast`，月神就会发送给你啦！

7. **随机 Pixiv 图片**
    月神可以发送随机的 Pixiv 图片哦！只需要在群组中输入`/random_pixiv`，月神就会发送给你啦！

8. **一言**
    月神可以给你一句箴言哦！只需要在群组中`@月神`+“你怎么看”，月神就会发送给你啦！

9. **答案之书**
    月神可以赐你回答！在群组中输入`/answer`，跟上你的问题，月神就会给你答案！

10. **学术查询**
    月神可以帮你在 Google Scholar 中查询哦！只需要在群组中输入`/scholar`+你想查询的内容，月神就会发送给你啦！
    例如：`/scholar 月神`

11. **营养查询**
    月神可以帮你在 FatSecret 中查询哦！只需要在群组中输入`/food`+你想查询的内容，月神就会发送给你啦！

12. **塔罗占卜**
    月神可以帮你进行塔罗占卜哦！只需要在群组中输入`/tarot`，后面可以选择跟上你想问的话题，月神就会为你用塔罗牌占卜！
    例如：`/tarot 我想知道我明天的运势`

13. **设置提醒**
    月神可以帮你设置提醒哦！只需要在私聊中输入`/reminder YYYYMMDDHHMM <提醒内容>`，月神就会在指定时间提醒你！
    例如：`/reminder 202508281930 去看电影`

## 致谢

答案之书的字典来源：<https://github.com/D1N910/answers-of-my-life>

学术功能来自Google Scholar：<https://scholar.google.com/>

食物营养数据来自fatsecret：<https://www.fatsecret.cn/>

塔罗牌牌面数据来源：<https://github.com/jeremytarling/python-tarot>

---

以及我的朋友们。I love you all.
