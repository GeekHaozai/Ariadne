# from claude_api import Client
# import requests
# import time
# from graia.ariadne.app import Ariadne
# from graia.ariadne.event.message import GroupMessage
# from graia.ariadne.message.chain import MessageChain
# from graia.ariadne.message.element import *
# from graia.ariadne.model import Group
#
# from graia.saya import Channel
# from graia.saya.builtins.broadcast.schema import ListenerSchema
#
# cookie = "sessionKey=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; intercom-device-id-lupk8zyo=535ba67e-db82-4f2a-99f8-adba2a926ad2; __cf_bm=WZ6zRqNzsJIfI6YjnVFOhaclELpYfayli2dhmkmvOSk-1690888918-0-AS5c4u+LT3wLyfMgB/01pRcL+nhnLof2CG2PWEYnXwTbeYN7Ak6oSPowL5YgL5uoJVZ7pEW3UPU6k919iDhtyrc=; intercom-session-lupk8zyo=TE9LcjU5MnZmM3puL0h5WDJDeGZqZ3N1ajcrTnJvemlQaWlqd1VEbzd2d0liQTZ3ckVHdlNkeVhEbEhrS3FUUS0tSFI1dUhCZlVRSnEvQjlhWndxbldUQT09--7dc77ce55d5ddfb0a1eab163b6653fbaa6b8eb3f"
# claude_api = Client(cookie)
# new_chat = claude_api.create_new_chat()
# new_chat_id = new_chat["uuid"]
#
# channal = Channel.current()
#
# @channal.use(ListenerSchema(listening_events=[GroupMessage]))
# async def chat_claude(app:Ariadne,group:Group,message:MessageChain):
#     if At(app.account) in message:
#         time.sleep(1)
#         content = message.replace(str(At(app.account)),"")
#         response = claude_api.send_message(content,new_chat_id)
#         await app.send_message(
#             group,
#             MessageChain("对话ID:\n",new_chat_id,"\n",response)
#         )
#
