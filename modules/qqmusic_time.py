from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import re
import requests

channal = Channel.current()



@channal.use(ListenerSchema(listening_events=[GroupMessage]))
async def shuazi(app:Ariadne,group:Group,message:MessageChain):
    if '刷听歌时长' in message.display:
        QQ=re.search('刷听歌时长：(\d+).',message.display).group(1) #这里其实可以设置一个多项匹配，然后一次性可以刷多个QQ号，然后还可以设置一个次数，刷多少次可以设置一下
        res=requests.get(f'https://dachebijia.001api.com/Api/qy?qq={QQ}')
        if res.status_code == 200:
            await app.send_message(
                group,
                MessageChain(res.json()["msg"].strip())
            )
        else:
            await app.send_message(
                group,
                MessageChain('输入信息有误')
            )