from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.event.mirai import NudgeEvent

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()
#
# @channel.use(ListenerSchema(listening_events=[GroupMessage,NudgeEvent]))
# async def who_calls_me(app:Ariadne,message:GroupMessage,)