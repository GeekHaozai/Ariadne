from graia.ariadne.app import Ariadne
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend, Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()
# 只有在以下协议登录下该模块才能工作
# ANDROID_PHONE
# IPAD
# MACOS
@channel.use(ListenerSchema(listening_events=[NudgeEvent]))
async def nudge_listener(app: Ariadne, event: NudgeEvent):
    if isinstance(event.subject, Group) or isinstance((event.subject,Friend)) and event.supplicant is not None:
        print(f"[INFO] 收到{event.supplicant}的戳一戳")
        await app.send_group_message(event.supplicant, MessageChain("干嘛~戳疼我了！"))
