from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
import requests
import re
channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def today_in_history(app: Ariadne, group: Group, message: MessageChain):
    if "历史上的今天" in message.display:
        r = requests.get("https://api.oioweb.cn/api/common/history")
        if r.status_code == 200 and r.json()["code"]==200:
            message_list = []
            index = 1
            for i in r.json()["result"]:
                year = i["year"].replace("-","公元前").strip()+"年"
                title = i["title"].strip()
                title = re.sub(r"<.*?>","",title)
                desc = i["desc"].strip()
                desc = re.sub(r"<.*?>","",desc)
                message_list.append(f"{index}.{year} {title}\n{desc}")
                index += 1
            await app.send_group_message(group, MessageChain("\n".join(message_list)))
        else:
            await app.send_group_message(group, MessageChain("获取历史上的今天信息失败了QAQ"))