from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from datetime import datetime
import random


channel = Channel.current()

@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchContent("好大的奶")],
    )
)
async def create_forward(app: Ariadne, group: Group, member: Member):
    fwd_nodeList = [
        ForwardNode(
            target=member,
            time=datetime.now(),
            message=MessageChain(Image(path=r"C:\Users\DELL123\Desktop\日常\公众号.jpg")),
        )
    ]
    member_list = await app.get_member_list(group)
    for _ in range(3):
        random_member: Member = random.choice(member_list)
        fwd_nodeList.append(
            ForwardNode(
                target=random_member,
                time=datetime.now(),
                message=MessageChain("好大的奶"),
            )
        )
    message = MessageChain(Forward(nodeList=fwd_nodeList))
    await app.send_message(group, message)