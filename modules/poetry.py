import time

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import *
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import re
import requests
from bs4 import BeautifulSoup

channal = Channel.current()



@channal.use(ListenerSchema(listening_events=[GroupMessage]))
async def shuazi(app:Ariadne,group:Group,message:MessageChain):
    if At(app.account) and '古诗' in message.display:
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51'
        }
        res=requests.get('http://api.tangdouz.com/poet/poet.php?return=text',headers=headers)
        if res.status_code == 200:
            time.sleep(1)
            await app.send_message(
                group,
                MessageChain(res.text.replace("\\r","\n"))
            )
        else:
            await app.send_message(
                group,
                MessageChain('输入信息有误')
            )
    elif '但丁神曲' in message.display:
        # await app.send_message(
        #     group,
        #     MessageChain(
        #         "1.序\n2.地狱篇（共34歌）\n3.炼狱篇（共33歌）\n4.天堂篇（共33歌）")
        # )
        if '序' in message.display:
            url = "https://www.zhonghuadiancang.com/waiguomingzhu/9681/" + str(197572) + ".html"
            res = requests.get(url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            p_tags = soup.findAll('p')
            content = "\n".join([p.get_text() for p in p_tags])
            time.sleep(1)
            await app.send_message(
                group,
                MessageChain(content.replace('但丁作品集','').replace('本站非营利性站点，以方便网友为主，仅供学习。','').strip())
            )
        if "地狱篇" in message.display:
            chapter = re.search("地狱篇(\d)", message.display).group(1)
            url = "https://www.zhonghuadiancang.com/waiguomingzhu/9681/" + str(197572 + int(chapter)) + ".html"
            res = requests.get(url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            p_tags = soup.findAll('p')
            content = "\n".join([p.get_text() for p in p_tags])
            time.sleep(1)
            await app.send_message(
                group,
                MessageChain(
                    content.replace('但丁作品集', '').replace('本站非营利性站点，以方便网友为主，仅供学习。', '').strip())
            )
        if "炼狱篇" in message.display:
            chapter = re.search("炼狱篇(\d)",message.display).group(1)
            url = "https://www.zhonghuadiancang.com/waiguomingzhu/9681/" + str(197606+int(chapter)) + ".html"
            res = requests.get(url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            p_tags = soup.findAll('p')
            content = "\n".join([p.get_text() for p in p_tags])
            time.sleep(1)
            await app.send_message(
                group,
                MessageChain(
                    content.replace('但丁作品集', '').replace('本站非营利性站点，以方便网友为主，仅供学习。', '').strip())
            )
        if "天堂篇" in message.display:
            chapter = re.search("炼狱篇(\d)", message.display).group(1)
            url = "https://www.zhonghuadiancang.com/waiguomingzhu/9681/" + str(197639 + int(chapter)) + ".html"
            res = requests.get(url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            p_tags = soup.findAll('p')
            content = "\n".join([p.get_text() for p in p_tags])
            time.sleep(1)
            await app.send_message(
                group,
                MessageChain(
                    content.replace('但丁作品集', '').replace('本站非营利性站点，以方便网友为主，仅供学习。', '').strip())
            )