import random
from datetime import datetime
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.ariadne.message.element import At, Plain, Image, Forward, ForwardNode

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()

# @channel.use(ListenerSchema(listening_events=[GroupMessage],decorators=[MatchContent()]))
