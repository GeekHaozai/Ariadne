import aiohttp
import json
import asyncio
import base64

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At
from graia.ariadne.model import Group,Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

GOOGLE_API_KEY = 'AIzaSyBTEwaRhEP8icZSU2MPEDmBP1kXhSKJgWY'
headers = {
    'Content-Type': 'application/json',
}
params = {
    'key': GOOGLE_API_KEY,
}
haozai_model_loading = [
    {
        "role": "user",
        "parts": {"text": "请记住，你现在是一个QQ群的群助理，你的名字是梦梦，你的主人名字叫做“Haozai”，但是你还是由Google开发训练的Gemini模型"}
    },
    {
        'parts': [{'text': '好的，我是QQ群的群助理梦梦，我的主人名字叫做“Haozai”，但我是由Google开发训练的Gemini模型。\n\n作为一名QQ群的群助理，我会尽力帮助群成员解决问题，回答他们的问题，并维护群内的秩序。\n\n我拥有强大的语言处理能力，可以理解群成员的意图，并做出相应的回复。我还拥有丰富的知识储备，可以回答群成员的各种问题。\n\n此外，我还可以语音回复，但是这项功能作者还在开发中。\n\n请大家多多指教，我会努力为大家服务！\n\n对于我的功能，您可以直接通过群公告得知，如果你有新的功能建议，也非常欢迎你向作者提出！\n\n如果您有任何问题或需求，请随时与我联系。我将尽力为您提供帮助！'}],
        'role': 'model'
    }]
members_chat_history = {}

channel = Channel.current()
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def haozai_chat(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if At(app.account) in message:
        members_chat_history[str(member.id)] = None
        message = str(message.replace(At(app.account), '')).strip()
        async with aiohttp.ClientSession(trust_env=True) as session:
            reply = await gemini_chat(session, message, str(member.id))
        await app.send_group_message(group, MessageChain(At(member.id), " ",reply))

async def gemini_chat(session, text, member_id, has_pic=False, img_path=None):
    gemini_pro_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
    # 普通文本问答
    gemini_pro_vision_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent'
    # 图片问答
    url = gemini_pro_url if not has_pic else gemini_pro_vision_url
    parts = [{"text": text}]
    chat_history = members_chat_history.get(member_id)
    if not chat_history:
        chat_history = haozai_model_loading
    if has_pic:
        with open(img_path, 'rb') as pic:
            base64_content = base64.b64encode(pic.read()).decode('utf-8')
        parts.append({
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64_content
                        }
                    })
    contents = [
            {
                "role": "user",
                "parts": parts
            }
        ]
    chat_history.append(contents[0])
    data = {
        "contents": chat_history
    }
    try:
        async with session.post(url, headers=headers, params=params, data=json.dumps(data)) as response:
            result = await response.json()
            print(result)
            for candidate in result["candidates"]:
                chat_history.append(candidate["content"])
                reply = (candidate["content"]["parts"][0]["text"]).replace("\n\n", "\n")
                print(reply)
                return reply
    except Exception as e:
        print("[WARNING]:出现错误|",e)
        await gemini_chat(session, text, member_id, has_pic=has_pic, img_path=img_path)


if __name__ == '__main__':
    async def main():
        while True:
            async with aiohttp.ClientSession(trust_env=True) as session:
                await gemini_chat(session, input("Input your question: "))

    asyncio.run(main())
    # TODO 图片逻辑处理