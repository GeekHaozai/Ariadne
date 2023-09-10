from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.ariadne.event.mirai import NudgeEvent

channnel = Channel.current()

@channnel.use(ListenerSchema(listening_events=[NudgeEvent]))
async def chuochuo(app:Ariadne,event:NudgeEvent):
    match event.context_type:
        case "group":
            await app.send_group_message(
                event.group_id,
                MessageChain("你戳什么戳，戳疼我了！")
            )
        case "friend":
            await app.send_friend_message(
                event.friend_id,
                MessageChain("戳我是不是喜欢我~")
            )
        case _:
            return
