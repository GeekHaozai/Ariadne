import random
import time

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.ariadne.event.mirai import NudgeEvent

# channnel = Channel.current()
#
# @channnel.use(ListenerSchema(listening_events=[GroupMessage]))
# async def setu(app:Ariadne,group:Group,message:MessageChain):
#     if (str(At(app.account)) in message.display) and ('美女图片' in message.display):
#         time.sleep(2.5)
#         await app.send_message(
#             group,
#             MessageChain(Image(path=fr"C:\Users\DELL123\Desktop\study\爬虫项目\每日一练\7.11\爬取的知乎图片\{random.randint(1,85)}.jpg"))
#         )
#     elif (str(At(app.account)) in message.display) and ("帅哥图片" in message.display):
#         await app.send_message(
#             group,
#             MessageChain(Image(
#                 path=fr"C:\Users\DELL123\Desktop\study\爬虫项目\每日一练\7.11\爬取的知乎图片\-5781cbb24b920967.jpg"))
#         )
