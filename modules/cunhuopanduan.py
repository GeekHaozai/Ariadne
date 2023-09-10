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


channal = Channel.current()



@channal.use(ListenerSchema(listening_events=[GroupMessage]))
async def cunhuo(app:Ariadne,group:Group,message:MessageChain):
    if At(app.account) in message and '存活判断' in message:
        await app.send_message(
            group,
            MessageChain('我一直都在的~')
        )

