from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import re
import requests
import json

channal = Channel.current()



@channal.use(ListenerSchema(listening_events=[GroupMessage]))
async def shuazi(app:Ariadne,group:Group,message:MessageChain):
    if '翻译' in message.display:
        content=re.search('翻译：(.*)',message.display).group(1)
        res=requests.get(f'https://api.oioweb.cn/api/txt/QQFanyi?sourceText={content}')
        if res.status_code == 200:
            await app.send_message(
                group,
                MessageChain(res.json()["result"]["targetText"].strip(),f'\n{res.json()["result"]["source"].strip()}->{res.json()["result"]["target"].strip()}')
            )
        else:
            await app.send_message(
                group,
                MessageChain('输入信息有误')
            )