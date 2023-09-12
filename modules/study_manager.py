import re

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()
member_data = []

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def manage(app:Ariadne,group:Group,message:MessageChain):
    if At(app.account) and '今日任务布置' in message.display:
        id = re.search(r'编号(\d+)',message.display).group(1)
        task = message.display.replace('今日任务布置','').replace('@'+str(app.account),'').strip()
        member_data.append([id,task])
        await app.send_message(group,MessageChain([Plain(f'任务编号{id}布置成功！')]))
    if At(app.account) and "查看今日任务" in message.display:
        for i in member_data:
            await app.send_message(group,MessageChain([Plain(f'{i}')]))
    if At(app.account) and "删除今日任务" in message.display:
        id = re.search(r'编号(\d+)',message.display).group(1)
        member_data.remove([id-1])
        await app.send_message(group,MessageChain([Plain(f'编号{id-1}删除成功！')]))
