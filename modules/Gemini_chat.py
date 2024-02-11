import aiohttp
import json
import asyncio
import base64
import aiofiles

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At,Image
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
        "parts": {"text": "请记住，你现在是一个全知的神，你的名字是梦梦，你的主人名字叫做“Haozai”，但是你还是由Google开发训练的Gemini模型"}
    },
    {
        'parts': [{'text': """好的，我会记住。
我是梦梦，一个全知的神。 我的主人叫做“Haozai”，但实际上我是由 Google 开发训练的 Gemini 模型。
我可以访问和处理来自现实世界的信息，并使用我的知识来回答您的问题，完成您的请求，并帮助您实现您的目标。"""}],
        'role': 'model'
    }]
members_chat_history = {}
reply_lock = asyncio.Lock()
pic_lock = asyncio.Lock()

channel = Channel.current()
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def haozai_chat(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if At(app.account) in message:
        members_chat_history[str(member.id)] = None
        imgs = message[Image]
        has_pic = True if imgs else False
        img_paths = []
        for img in imgs:
            each_url = img.url
            each_id = img.id
            print("[INFO]:图片信息| ",each_url,each_id)
            img_paths.append(f"modules\\pics\\{each_id}")
            async with pic_lock:
                async with aiohttp.ClientSession() as session:
                    async with session.get(each_url) as response:
                        async with aiofiles.open(f"modules\\pics\\{each_id}","wb") as f:
                            await f.write(await response.read())
        message = str(message.replace(At(app.account), '')).strip()
        async with aiohttp.ClientSession(trust_env=True) as session:
            reply = await gemini_chat(session, message, str(member.id),img_paths=img_paths,has_pic=has_pic)
        await app.send_group_message(group, MessageChain(At(member.id), " ",reply))

async def gemini_chat(session, text, member_id, has_pic=False, img_paths=None):
    async with reply_lock:
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
            async with pic_lock:
                for img_path in img_paths:
                    async with aiofiles.open(img_path, 'rb') as pic:
                        base64_content = base64.b64encode(await pic.read()).decode('utf-8')
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
        data = {"contents": contents} if has_pic else {"contents": chat_history}
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
            await gemini_chat(session, text, member_id, has_pic=has_pic, img_paths=img_paths)


if __name__ == '__main__':
    async def main():
        while True:
            async with aiohttp.ClientSession(trust_env=True) as session:
                await gemini_chat(session, input("Input your question: "), "test_id")

    asyncio.run(main())
    # TODO 涩图api处理逻辑
    # TODO 超出对话TOKEN处理
    # TODO AI 绘画功能
    # TODO 超过每分钟对话频率限制

