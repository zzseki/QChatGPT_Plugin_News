from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import * # 导入事件类
import re
import httpx
import requests
from mirai import Image, MessageChain,Plain


# 注册插件
@register(name="News", description="Get News", version="0.1", author="zzseki")
class GetNewsPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.token = "YOUR_COOKIE"  # 请将这里的'YOUR_TOKEN'替换为你实际获取的token


    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        receive_text = ctx.event.text_message
        NEWS_PATTERN_1 = re.compile(r"新闻")
        NEWS_PATTERN_2 = re.compile(r"热点")
        if NEWS_PATTERN_1.search(receive_text) or NEWS_PATTERN_2.search(receive_text):
            url = await self.get_news()
            if url:
                ctx.add_return("reply", [Image(url = url)])
                self.ap.logger.info(url)
                ctx.prevent_default()




    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_Normal_message_received(self, ctx: EventContext):
        receive_text = ctx.event.text_message
        NEWS_PATTERN_1 = re.compile(r"新闻")
        NEWS_PATTERN_2 = re.compile(r"热点")
        if NEWS_PATTERN_1.search(receive_text) or NEWS_PATTERN_2.search(receive_text):
            url = await self.get_news()
            if url:
                ctx.add_return("reply", [Image(url=url)])
                self.ap.logger.info(url)
                ctx.prevent_default()



    async def get_news(self):
        url = "https://v2.alapi.cn/api/zaobao"
        params = {
            "format": "json",
            "token": self.token,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()["data"]
            url = data["image"]
            return url




    # 插件卸载时触发
    def __del__(self):
        pass
