from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def today_in_history(app: Ariadne, group: Group, message: MessageChain):