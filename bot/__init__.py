from telethon import events,functions,errors,Button
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import Config
import asyncio
import threading
import re
from urllib.parse import quote
w = dict()
v = dict()
import time

client = TelegramClient(
            StringSession(),
            Config.API_ID,
            Config.API_HASH,
            # proxy=("socks5","127.0.0.1",9050)
            ).start(bot_token=Config.TOKEN)

username_bot = client.get_me().username

def get_file_name(message):
    if message.file.name:
        return quote(message.file.name)
    ext = message.file.ext or ""
    return f"file{ext}"

join = [Button.url('💠عضویت در کانال💠', f'https://t.me/{Config.CHANNEL_USERNAME}')]
@client.on(events.NewMessage(incoming=True))
async def download(event):
    if (pv := event.is_private) or event.is_group :
        if event.sender_id in w.keys():
            if w[event.sender_id] > time.time() - 1 :
                await event.reply(f"⛔️امکان ارسال همزمان چند فایل وجود ندارد⛔️")
                return
        w[event.sender_id] = time.time()
        if pv:
            try:
                    user = await event.client(functions.channels.GetParticipantRequest(
                    channel = Config.CHANNEL_USERNAME,
                    participant = event.sender_id
                    ))
            except errors.UserNotParticipantError:
                    await client.send_message(event.chat_id,"📛 برای حمایت از ما و همچنان ربات ابتدا در کانال ما عضو شوید.\n\n✅ پس از عضویت وارد ربات شده و دستور /start را ارسال کنید.", buttons=join)
                    return

            if event.file :
                if not pv :
                    if not event.file.size > 10_000_000:
                        return 
                sender = await event.get_sender()
                msg = await event.client.send_file(
                    Config.CHANNEL,
                    file=event.message.media,
                    caption=f"🔆یک فایل جدید ارسال شد\n\n🔸User ID : [{event.chat_id}](tg://user?id={event.sender_id})\n\n🆔 @{Config.CHANNEL_USERNAME}",buttons=[
    [Button.url('👤User', f'https://t.me/{sender.username}'),Button.url('Bot🔰', f't.me/{username_bot}')]
])
                id_hex = hex(msg.id)[2:]
                id = f"{id_hex}/@{Config.CHANNEL_USERNAME}-{get_file_name(msg)}"
                bot_url = f"[share](t.me/{username_bot}?start={id_hex})"
                await client.send_message(event.chat_id,f"♻️فایل شما با موفقیت به لینک تبدیل شد\n\n💢File Name: {get_file_name(msg)}\n\nℹ️File ID: {id_hex}\n\n☣️File Link: `{Config.DOMAIN}/{id}`\n\n⚠️لینک دانلود نیم بها میباشد، قبل از دانلود VPN خود را خاموش کنید!\n\n🆔 @{Config.CHANNEL_USERNAME}",buttons=[
    [Button.url('دانلود🌐', f'{Config.DOMAIN}/{id}'),Button.url('⚡️دونیت', 'https://www.payping.ir/d/WiZG')]
],parse_mode='md')
                return
        
            elif id_msg := re.search("/start (.*)", event.raw_text ):
                try :
                    if id_hex := id_msg.group(1) :
                        try:
                            id = int(id_hex,16)
                        except ValueError:
                            return
                        msg = await event.client.get_messages(Config.CHANNEL,ids=id)
                        if not msg or not msg.file :
                            return await event.reply("404! File Not Found")
                        if regex := re.search(r"(\d*)/(\d*)",msg.message):
                            if regex.group(1) :
                                user_id = int(regex.group(1))
                                if "100" in regex.group(1):
                                    user_id = int("-"+regex.group(1))
                                msg_id = int(regex.group(2))
                                file = await event.client.get_messages(user_id,ids=msg_id)
                                if not file or not file.file :
                                    return await event.reply("404! File Not Found")
                                forward = await file.forward_to(event.chat_id)
                                id_name = f"{id_hex}/{get_file_name(msg)}"
                                bot_url = f"[share](t.me/{username_bot}?start={id_hex})"
                                forward_reply = await forward.reply(f"will be deleted in 21 seconds. \n\n📎 : [Link]({Config.DOMAIN}/{id_name})\n🤖 : {bot_url}",link_preview=False)
                                await asyncio.sleep(12)
                                await forward_reply.edit(f"will be deleted in 10 seconds. \n\n📎 : [Link]({Config.DOMAIN}/{id_name})\n🤖 : {bot_url}")
                                await asyncio.sleep(10)
                                await forward.delete()
                                await forward_reply.edit(f"📎 : [Link]({Config.DOMAIN}/{id_name})\n🤖 : {bot_url}",link_preview=True)
                        return
                except:
                    return await event.reply("404! فایل یافت نشد")
            
            if pv:
                if event.raw_text == "/start":
                        await client.send_message(event.chat_id,f"⚡️خوش آمدید\n\n💥برای استفاده از ربات کافی است فایل خود را ارسال کرده و سپس لینک آن را دریافت کنید.\n\n🆔 @{Config.CHANNEL_USERNAME}", buttons=[
                                    [Button.text('پشتیبانی💠', resize=True),Button.text('💰حمایت', resize=True)],
                                    [Button.text('راهنما📜', resize=True),Button.text('❓درباره ما', resize=True)]
                        ])
                #else :
                    #await event.delete()
                if event.raw_text == "❓درباره ما":
                    await event.reply(f"👤درباره ما\n\n↯طراحی: KingNetwork\n↯سرور: [Exclusive](https://t.me/King_network7)\n↯ورژن: 1.0.3\n↯لینک: نیم بها\n↯حمایت: [دونیت](https://www.payping.ir/d/WiZG)\n\n🆔 @{Config.CHANNEL_USERNAME}",link_preview=False)
            
        elif event.is_channel:
            if event.chat_id == Config.CHANNEL:
                if event.reply_to:
                    msg = await event.get_reply_message()
                    if regex := re.search(r"(\d*)/(\d*)",msg.message):
                        if regex.group(1) :
                            user_id = int(regex.group(1))
                            if "100" in regex.group(1):
                                user_id = int("-"+regex.group(1))
                            msg_id = int(regex.group(2))
                            if await event.client.send_message(entity=user_id, message=event.message, reply_to=msg_id):
                                await event.client.edit_message(event.chat_id,event.id,f"{event.message.message}\n sended")
                        
@client.on(events.NewMessage(incoming=True))
async def help_handler(event):
                        if event.raw_text == "راهنما📜":
                                    await event.reply(f"❗️راهنمای ربات\n\n⇇فایل مورد نظر خود ارسال یا فوروارد کنید\n⇇قبل از دانلود VPN را خاموش کنید\n⇇لینک های ربات نیم بها میباشد\n⇇انقضای فایل ها 30 روز است\n\n🆔 @{Config.CHANNEL_USERNAME}",link_preview=False)
                                    
@client.on(events.NewMessage(incoming=True))
async def donate_handler(event):
            if event.raw_text == "💰حمایت":
                        await client.send_message(event.chat_id,f"‼️برای ادامه فعالیت ربات و تامین بخشی از هزینه های سرور میتوانید از طریق لینک زیر از ربات و تیم حمایت کنید.\n\n🆔 @{Config.CHANNEL_USERNAME}",buttons=[
                                    [Button.url('🔥لینک دونیت🔥', 'https://payping.ir/d/WiZG')]
                        ])
            
@client.on(events.NewMessage(incoming=True))
async def support_handler(event):
            if event.raw_text == "پشتیبانی💠":
                        await client.send_message(event.chat_id,f"📞برای گزارش مشکل، انتقاد، پیشنهاد و... با آیدی زیر در ارتباط باشید.\n\n🆔 @{Config.CHANNEL_USERNAME}",buttons=[
                                    [Button.url('💡تماس با ما💡', 'https://t.me/king_network7_GP')]
                        ])
                        
                        
            
        elif event.is_channel:
            if event.chat_id == Config.CHANNEL:
                if event.reply_to:
                    msg = await event.get_reply_message()
                    if regex := re.search(r"(\d*)/(\d*)",msg.message):
                        if regex.group(1) :
                            user_id = int(regex.group(1))
                            if "100" in regex.group(1):
                                user_id = int("-"+regex.group(1))
                            msg_id = int(regex.group(2))
                            if await event.client.send_message(entity=user_id, message=event.message, reply_to=msg_id):
                                await event.client.edit_message(event.chat_id,event.id,f"{event.message.message}\n sended")
                        
                        
                        
            
client.run_until_disconnected()
