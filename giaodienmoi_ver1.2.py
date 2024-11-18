from keep_alive import keep_alive
keep_alive()

import aiohttp
import asyncio
import nest_asyncio #quan trọng nhất
import time
from collections import defaultdict
import random
import json
import os
import re
import io
import requests
import sqlite3
import hashlib
import zipfile
import tempfile
import subprocess
import logging
import threading
from threading import Lock
from datetime import datetime, timedelta, date
from io import BytesIO
from urllib.parse import urljoin, urlparse, urldefrag
from bs4 import BeautifulSoup
from PIL import Image, ImageOps, ImageDraw, ImageFont
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update, InputMediaPhoto
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
import psutil
from telegram import Update, InputFile
from gtts import gTTS
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
from typing import List  # Thêm dòng này để nhập khẩu List
from collections import deque
from telegram.ext import Application, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import filters  # Thay đổi ở đây
import httpx
from pyshorteners import Shortener
import pyshorteners
import urllib.parse


# Cài đặt mức độ login
#logging.basicConfig(level=logging.INFO) #xem lỗi k xem thì thêm #
logging.basicConfig(level=logging.WARNING)  # Chỉ hiển thị cảnh báo và lỗi
logging.getLogger('httpx').setLevel(logging.WARNING)
nest_asyncio.apply()
# Thông tin cấu hình
JOKE_FILE_PATH = 'dua.txt'
USERS_FILE_PATH = 'users.json'
users_keys = {}
freeuser = []
auto_spam_active = False
allowed_users = []
processes = []
ADMIN_ID = 5047988352  # ID ADMIN
GROUP_ID_KIN = -1001929593081 # ID NHÓM THÔNG TIN SPAM VỀ
ALLOWED_GROUP_ID = -1001988961300  #ID NHÓM CHO PHÉP
TOKEN = '7173014638:AAFJX-rdksp6AczK9ydmSn__soEtUyVXAhY'
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
last_command_time = {}
user_cooldowns = {}
is_bot_active = True  # Đặt trạng thái bot
start_time = time.time()  # Khởi tạo thời gian bắt đầu
request_queue = deque()
is_processing = False  # Biến để kiểm tra xem có đang xử lý không
users = []
# Biến toàn cục để lưu trạng thái
user_input_state = {}
nest_asyncio.apply()
IMGUR_CLIENT_ID = '74f5c858f447bb9'
SHORTENER = pyshorteners.Shortener()
API_KEY_THOI_TIET = '1dcdf9b01ee855ab4b7760d43a10f854'
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyA6kHx4wpCWYtjI9RKXXr5wQxHj27nRoV0'
bot = TeleBot(TOKEN)

#Hàm thả cảm xúc
class TelegramBotAPI:
    def __init__(self, bot_token):
        self.api_url = f"https://api.telegram.org/bot{bot_token}/"

    def call_api(self, action, body):
        response = requests.post(self.api_url + action, json=body)
        data = response.json()
        if not response.ok:
            print(f"Telegram API request failed: {action}", data)
            raise Exception('Telegram API request failed: ' + action)
        return data

    def set_message_reaction(self, chat_id, message_id, emoji):
        self.call_api('setMessageReaction', {
            'chat_id': chat_id,
            'message_id': message_id,
            'reaction': [{'type': 'emoji', 'emoji': emoji}],
            'is_big': True
        })

    def send_message(self, chat_id, text, inline_keyboard=None):
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': "Markdown",
            'disable_web_page_preview': True
        }
        if inline_keyboard:
            payload['reply_markup'] = {'inline_keyboard': inline_keyboard}

        self.call_api('sendMessage', payload)

def get_random_positive_reaction():
    valid_reactions = [
        '👍', '❤️', '🎉', '👾', '🤡', '💋', '🫡', '😡', '👄',
        '😘', '🥰', '😁', '👏', '😍', '💯', '🔥', '🏆',
        '⚡️', '🤩', '🕊', '🐳', '😱', '🐳', '🤩', '⚡️',
        '🏆', '🔥', '💯', '👏', '👾', '😡', '🤓', '😎',
        '🤪', '🥴', '💩', '🤡', '🙏🏼', '💋', '🎃', '🧑‍💻', '🤷',
        '💅', '💔', '❤️‍🔥', '💘', '👻', '👨‍👧‍👧', '🎅', '🍾',
        '😭', '👌', '🍌', '🥱', '🆒', '😴', '💊', '😈', '🖕',
        '😇', '🙉', '☃️', '🌭', '🎄', '😐', '🤷‍♀️', '🦄',
        '🐋', '🤯', '🤗'
    ]
    return random.choice(valid_reactions)

async def get_updates(bot_api):
    offset = None
    while True:
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?timeout=100&offset={offset}")
        data = response.json()
        if 'result' in data:
            for update in data['result']:
                offset = update['update_id'] + 1
                await on_update(update, bot_api)
        await asyncio.sleep(1)
###########
# Hàm tiện ích
def get_time_vietnam():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()
    
    if user_id in last_command_time and current_time - last_command_time[user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown - (current_time - last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None

# Tạo bảng người dùng trong cơ sở dữ liệu
def create_users_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            expiration_time TEXT
        )
    ''') 
    connection.commit()

# Hàm lấy timestamp
def TimeStamp():
    return str(date.today())

async def load_users_from_database():
    cursor.execute('SELECT user_id, expiration_time FROM users')
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        if expiration_time > datetime.now():
            allowed_users.append(user_id)

async def save_user_to_database(user_id, expiration_time):
    cursor.execute(
        '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
        ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()


#####################PHẦN KHAI BÁO##############################

# Hàm kiểm tra và đọc dữ liệu từ file users.json
async def load_users(filename=USERS_FILE_PATH) -> list:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    print('Lỗi khi phân tích dữ liệu JSON:', e)
                    return []
    else:
        print('Tệp users.json không tồn tại.')
    
    return []

def get_user():
    return load_users()  # Lấy danh sách người dùng

# Hàm lưu danh sách người dùng vào tệp JSON
async def save_user(users):
    with open(USERS_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# Hàm Gửi thông báo cho admin
async def notify_admin(context, user_info):
    try:
        total_users = len(users) + 1
        admin_message = (
            f"🔴 Người dùng mới❗️\n"
            f"Số lượng: {total_users}\n"
            f"Tên: @{user_info['username'] or 'Không có tên'}\n"
            f"ID: {user_info['id']}"  # Thêm ID của người dùng
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
    except Exception as e:
        print(f"Lỗi khi gửi thông báo cho admin: {e}")

# Hàm xử lý khi có người dùng mới
async def on_new_user(update, user_info, context):
    global users
    new_user_info = {
        'id': user_info['id'],
        'username': user_info['username']
    }
    
    if not any(user['id'] == new_user_info['id'] for user in users):
        users.append(new_user_info)
        await save_user(users)  # Lưu danh sách người dùng
        await notify_admin(context, new_user_info)  # Gửi thông báo cho admin


# Hàm khởi động để tải người dùng
async def initialize_users():
    global users
    users = await load_users()  # Tải người dùng từ file

# Hàm xử lý tin nhắn
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user:
        user_info = {
            'id': user.id,
            'username': user.username or 'Không có tên người dùng',
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        await on_new_user(update, user_info, context)

# Chạy hàm khởi động trong vòng lặp sự kiện
if __name__ == "__main__":
    import asyncio
    asyncio.run(initialize_users())  # Khởi động và tải người dùng
###################################################
# Hàm xử lý lệnh /users
async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(f'ID_ADMIN={ADMIN_ID}\nĐang tạo file users.json...')

        # Lưu danh sách người dùng vào file users.json
        with open('users.json', 'w') as json_file:
            json.dump(users, json_file, indent=4)

        # Gửi file users.json cho admin
        with open('users.json', 'rb') as json_file:
            await update.message.reply_document(document=json_file, filename='users.json', caption='Danh sách người dùng:')
    else:
        await update.message.reply_text("Lệnh này không được phép sử dụng.")

# Hàm xử lý lệnh /thongke
async def thongke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        total_users = len(users)
        blocked_users = 0  # Thay đổi logic nếu bạn có cách để theo dõi người đã chặn bot
        await update.message.reply_text(
            f"Số người đã sử dụng bot: {total_users}\nSố người đã chặn bot: {blocked_users}"
        )
    else:
        await update.message.reply_text("Lệnh này chỉ dành cho admin.")

# Hàm xử lý lệnh /send
async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text("Vui lòng nhập tin nhắn cần gửi:")
        user_input_state[user_id] = 'waiting_for_message'  # Đánh dấu trạng thái
    else:
        await update.message.reply_text("Lệnh này không được phép sử dụng.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_input_state and user_input_state[user_id] == 'waiting_for_message':
        message_to_send = update.message.text.strip()

        if not message_to_send:
            await update.message.reply_text("Tin nhắn không được để trống. Vui lòng nhập lại.")
            return

        confirmation_message = await update.message.reply_text(
            f"Bạn có muốn gửi tin nhắn này không?\n\n{message_to_send}\n\n(Trả lời 'Có' hoặc 'Không')"
        )
        user_input_state[user_id] = message_to_send  # Lưu tin nhắn để xử lý sau
    elif user_id in user_input_state:
        answer = update.message.text.strip().lower()

        if answer == 'có':
            message_to_send = user_input_state[user_id]
            success_count = 0
            failure_count = 0

            for user in users:
                user_id = user['id']
                if user_id:
                    try:
                        await context.bot.send_message(user_id, message_to_send)
                        success_count += 1
                    except Exception:
                        failure_count += 1

            await update.message.reply_text(
                f"Tin nhắn đã được gửi thành công!\n"
                f"Số lượng gửi thành công: {success_count}\n"
                f"Số lượng gửi thất bại: {failure_count}"
            )
            # Kiểm tra và xóa trạng thái
            if user_id in user_input_state:
                del user_input_state[user_id]
        elif answer == 'không':
            await update.message.reply_text("Quá trình gửi đã được hủy.")
            # Kiểm tra và xóa trạng thái
            if user_id in user_input_state:
                del user_input_state[user_id]
        else:
            await update.message.reply_text("Phản hồi không hợp lệ. Vui lòng trả lời 'Có' hoặc 'Không'.")

##################################################################################################
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Danh sách các ID hiệu ứng
    effects = {
        "🔥": "5104841245755180586",
        "👍": "5107584321108051014",
        "👎": "5104858069142078462",
        #"❤️": "5044134455711629726",
        "🎉": "5046509860389126442",
        "💩": "5046589136895476101"
    }

    # Chọn ngẫu nhiên một hiệu ứng từ danh sách
    effect_id = random.choice(list(effects.values()))

    user_info = {
        'id': update.effective_user.id,
        'name': update.effective_user.first_name,
        'username': update.effective_user.username
    }

    # Gọi hàm xử lý người dùng mới
    await on_new_user(update, user_info, context)

    help_text = '''
<blockquote expandable>
<tg-spoiler>┏➖〰️➖〰️➖〰️➖〰️➖〰️┓</tg-spoiler>
    <b>━━━LỆNH CỦA BOT━━━</b>
<tg-spoiler>┗➖〰️➖〰️➖〰️➖〰️➖〰️┛</tg-spoiler>
┌────⭓
│        <tg-spoiler><b>━━━AI━━━</b></tg-spoiler>
│» <b>/gpt</b> - Chat GPT
│» <b>/gemi</b> - Gemini Pro
│» <b>/hoi</b> - Chat cùng Gemini
│» <b>/bb</b> - BB Ai Help v3
│» <b>/tbp</b> - TPY AI 
│» <b>/php</b> - PHP AI 
│» <b>/bing</b> - Microsoft Copilot
│» <b>/llama</b> - Meta AI
│» <b>/qwen</b> - Alibaba Cloud AI 
│        <tg-spoiler><b>━━━MXH━━━</b></tg-spoiler>
│» <b>/tt</b> - Check info Tiktok
│» <b>/fb</b> - Check info Facebook
│» <b>/yt</b> + [Link Youtube] Scan info + Tải mp3
│» <b>/ytb_audio</b> + [Link Youtube] Tải mp3
│» <b>/downfb</b> - Tải video Facebook
│» <b>/downig</b> - Tải video Instagram
│» <b>/downx</b> - Tải video X
│» <b>/lyrics</b> [Lời bài hát] : Tìm lời bài hát
│» <b>/spotify</b> : Tải nhạc Spotify
│» <b>/timnhac</b> : Tìm bài hát
│» <b>/tiktok</b> - Tải video tik tok (nhanh)
│» <b>/down</b> + [Link Video] : Tải video Facebook, Tiktok, Instagram
│        <tg-spoiler><b>━━━Tiện ích━━━</b></tg-spoiler>
│» <b>/trollvn</b> - Troll troll troll
│» <b>/taoanhnhanh</b> + [Mô tả tiếng anh] : Tạo ảnh theo yêu cầu
│» <b>/voice</b> + [văn bản] - Tạo voice từ văn bản
│» <b>/upanh</b> - Up ảnh lấy link
│» <b>/bank</b> + [Ngân Hàng] + [STK] - Tạo QR chuyển khoản
│» <b>/checkvar</b> + [HỌ VÀ TÊN HOẶC SỐ TIỀN] - Check phông bạt
│» <b>/thoitiet</b> - Xem thời tiết
│» <b>/rd_cat</b> : Random ảnh mèo
│» <b>/timanh</b> + [Mô tả] : Tìm ảnh 
│» <b>/camhung</b> : Câu nói cảm hứng
│» <b>/code</b> - Lấy Code HTML
│» <b>/laytheme</b> + [Link web] : Lấy theme website
│» <b>/tuoi</b> + [Tên] : Đoán tuổi qua tên 
│» <b>/checkip</b> + [IP] - Check IP
│» <b>/bxs</b> - Check phạt nguội
│» <b>/qr</b> + [Văn bản] - Tạo QR CODE
│» <b>/time</b> - Thời gian hoạt động
│» <b>/tv</b> - Ngôn ngữ tiếng việt
│» <b>/2fa</b> - Lấy mã 2FA
│» <b>/id</b> - Lấy ID
└───────────⭓
</blockquote>
'''

    # Tạo nút nằm ngang
    keyboard = [
        [
            InlineKeyboardButton("➕ ADD ME", url='https://t.me/kmb_tienich_bot?startgroup=true'),
            InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=help_text, 
        parse_mode='HTML', 
        reply_markup=reply_markup,
        reply_to_message_id=update.message.message_id if update.message else None,
        message_effect_id=effect_id
    )

is_bot_active = True

#XỬ LÝ LỆNH TROLL
async def trollvn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    def read_jokes():
        with open(JOKE_FILE_PATH, 'r', encoding='utf-8') as file:
            jokes = file.readlines()
        return jokes

    chat_id = update.message.chat.id
    message_id = update.message.message_id
    await update.message.chat.send_action("typing")  # Thêm dòng này

    try:
        vietnamese_jokes = read_jokes()
        joke = random.choice(vietnamese_jokes).strip()  # Loại bỏ ký tự xuống dòng
        await update.message.reply_text(text=f"<blockquote><i>{joke}</i></blockquote>", parse_mode='HTML')  # Sử dụng thẻ <i>
    except FileNotFoundError:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="HẾT CÂU ĐỂ NÓI.")
    except Exception as e:
        await update.message.reply_text(text=f"LỖI: {e}")

# Hàm xử lý lệnh /voice
async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    user_id = update.effective_user.id

    if not is_bot_active:
        await update.message.reply_text(text='Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    text = ' '.join(context.args)

    if not text:
        await update.message.reply_text(text='<blockquote><i>❓Sử dụng: /voice {văn bản cần tạo giọng}\n💭 Ví dụ: <code>/voice KMB247</code></i></blockquote>', parse_mode='HTML')  # Sử dụng thẻ <i>
        return

    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            pass  # Bỏ qua phần này
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    try:
        tts = gTTS(text, lang='vi', slow=False)
        tts.save('voice_message.mp3')

        with open('voice_message.mp3', 'rb') as voice_file:
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=voice_file, caption=f"Nội dung: {text}", reply_to_message_id=update.message.message_id)

        os.remove('voice_message.mp3')  # Xóa file sau khi gửi để tiết kiệm dung lượng

    except Exception as e:
        await update.message.reply_text(chat_id=update.effective_chat.id, text=f'Có lỗi xảy ra: {e}')
    
# Hàm xử lý lệnh /time
async def thoigianhdbot(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    current_time = time.time()
    uptime = current_time - start_time
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    seconds = int(uptime % 60)
    uptime_str = f'{hours} giờ, {minutes} phút, {seconds} giây'

    # Gửi phản hồi về thời gian hoạt động
    await update.message.reply_text(
        text=f'<blockquote>Bot Đã Hoạt Động Được: {uptime_str}</blockquote>',
        parse_mode='HTML'
    )

#Xử lý lệnh /code
async def code(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    # Tách lệnh và URL từ tin nhắn
    command_args = update.message.text.split(maxsplit=1)

    # Kiểm tra xem URL có được cung cấp không
    if len(command_args) < 2:
        await update.message.reply_text(text='<blockquote><i>❓Sử dụng: /code.\n💭Ví dụ: /code https://google.com </i></blockquote>', parse_mode='HTML')  # Sử dụng thẻ <i>
        return

    url = command_args[1]
    domain = urlparse(url).netloc
    file_name = f"{domain}.txt"
    
    try:
        # Lấy nội dung HTML từ URL
        response = requests.get(url)
        response.raise_for_status()  # Xảy ra lỗi nếu có lỗi HTTP

        # Lưu nội dung HTML vào file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)

        # Gửi file về người dùng
        with open(file_name, 'rb') as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=file, caption=f"HTML của trang web {url}")

        # Phản hồi tin nhắn gốc
        await update.message.reply_text(text="<blockquote><i>Đã gửi mã nguồn HTML đây.</i></blockquote>", parse_mode='HTML')

    except requests.RequestException as e:
        await update.message.reply_text(text=f"<i>LỖI khi tải trang web: {e}</i>", parse_mode='HTML')

    finally:
        # Đảm bảo xóa file sau khi gửi
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                await update.message.reply_text(chat_id=update.effective_chat.id, text=f"LỖI khi xóa file: {e}")

# Xử lý lệnh /id
async def get_user_info(user, bot):
    user_mention = user.first_name
    user_id = user.id
    username = user.username if user.username else None
    language_code = user.language_code if hasattr(user, 'language_code') else "Không rõ"
    bio = (await bot.get_chat(user_id)).bio or "Không có bio"
    status_text = "Trạng thái"  # Cần xác định rõ trạng thái nếu có

    return user_mention, user_id, username, language_code, bio, status_text

async def id(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    if len(update.message.text.split()) == 1:  
        user_id = update.message.from_user.id
        first_name = update.message.from_user.first_name
        user_mention, user_id, username, language_code, bio, status_text = await get_user_info(update.message.from_user, context.bot)

        # Tạo user_link chỉ khi username tồn tại
        user_link = f"https://t.me/{username}" if username else "Chưa Có"

        # Lấy avatar
        profile_photos = await context.bot.get_user_profile_photos(user_id)
        avatar_url = profile_photos.photos[-1][-1].file_id if profile_photos.photos else None

        response_message = f"""
<blockquote>
┌───⭓ Thông Tin
│» <b>Tên Người Dùng:</b> {first_name}
│» <b>Username:</b> <a href="{user_link}">{username}</a>
│» <b>User Link:</b> <a href="{user_link}">Link đến Hồ Sơ</a>
│» <b>User ID:</b> <code>{user_id}</code>
│» <b>Language</b>: {language_code}
│» <b>Bio</b>: {bio}
│» <b>Trạng thái</b>: {status_text}
└───────────
</blockquote>
"""

        # Tạo nút nằm ngang
        keyboard = [
            [
                InlineKeyboardButton("➕ ADD ME", url='https://t.me/kmb_tienich_bot?startgroup=true'),
                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if avatar_url:
            await update.message.reply_photo(photo=avatar_url, caption=response_message, parse_mode='HTML', reply_markup=reply_markup)
        else:
            await update.message.reply_text(text=response_message, parse_mode='HTML', reply_markup=reply_markup)
    else:  
        username = update.message.text.split('@')[-1].strip()
        try:
            user = await context.bot.get_chat(username)  # Lấy thông tin người dùng từ username
            user_mention, user_id, username, language_code, bio, status_text = await get_user_info(user, context.bot)

            # Tạo user_link chỉ khi username tồn tại
            user_link = f"https://t.me/{username}" if username else "Chưa Có"

            # Lấy avatar
            profile_photos = await context.bot.get_user_profile_photos(user.id)
            avatar_url = profile_photos.photos[-1][-1].file_id if profile_photos.photos else None

            response_message = f"""
<blockquote>
┌───⭓ Thông Tin
│» <b>Tên Người Dùng:</b> {user.first_name}
│» <b>Username:</b> <a href="{user_link}">{username}</a>
│» <b>User Link:</b> <a href="{user_link}">Link đến Hồ Sơ</a>
│» <b>User ID:</b> <code>{user.id}</code>
│» <b>Language</b>: {language_code}
│» <b>Bio</b>: {bio}
│» <b>Trạng thái</b>: {status_text}
└───────────
</blockquote>
"""
            # Tạo nút nằm ngang
            keyboard = [
                [
                    InlineKeyboardButton("➕ ADD ME", url='https://t.me/kmb_tienich_bot?startgroup=true'),
                    InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if avatar_url:
                await update.message.reply_photo(photo=avatar_url, caption=response_message, parse_mode='HTML', reply_markup=reply_markup)
            else:
                await update.message.reply_text(text=response_message, parse_mode='HTML', reply_markup=reply_markup)
        except Exception as e:
            await update.message.reply_text(text="Không tìm thấy người dùng có username này.")

# Xử lý lệnh /tv
async def tieng_viet(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    # Tạo bàn phím với một hàng
    keyboard = [[InlineKeyboardButton("Tiếng Việt 🇻🇳", url='https://t.me/setlanguage/abcxyz')]]
    reply_markup = InlineKeyboardMarkup(keyboard)  # Khởi tạo InlineKeyboardMarkup với keyboard
    
    try:
        # Gửi tin nhắn với bàn phím
        await update.message.reply_text(
            'Click Vào Nút "<b>Tiếng Việt</b>" để đổi ngôn ngữ.',
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        # Xóa tin nhắn lệnh của người dùng
        await context.bot.delete_message(chat_id, message_id)
    except Exception as e:
        await update.message.reply_text(f"Không thể xóa tin nhắn: {e}", parse_mode='HTML')

# Hàm xử lý lệnh /2fa
async def send_2fa(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi
    if update.message is None:
        return  # Không có tin nhắn để phản hồi

    if len(context.args) == 0:
        await update.message.reply_text("<blockquote>Sử dụng: /2fa {mã 2fa}</blockquote>", parse_mode='HTML')
        return

    # Kết hợp mã và loại bỏ khoảng trắng
    code = ''.join(context.args)  # Kết hợp tất cả các phần lại với nhau
    url = f'https://2fa.live/tok/{code}'

    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            # Phân tích JSON để lấy mã token
            data = json.loads(response.text)
            token = data.get('token', 'Không tìm thấy mã token.')
            await update.message.reply_text(f"<blockquote><i>Mã 2FA: 👉     {token}     👈</i></blockquote>", parse_mode='HTML')
        else:
            await update.message.reply_text("Đã có lỗi xảy ra khi lấy mã.")
    except Exception as e:
        await update.message.reply_text(f"Đã có lỗi xảy ra: {str(e)}")

# Hàm tải ảnh lên Imgur
async def upload_to_imgur(image_data):
    headers = {
        'Authorization': f'Client-ID {IMGUR_CLIENT_ID}',
    }
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        async with session.post('https://api.imgur.com/3/image', data=image_data, headers=headers) as response:
            return await response.json()

# Hàm xử lý lệnh /upanh
async def cmd_upanh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("GỬI TÔI ẢNH CẦN LẤY LINK")
    context.user_data['waiting_for_photo'] = True  # Đánh dấu trạng thái

# Hàm xử lý ảnh
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('waiting_for_photo'):
        photo = update.message.photo[-1]  # Lấy ảnh có độ phân giải cao nhất
        file = await context.bot.get_file(photo.file_id)

        # Tải tệp hình ảnh về
        image_data = await file.download_as_bytearray()

        # Tạo data cho yêu cầu tải lên Imgur
        imgur_data = aiohttp.FormData()
        imgur_data.add_field('image', image_data, filename='image.jpg', content_type='image/jpeg')

        try:
            # Tải ảnh lên Imgur
            response = await upload_to_imgur(imgur_data)
            if response['success']:
                link = response['data']['link']
                await update.message.reply_text(f"LINK ẢNH CỦA BẠN ĐÂY: {link}")

                # Gửi thông báo vào nhóm
                await context.bot.send_message(GROUP_ID_KIN, f'''
<b>THÔNG BÁO MỚI</b>\n
<blockquote>
╭─────────────⭓
│ 👮 @{update.message.from_user.username} 
│ 🔗 Liên kết ảnh: {link}
╰─────────────⭓
</blockquote>
                ''', parse_mode='HTML')
            else:
                await update.message.reply_text("Có lỗi xảy ra khi tải ảnh lên Imgur.")
        except httpx.ReadTimeout:
            await update.message.reply_text("Yêu cầu đã hết thời gian chờ. Vui lòng thử lại.")
        
        context.user_data['waiting_for_photo'] = False  # Kết thúc trạng thái
    else:
        pass  # Không làm gì nếu không đang chờ ảnh


async def zhelp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id != ADMIN_ID:  # Kiểm tra xem người dùng có phải là admin không
        await update.message.reply_text("Bạn không có quyền sử dụng lệnh này.")
        return

    help_text = (
        "<blockquote>DANH SÁCH LỆNH CỦA ADMIN:\n"
        "/users - Xem danh sách người dùng\n"
        "/thongke - Xem số người sử dụng\n"
        "/send - Gửi tin nhắn cho người dùng\n"
        "</blockquote>"
    )
    
    await update.message.reply_text(help_text, parse_mode='HTML')

#Hàm xử lý lệnh /tiktok
#https://www.tikwm.com/api/?url=
async def luuvideo_tiktok(update, context, bot_api=None):
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    if len(context.args) == 0:
        await update.message.reply_text('<blockquote>❓ /tiktok {link video}.\n💭 Ví dụ: <code>/tiktok https://vt.tiktok.com/ABC</code></blockquote>', parse_mode='HTML')
        return
    
    linktt = context.args[0]
    data = f'url={linktt}'
    head = {
        "Host": "www.tikwm.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://www.tikwm.com/api/", data=data, headers=head) as response:
            response_json = await response.json()
    
    rq = response_json['data']
    tieude = rq['title']
    author_nickname = rq['author']['nickname']
    author_id = rq['author']['unique_id']
    region = rq['region']
    view = rq['play_count']
    likes = rq['digg_count']
    comments = rq['comment_count']
    shares = rq['share_count']
    downloads = rq['download_count']
    favorites = rq['collect_count']
    music_play = rq['music_info']['play']  # Link âm thanh
    music_title = rq['music_info']['title']  # Tiêu đề âm thanh
    
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    sent_message = await update.message.reply_text('🔎')

    try:
        # Tạo nút nằm ngang
        keyboard = [
            [
                InlineKeyboardButton("🎹 LINK NHẠC", url=rq['music']),
                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if rq['duration'] > 0:  # Nếu là video
            linkz = rq['play']
            caption = (
                f'🎥 <b>{tieude}</b>\n'
                f'<blockquote>'
                f'👤 <b>Tác giả:</b> <a href="https://www.tiktok.com/@{author_id}">{author_nickname}</a>\n'
                f'🌍 <b>Khu Vực:</b> {region}\n'
                f'🎮 <b>Độ Dài Video:</b> {rq["duration"]} Giây\n'
                f'---------------------------------------\n'
                f'▶️ <b>Views:</b> {view}\n'
                f'❤️ <b>Likes:</b> {likes} like\n'
                f'💬 <b>Comments:</b> {comments}\n'
                f'🔄 <b>Shares:</b> {shares}\n'
                f'⬇️ <b>Downloads:</b> {downloads}\n'
                f'📥 <b>Favorites:</b> {favorites}\n'
                f'</blockquote>'
            )
            
            # Gửi video
            await context.bot.send_video(
                update.message.chat_id,
                video=linkz,
                caption=caption,
                supports_streaming=True,
                parse_mode='HTML',
                reply_markup=reply_markup,
                reply_to_message_id=update.message.message_id
            )
            
#            # Gửi tệp âm thanh cùng với video
#            await context.bot.send_audio(
#                chat_id=update.message.chat_id,
#                audio=music_play,
#                title=music_title,
#                caption=caption,
#                parse_mode='HTML',
#            )

        else:  # Nếu là ảnh
            images = rq['images']
            captions = (
                f'📸 <b>{tieude}</b>\n'
                f'<blockquote>'
                f'👤 <b>Tác giả:</b> <a href="https://www.tiktok.com/@{author_id}">{author_nickname}</a>\n'
                f'🌍 <b>Khu Vực:</b> {region}\n'
                f'---------------------------------------\n'
                f'▶️ <b>Views:</b> {view}\n'
                f'❤️ <b>Likes:</b> {likes} like\n'
                f'💬 <b>Comments:</b> {comments}\n'
                f'🔄 <b>Shares:</b> {shares}\n'
                f'⬇️ <b>Downloads:</b> {downloads}\n'
                f'📥 <b>Favorites:</b> {favorites}\n'
                f'</blockquote>'
            )

            # Gửi ảnh theo nhóm tối đa 10 ảnh
            for i in range(0, len(images), 10):
                media_group = [InputMediaPhoto(media=img) for img in images[i:i+10]]
                await context.bot.send_media_group(
                    chat_id=update.message.chat_id,
                    media=media_group,
                    reply_to_message_id=update.message.message_id
                )
                
            # Gửi tệp âm thanh
            await context.bot.send_audio(
                chat_id=update.message.chat_id,
                audio=music_play,
                title=music_title,
                caption=captions,
                parse_mode='HTML',
                reply_markup=reply_markup, # Thêm nút vào phần gửi ảnh
                reply_to_message_id=update.message.message_id   
            )

    except Exception as e:
        await context.bot.send_message(
            update.message.chat_id,
            f'Có lỗi xảy ra: {str(e)}',
        )
    
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=sent_message.message_id)

# Hàm xử lý lệnh thời tiết
async def thoitiet(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi
        
    command, *args = update.message.text.split()
    if not args:
        await context.bot.send_message(chat_id=update.message.chat_id, 
                                        text='<blockquote>❓Sử dụng /thoitiet.\n💭 Ví dụ: <code>thoitiet Hà nội</code></blockquote>', 
                                        parse_mode='HTML')
        return
    
    city = ' '.join(args)
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_THOI_TIET}&units=metric'
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url) as response:
                if response.status == 200:
                    weather_data = await response.json()
                    if weather_data['cod'] == 200:
                        weather_info = weather_data['weather'][0]['description']
                        temp_info = weather_data['main']['temp']
                        humidity_info = weather_data['main']['humidity']
                        wind_speed_info = weather_data['wind']['speed']
                        feels_like_info = weather_data['main']['feels_like']
                        pressure_info = weather_data['main']['pressure']
                        visibility_info = weather_data['visibility']
                        wind_direction = weather_data['wind']['deg']
                        wind_gust = weather_data['wind'].get('gust', 0)

                        reply = (f'<blockquote>'
                        f'╭────⭓ Thời Tiết\n'
                        f'│🔆 <b>Thông Tin Thời Tiết ở</b> {weather_data["name"]}\n'
                        f'│🌍 <b>Thành phố:</b> {weather_data["name"]}\n'
                        f'│🔗 <b>Link bản đồ:</b> <a href="https://www.google.com/maps/search/?api=1&query={weather_data["coord"]["lat"]},{weather_data["coord"]["lon"]}">Xem bản đồ</a>\n'
                        f'│☁️ <b>Thời tiết:</b> {weather_info}\n'
                        f'│🌡 <b>Nhiệt độ hiện tại:</b> {temp_info}°C\n'
                        f'│🌡️ <b>Cảm giác như:</b> {feels_like_info}°C\n'
                        f'│🌡️ <b>Nhiệt độ tối đa:</b> {weather_data["main"]["temp_max"]}°C\n'
                        f'│🌡️ <b>Nhiệt độ tối thiểu:</b> {weather_data["main"]["temp_min"]}°C\n'
                        f'│🍃 <b>Áp suất:</b> {pressure_info} hPa\n'
                        f'│🫧 <b>Độ ẩm:</b> {humidity_info}%\n'
                        f'│☁️ <b>Mức độ mây:</b> {weather_data["clouds"]["all"]}%\n'
                        f'│🌬️ <b>Tốc độ gió:</b> {wind_speed_info} m/s\n'
                        f'│🌐 <b>Quốc gia:</b> {weather_data["sys"]["country"]}\n'
                        f'│🌬 <b>Hướng gió:</b> {wind_direction}°\n'
                        f'│🏭 <b>Chất lượng không khí:</b> 3\n'
                        f'╰───────────── ⭐'
                        f'</blockquote>')

                    else:
                        reply = 'Không tìm thấy thông tin thời tiết cho địa điểm này.'
                else:
                    reply = f'LỖI: {response.status}'
    
    except Exception as e:
        reply = f'LỖI khi thực hiện yêu cầu: {str(e)}'
    
    await context.bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode='HTML')


#Hàm liên quan đến lệnh /hoi cái gì cũng nằm đây hết
# Thư mục cache
CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

async def get_me(application):
    try:
        await application.bot.get_me()
    except httpx.ConnectTimeout:
        print("Từ từ, hình như bị lỗi rồi.")
    except Exception as e:
        print(f"Lỗi: {str(e)}")

def cache_response(question, response):
    cache_file = os.path.join(CACHE_DIR, f"{hash(question)}.json")
    with open(cache_file, 'w') as f:
        json.dump(response, f)

def get_cached_response(question):
    cache_file = os.path.join(CACHE_DIR, f"{hash(question)}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

#Hàm xử lý lệnh /hoi #################
async def hoi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    question = ' '.join(context.args)

    # Gửi trạng thái "Đang suy nghĩ..."
    thinking_message = await update.message.reply_text('🤖 Đang suy nghĩ...')

    # Kiểm tra phản hồi nô đùa
    custom_response = get_custom_response(question)
    if custom_response:
        await thinking_message.delete()  # Xóa trạng thái
        await update.message.reply_text(custom_response)
        return

    # Kiểm tra cache trước
    cached_response = get_cached_response(question)
    if cached_response:
        await thinking_message.delete()  # Xóa trạng thái
        await update.message.reply_text(cached_response['result']['message'])
        return

    # Gửi yêu cầu đến API
    payload = {
        'contents': [
            {
                'parts': [
                    {'text': question}
                ]
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        data = response.json()
        if 'candidates' in data and data['candidates']:
            message = data['candidates'][0]['content']['parts'][0]['text']
            await thinking_message.delete()  # Xóa trạng thái
#            formatted_message = f"*Phản hồi:* \n{message}"
            formatted_message = f"🤖\n{message}"
            await update.message.reply_text(formatted_message, parse_mode='MarkdownV2')


            # Lưu vào cache
            cache_response(question, {'result': {'message': message}})
        else:
            await thinking_message.delete()  # Xóa trạng thái
            await update.message.reply_text('Không có phản hồi từ API.')
    except Exception as e:
        await thinking_message.delete()  # Xóa trạng thái
        pass

#Hàm khi ai đó reply lại tin nhắn bot################################
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        question = update.message.text

        # Tùy chỉnh phản hồi nô đùa
        custom_response = get_custom_response(question)
        if custom_response:
            await update.message.reply_text(custom_response)
            return

        # Gửi yêu cầu đến API
        thinking_message = await update.message.reply_text('🤖 Đang suy nghĩ...')
        payload = {
            'contents': [
                {
                    'parts': [
                        {'text': question}
                    ]
                }
            ]
        }

        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()  # Kiểm tra lỗi HTTP

            data = response.json()
            if 'candidates' in data and data['candidates']:
                message = data['candidates'][0]['content']['parts'][0]['text']

                # Xóa trạng thái
                if thinking_message:
                    try:
                        await thinking_message.delete()
                    except Exception as e:
                        print(f"Không thể xóa tin nhắn: {str(e)}")

                # Escape các ký tự Markdown
                formatted_message = escape_markdown(f"🤖\n\n{message}")

                # Kiểm tra độ dài tin nhắn
                if len(formatted_message) > 4096:
                    # Chia nhỏ tin nhắn
                    for i in range(0, len(formatted_message), 4096):
                        await update.message.reply_text(formatted_message[i:i + 4096], parse_mode='MarkdownV2')
                else:
                    await update.message.reply_text(formatted_message, parse_mode='MarkdownV2')
            else:
                # Xóa trạng thái
                if thinking_message:
                    try:
                        await thinking_message.delete()
                    except Exception as e:
                        print(f"Không thể xóa tin nhắn: {str(e)}")
                await update.message.reply_text('Không có phản hồi từ API.')
        except Exception as e:
            # Xóa trạng thái
            if thinking_message:
                try:
                    await thinking_message.delete()
                except Exception as e:
                    print(f"Không thể xóa tin nhắn: {str(e)}")
            await update.message.reply_text(f'Lỗi: {str(e)}')

def escape_markdown(text: str) -> str:
    """Escape các ký tự đặc biệt trong MarkdownV2."""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text

#Phần từ khóa chửi lại
def get_custom_response(question: str) -> str:
    question = question.lower()
    if 'cmm' in question:
        return "🤖con mẹ tao ở nhà"
    if 'dmm' in question:
        return "🤖rảnh hơi lắm hả"
    if 'cha' in question:
        return "🤖cha đây con iu"
    if 'mẹ' in question:
        return "🤖mẹ m tên gì"
    if 'đĩ' in question:
        return "🤖sao biết t làm đĩ"
    if 'cút' in question:
        return "🤖được, tôi cút vào tim em"
    if 'chó' in question:
        return "🤖vâng tôi là chó"
    if 'súc' in question:
        return "🤖mất day"
    if 'sv' in question:
        return "🤖cc"
    if 'hình' in question:
        return "🤖hình để ở nhà"
    if 'địt' in question:
        return "🤖cái mồm mày"
    if 'mày' in question:
        return "🤖thằng chóa này"
    if 'tao' in question:
        return "🤖what the fuck🖕"
    elif 'cc' in question:
        return "🤖sủa gì vậy"
    elif 'học' in question:
        return "🤖Học hành thì khó thật! Nhưng đừng lo, không biết thì hỏi tao này 😆"
    return None  # Không có phản hồi nô đùa


async def send_message_bank(chat_id, text, parse_mode=None):
    async with aiohttp.ClientSession() as session:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        async with session.post(f"{BASE_URL}sendMessage", json=payload) as response:
            return await response.json()

async def send_photo_bank(chat_id, photo_url, caption=None):
    async with aiohttp.ClientSession() as session:
        payload = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": 'HTML'
        }
        async with session.post(f"{BASE_URL}sendPhoto", json=payload) as response:
            return await response.json()

async def lenhbank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id  # Lấy chat_id từ update
    command = update.message.text  # Lấy lệnh từ message

    try:
        args = command.split()
        if len(args) != 3:
            await send_message_bank(chat_id, "<blockquote>\n<b>Sử dụng:</b> /bank {Ngân hàng}  {STK}\n<b>Ví dụ:</b> /bank mbbank 123878\n</blockquote>", parse_mode='HTML')
            return
        
        bank_name = args[1]
        account_no = args[2]

        bank_id = get_bank_id(bank_name)
        template = 'compact'
        amount = 0
        description = urllib.parse.quote('TIEN ICH KMB')  # Mã hóa mô tả
        account_name = 'Người thụ hưởng'

        quick_link = f"https://img.vietqr.io/image/{bank_id}-{account_no}-{template}.png?amount={amount}&addInfo={description}&accountName={account_name}"

        # Tạo tin nhắn mô tả
        message_text = (
            "<blockquote>\n"
            "<b>Mã QR CỦA</b>\n"
            f"<b>STK</b>: <code>{account_no}</code>\n"
            f"<b>NGÂN HÀNG</b>: <u>{bank_name}</u>\n"
            "<b>CHECK TRƯỚC KHI GỬI CHO NGƯỜI KHÁC</b>\n"
            "</blockquote>"
        )

        # Gửi hình ảnh QR kèm theo mô tả
        await update.message.chat.send_action("upload_photo")
        await send_photo_bank(chat_id, quick_link, message_text)

    except Exception as e:
        await send_message(chat_id, f"LỖI: {str(e)}")

def get_bank_id(bank_name):
    bank_ids = {
        "mbbank": "mbbank",
        "vietinbank": "970415",
        # Thêm các ngân hàng khác tại đây
    }
    return bank_ids.get(bank_name.lower(), bank_name)
#####
# Đọc các đường link từ file getproxy.txt
async def load_proxy_sites():
    with open('getproxy.txt', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# Hàm xử lý lệnh /proxy
async def proxy(update, context, bot_api=None):
    chat_id = update.effective_chat.id
    num_proxies_str = context.args[0] if context.args else None  # Lấy tham số
    # Kiểm tra nếu không có số lượng
    if not num_proxies_str or not num_proxies_str.isdigit():
        await context.bot.send_message(
            chat_id=chat_id,
            text='<blockquote><i>❓Sử dụng: /proxy {số lượng}\n💭 Ví dụ: <code>/proxy 100</code></i></blockquote>',
            parse_mode='HTML',
            reply_to_message_id=update.message.message_id
        )
        return

    num_proxies = int(num_proxies_str)
    proxies = []

    proxy_sites = await load_proxy_sites()

    try:
        async with aiohttp.ClientSession() as session:
            for site in proxy_sites:
                async with session.get(site) as response:
                    if response.status == 200:
                        lines = await response.text()
                        for line in lines.split('\n'):
                            if ':' in line:
                                proxies.append(line.strip())
                                if len(proxies) >= num_proxies:
                                    break
                    if len(proxies) >= num_proxies:
                        break

        # Tạo file proxy_kmb.txt
        proxy_file_path = 'proxy_kmb.txt'
        with open(proxy_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(proxies))

        # Tạo nút nằm ngang
        keyboard = [
            [
                InlineKeyboardButton("➕ ADD ME", url='https://t.me/kmb_tienich_bot?startgroup=true'),
                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.chat.send_action("upload_document") #trạng thái gửi
        # Gửi file proxy cho người dùng
        with open(proxy_file_path, 'rb') as proxy_file:
            await context.bot.send_document(
                chat_id=chat_id,
                document=proxy_file,
                caption='Đây là danh sách proxy của bạn.',
                reply_to_message_id=update.message.message_id,
                reply_markup=reply_markup,  # Sử dụng reply_markup ở đây
            )

        # Xóa file tạm sau khi gửi
        os.remove(proxy_file_path)

    except Exception as error:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f'Đã có lỗi xảy ra: {error}',
            reply_to_message_id=update.message.message_id
        )

# Hàm xử lý lệnh /fb
async def fb(update: Update, context: CallbackContext) -> None:
    # Kiểm tra nếu có ID được cung cấp
    if not context.args:
        await update.message.reply_text("Sử dụng /fb [id]", parse_mode=ParseMode.HTML)
        return

    user_id = ' '.join(context.args)

    # Gửi trạng thái đang gõ
    await update.message.chat.send_action("typing")

    # Gọi API để lấy thông tin Facebook
    api_url = f"https://keyherlyswar.x10.mx/getinfofb.php?uid={user_id}"
    response = requests.get(api_url)
    data = response.json()

    if data.get("id"):
        # Lấy thông tin từ API
        user_id = data["id"]
        is_verified = data["is_verified"]
        updated_time = data["updated_time"]
        likes = data.get("likes", {}).get("data", [])
        created_time = data["created_time"]
        posts = data.get("posts", {}).get("data", [])
        username = data["username"]
        link = data["link"]
        name = data["name"]
        locale = data["locale"]
        location = data.get("location", {}).get("name", "")
        first_name = data["first_name"]
        subscribers = data.get("subscribers", {}).get("summary", {}).get("total_count", 0)
        birthday = data.get("birthday", "")
        gender = data.get("gender", "")
        about = data.get("about", "")
        education = data.get("education", [])
        living = data.get("living", [])
        interested_in = data.get("interested_in", [])

        # Tạo nội dung thông tin
        info_text = f"╭─────────────⭓\n"\
                    f"│ ID: {user_id}\n"\
                    f"│ Name: ‎ (ảnh) {name} (facebook.com/{user_id})\n"\
                    f"│ Username: {username}\n"\
                    f"│ Link: facebook.com/{username}\n"\
                    f"│ Verified: {'Chưa xác minh' if not is_verified else 'Đã xác minh'}\n"\
                    f"│ Creatime Time: {created_time}\n"\
                    f"│ Gender: {gender}\n"\
                    f"│ Location: Sống tại {location}\n"\
                    f"│ Work: Không xác định\n"\
                    f"│ Birthday: {birthday}\n"\
                    f"│ Follows: Có {subscribers} người (facebook.com/{user_id}/followers) theo dõi\n"\
                    f"│ Friends: Có 0 người (facebook.com/{user_id}/friends) bạn\n"\
                    f"│ Likes: Tiên đã thích {len(likes)} trang (facebook.com/profile.php?id={user_id}&sk=likes)\n"\
                    f"│ About: {about}\n"\
                    f"├─────────────⭔\n"\
                    f"│ Language: 🇻🇳 Tiếng Việt (vi_VN)\n"\
                    f"│ Last Updated: {updated_time}\n"\
                    f"│ Time Zone: GMT 7\n"\
                    f"╰─────────────⭓"

        # Tạo phần thông tin học vấn
        education_text = ""
        if education:
            education_text = "╭─────────────⭓\n"\
                             "│ Học vấn:\n"
            for school in education:
                school_name = school.get("school", {}).get("name", "")
                degree = school.get("degree", "")
                start_date = school.get("start_date", "")
                end_date = school.get("end_date", "")
                if school_name:
                    education_text += f"│ - {school_name}: {degree} ({start_date} - {end_date})\n"
            education_text += "╰─────────────⭓"

        # Tạo phần thông tin nơi ở
        living_text = ""
        if living:
            living_text = "╭─────────────⭓\n"\
                          "│ Nơi ở:\n"
            for place in living:
                place_name = place["name"]
                living_text += f"│ - {place_name}\n"
            living_text += "╰─────────────⭓"

        # Tạo phần thông tin sở thích
        interested_in_text = ""
        if interested_in:
            interested_in_text = "╭─────────────⭓\n"\
                                 "│ Sở thích:\n"
            for interest in interested_in:
                interest_name = interest
                interested_in_text += f"│ - {interest_name}\n"
            interested_in_text += "╰─────────────⭓"

        # Tạo phần thông tin like
        likes_text = "╭─────────────⭓\n"\
                     "│ Những người đã like:\n"
        for like in likes:
            name = like["name"]
            category = like["category"]
            link = f"facebook.com/{like['id']}"
            likes_text += f"│ - {name} ({category})\n"
        likes_text += "╰─────────────⭓"

        # Tạo phần thông tin bài viết
        posts_text = "╭─────────────⭓\n"\
                     "│ Bài viết gần đây:\n"
        for post in posts:
            created_time = post.get("created_time", "")
            message = post.get("message", "")
            post_link = post.get("link", "")
            if post_link:
                link = f"Xem bài viết"
            else:
                link = ""
            posts_text += f"│ - {created_time}: {message}\n│   {link}\n"
        posts_text += "╰─────────────⭓"

        # Gửi thông tin
        await update.message.reply_text(info_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        await update.message.reply_text(education_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        await update.message.reply_text(living_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        await update.message.reply_text(interested_in_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        await update.message.reply_text(likes_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        await update.message.reply_text(posts_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        await update.message.reply_text("Không thể lấy thông tin Facebook.", parse_mode=ParseMode.HTML)


# Hàm xử lý lệnh /tt
#https://chongluadao.x10.bz/api/other/admintiktokduyvinh09.php?user={user_id}
#https://iuhchinh.x10.mx/tt.php?user={user_id}
async def tt(update: Update, context: CallbackContext, bot_api=None):
    chat_id = update.effective_chat.id
    user_id = context.args[0].strip() if context.args else None  # Lấy tham số

    # Kiểm tra nếu không có ID hoặc tên người dùng
    if not user_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text='<blockquote><i>❓Sử dụng: /tt user\n💭 Ví dụ: <code>/tt KMB247</code></i></blockquote>',
            parse_mode='HTML',
            reply_to_message_id=update.message.message_id
        )
        return

    url = f'https://iuhchinh.x10.mx/tt.php?user={user_id}'

    try:
        # Gửi trạng thái chờ
        thinking_message = await context.bot.send_message(chat_id=chat_id, text='🔎')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        user_info = data['info']['userInfo']['user']
        stats = data['info']['userInfo']['stats']

        profile_id = user_info['id']
        nickname = user_info['nickname']
        username = user_info['uniqueId']
        avatar = user_info['avatarLarger']
        verified = "Đã xác minh" if user_info['verified'] else "Chưa xác minh"
        create_time = datetime.fromtimestamp(user_info['createTime']).strftime('%H:%M:%S | %d/%m/%Y')
        bio = user_info['signature']
        followers = stats['followerCount']
        following = stats['followingCount']
        friends = stats['friendCount']
        likes = stats['heart']
        videos = stats['videoCount']
        region = user_info['region']
        language = user_info['language']
        last_updated = datetime.now().strftime('%H:%M:%S | %d/%m/%Y')  # Cập nhật thời gian hiện tại

        status = """
| -> Tài khoản này đang ở chế độ Công Khai
| -> Là tài khoản Cá Nhân
| -> Không có danh sách phát
| -> Danh sách following đã bị ẩn
"""

        message = f"""
<blockquote>
╭─────────────⭓
│ 𝗜𝗗: {profile_id}
│ 𝗡𝗮𝗺𝗲: <a href="{avatar}">{nickname}</a>
│ 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}
│ 𝗟𝗶𝗻𝗸: https://www.tiktok.com/@{username}
│ 𝗩𝗲𝗿𝗶𝗳𝗶𝗲𝗱: {verified}
│ 𝗦𝘁𝗮𝘁𝘂𝘀:{status}│ 𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗧𝗶𝗺𝗲: {create_time}
│ 𝗕𝗶𝗼: {bio}
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀: {followers} Follower
│ 𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴: {following} Đang Follow
│ 𝗙𝗿𝗶𝗲𝗻𝗱𝘀: {friends} Bạn Bè
│ 𝗟𝗶𝗸𝗲𝘀: {likes} Thích
│ 𝗩𝗶𝗱𝗲𝗼𝘀: {videos} Video
├─────────────⭔
| 𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲: {language}
| 𝗥𝗲𝗴𝗶𝗼𝗻: {region}
| 𝗡𝗮𝗺𝗲 𝗨𝗽𝗱𝗮𝘁𝗲: {last_updated}
╰─────────────⭓
</blockquote>
"""

        # Tạo nút nằm ngang
        keyboard = [
            [
                InlineKeyboardButton("➕ ADD ME", url='https://t.me/kmb_tienich_bot?startgroup=true'),
                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(chat_id=chat_id, photo=avatar, caption=message, parse_mode='HTML', reply_to_message_id=update.message.message_id, reply_markup=reply_markup)

        # Xóa thông báo trạng thái chờ
        await context.bot.delete_message(chat_id=chat_id, message_id=thinking_message.message_id)

    except Exception as error:
        await context.bot.send_message(chat_id=chat_id, text=f'LỖI: {error}', reply_to_message_id=update.message.message_id)

#XỬ LÝ LỆNH CHECKVAR
def read_transactions(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

async def checkvar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if not context.args:
            await update.message.reply_text("<blockquote> Sử dụng : /checkvar {HỌ VÀ TÊN HOẶC SỐ TIỀN} </blockquote>", parse_mode='HTML')
            return

        query = ' '.join(context.args)
        transactions = read_transactions('ungho.json')

        # Chuyển đổi số tiền thành định dạng có dấu phẩy
        formatted_query = query.replace(',', '').replace(' ', '')

        matched_transactions = [
            transaction for transaction in transactions 
            if query in transaction['c'] or 
               formatted_query == str(transaction['am']).replace(',', '')
        ]

        if not matched_transactions:
            await update.message.reply_text("Không tìm thấy giao dịch nào với truy vấn đã cho.")
            return

        response_parts = []
        response = "<blockquote>"

        for transaction in matched_transactions:
            response += f"<b>Ngày:</b> {transaction['d']}\n"
            response += f"<b>Mã GD:</b> {transaction['no']}\n"
            response += f"<b>Số tiền:</b> {transaction['am']}\n"
            response += f"<b>Nội dung:</b> {transaction['c']}\n\n"

            if len(response) > 4096:
                response += "</blockquote>"
                response_parts.append(response)
                response = "<blockquote>"

        response += "</blockquote>"
        response_parts.append(response)

        for part in response_parts:
            await update.message.reply_text(part, parse_mode='HTML')

    except Exception as e:
        await update.message.reply_text("LỖI: " + str(e))

async def bb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cau_hoi = ' '.join(context.args)
    
    if not cau_hoi:
        await update.message.reply_text("/bb [Câu hỏi]")
        return

    # Hiển thị trạng thái "Đang gõ..."
    await update.message.chat.send_action("typing")
    
    url = f"https://teleserviceapi.vercel.app/gpt?text={cau_hoi}&type=bbai"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            message = data.get("message")
            if message:
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("LỖI RỒI, CHỜ TÔI XEM LẠI!!")
        else:
            await update.message.reply_text("Lỗi. Liên Hệ Admin : @khangmb247")
    except json.JSONDecodeError as e:
        await update.message.reply_text(f"LỖI: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"LỖI: {str(e)}")

async def tbp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cau_hoi = ' '.join(context.args)
    
    if not cau_hoi:
        await update.message.reply_text("/tbp [Câu hỏi]")
        return

    # Hiển thị trạng thái "Đang gõ..."
    await update.message.chat.send_action("typing")
    
    url = f"https://teleserviceapi.vercel.app/gpt?text={cau_hoi}&type=tbcai"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            message = data.get("message")
            if message:
                # Thay thế từ cấm nếu có
                message = message.replace("@Teleservices_Api", "trợ lý AI của tôi")
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("LỖI RỒI, CHỜ TÔI XEM LẠI.")
        else:
            await update.message.reply_text("LH Admin : @khangmb247")
    except json.JSONDecodeError as e:
        await update.message.reply_text(f"LỖI: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"LỖI: {str(e)}")




def escape_markdown_v2(text):
    # Escape các ký tự đặc biệt cho MarkdownV2
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

async def gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cau_hoi = ' '.join(context.args)
    
    if not cau_hoi:
        await update.message.reply_text("<blockquote>/gpt [Câu hỏi]</blockquote>", parse_mode="HTML")
        return

    await update.message.chat.send_action("typing")
    
    url = f"https://gpt.nepdevsnepcoder.workers.dev/?question={cau_hoi}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            message = data.get("answer")
            if message:
                # Escape các ký tự đặc biệt cho MarkdownV2
                escaped_message = escape_markdown_v2(message)

                # Chia tin nhắn nếu nó dài hơn 4096 ký tự
                max_length = 4096
                for i in range(0, len(escaped_message), max_length):
                    await update.message.reply_text(f"```\n{escaped_message[i:i + max_length]}\n```", parse_mode='MarkdownV2')
            else:
                await update.message.reply_text("<blockquote>LỖI RỒI, CHỜ TÔI XEM LẠI!!</blockquote>", parse_mode="HTML")
        else:
            await update.message.reply_text("<blockquote>Liên Hệ Admin : @khangmb247</blockquote>", parse_mode="HTML")
    except json.JSONDecodeError as e:
        await update.message.reply_text(f"LỖI: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"LỖI: {str(e)}")

async def gemi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cau_hoi = ' '.join(context.args)
    
    if not cau_hoi:
        await update.message.reply_text("<blockquote>/gemi [Câu hỏi]</blockquote>", parse_mode="HTML")
        return

    await update.message.chat.send_action("typing")
    
    url = f"https://api.pikaapis.my.id/gemini.php?prompt={cau_hoi}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            message = data.get("content")
            if message:
                # Escape các ký tự đặc biệt cho MarkdownV2
                escaped_message = escape_markdown_v2(message)

                # Chia tin nhắn nếu nó dài hơn 4096 ký tự
                max_length = 4096
                for i in range(0, len(escaped_message), max_length):
                    await update.message.reply_text(f"```\n{escaped_message[i:i + max_length]}\n```", parse_mode='MarkdownV2')
            else:
                await update.message.reply_text("<blockquote>LỖI RỒI, CHỜ TÔI XEM LẠI!!</blockquote>", parse_mode="HTML")
        else:
            await update.message.reply_text("<blockquote>Liên Hệ Admin : @khangmb247</blockquote>", parse_mode="HTML")
    except json.JSONDecodeError as e:
        await update.message.reply_text(f"LỖI: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"LỖI: {str(e)}")


async def php_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cau_hoi = ' '.join(context.args)
    
    if not cau_hoi:
        await update.message.reply_text("<blockquote>/php  [Câu hỏi]</blockquote>", parse_mode="HTML")
        return

    # Hiển thị trạng thái "Đang gõ..."
    await update.message.chat.send_action("typing")
    
    url = f"https://teleserviceapi.vercel.app/gpt?text={cau_hoi}&type=phpai"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            message = data.get("message")
            if message:
                # Thay thế từ cấm nếu có
                message = message.replace("@Teleservices_Api", "trợ lý AI của tôi")
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("LỖI RỒI, CHỜ TÔI XEM LẠI!!")
        else:
            await update.message.reply_text("Liên Hệ Admin : @khangmb247")
    except json.JSONDecodeError as e:
        await update.message.reply_text(f"LỖI: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"LỖI: {str(e)}")

async def query_api(update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str):
    cau_hoi = ' '.join(context.args)
    
    if not cau_hoi:
        await update.message.reply_text(f"/{mode.lower()} [Câu hỏi]")
        return

    # Hiển thị trạng thái "Đang gõ..."
    await update.message.chat.send_action("typing")
    
    url = f"https://lord-apis.ashlynn.workers.dev/?question={cau_hoi}&mode={mode}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                message = data.get("message")
                if message:
                    await update.message.reply_text(message)
                else:
                    await update.message.reply_text("LỖI RỒI, CHỜ TÔI XEM LẠI!!")
            else:
                await update.message.reply_text("Lỗi. Liên Hệ Admin : @khangmb247")

async def bing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await query_api(update, context, "Bing")

async def llama_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await query_api(update, context, "Llama")

async def qwen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await query_api(update, context, "Qwen")









#Lệnh /yt
# Hiển thị trạng thái "Đang gõ..."
async def yt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("<blockquote>❓Sử dụng /yt [Link video]\n💭 Ví dụ: <code>/yt https://www.youtube.com/watch?v=ABC</code></blockquote>", parse_mode="HTML")
        return

    link_video = context.args[0]
    
    # Hiển thị trạng thái "Đang gõ..."
    await update.message.chat.send_action("typing")
    
    url = f"https://yt-music.ashlynn.workers.dev/?url={link_video}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            if data["status"]:
                title = data["data"]["title"]
                author = data["data"]["author"]
                category = data["data"]["category"]
                views = f"{int(data['data']['views']):,}"
                likes = f"{int(data['data']['likes']):,}"
                comments = f"{int(data['data']['comments']):,}"
                download_url = data["data"]["download"]["url"]
                image_url = data["data"]["image"]

                # Tạo tin nhắn
                message = (
                    "<blockquote><b>┏━━━━━━━━━━━━┓\n"
                    "  ━━━━𝐘𝐎𝐔𝐓𝐔𝐁𝐄━━━━\n"
                    "┗━━━━━━━━━━━━┛\n"
                    "┌────⭓\n"
                    f"│» <b>Mô tả</b> : {title}\n"
                    f"│» <b>Tác giả</b> : {author}\n"
                    f"│» <b>Thể loại</b> : {category}\n"
                    f"│» <b>Lượt xem</b> : {views}\n"
                    f"│» <b>Lượt thích</b> : {likes}\n"
                    f"│» <b>Lượt comment</b> : {comments}\n"
                    "└───────────⭓</b></blockquote>"
                )

                # Tạo nút nằm ngang
                keyboard = [
                    [
                        InlineKeyboardButton("💻 TẢI MP3", url=download_url),
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                # Gửi ảnh và tin nhắn chung
                await update.message.reply_photo(photo=image_url, caption=message, parse_mode='HTML', reply_markup=reply_markup)
            else:
                await update.message.reply_text("KHÔNG THẤY THÔNG TIN.")
        else:
            await update.message.reply_text("LỖI API.")
    except Exception as e:
        await update.message.reply_text(f"LỖI: {str(e)}")
    
    # Kết thúc trạng thái "Đang gõ..."
    await update.message.chat.send_action("cancel")

# Lệnh /lyrics
async def lyrics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("<blockquote>❓Sử dụng /lyrics [Tên bài hát]\n💭 Ví dụ: /lyrics Hoàng hôn nhớ</blockquote>", parse_mode="HTML")
        return

    song_title = " ".join(context.args)
    
    # Hiển thị trạng thái "Đang gõ..."
    await update.message.chat.send_action("typing")
    
    url = f"https://lyrist.vercel.app/api/{song_title}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            lyrics = data["lyrics"]
            title = data["title"]
            artist = data["artist"]
            image_url = data["image"]

            # Tạo tin nhắn đầu tiên
            message_header = (
                "<blockquote>┏━━━━━━━━━━━━┓\n"
                "  ━━━━━ʟʏʀɪᴄs━━━━━\n"
                "┗━━━━━━━━━━━━┛\n"
                "┌────⭓\n"
                f"│» <b>Tên bài hát</b> : {title}\n"
                f"│» <b>Tác giả</b> : {artist}\n"
                "└───────────⭓</blockquote>\n\n"
            )

            # Gửi ảnh
            await update.message.reply_photo(photo=image_url, caption=message_header, parse_mode='HTML')

            # Kiểm tra độ dài lời bài hát
            max_length = 4096
            if len(lyrics) > max_length:
                # Cắt lời bài hát thành các phần nhỏ hơn nếu cần
                lyrics_parts = [lyrics[i:i + max_length] for i in range(0, len(lyrics), max_length)]

                # Gửi từng phần lời bài hát
                for part in lyrics_parts:
                    message_body = (
                        "<blockquote>\n"
                        "━━━━𝐋Ờ𝐈 𝐁À𝐈 𝐇Á𝐓━━━━\n"
                        f"<i><tg-spoiler>{part}</tg-spoiler></i>\n"
                        "</blockquote>"
                    )
                    await update.message.reply_text(message_body, parse_mode='HTML')
            else:
                # Gửi lời bài hát trong một tin nhắn nếu ngắn
                message_body = (
                    "<blockquote>\n"
                    "━━━━𝐋Ờ𝐈 𝐁À𝐈 𝐇Á𝐓━━━━\n"
                    f"<i><tg-spoiler>{lyrics}</tg-spoiler></i>\n"
                    "</blockquote>"
                )
                await update.message.reply_text(message_body, parse_mode='HTML')
        else:
            await update.message.reply_text("Không thể lấy lời bài hát.")
    except Exception as e:
        await update.message.reply_text(f"LỖI: {str(e)}")
    
    # Kết thúc trạng thái "Đang gõ..."
    await update.message.chat.send_action("cancel")

async def xuly_image(api_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.json()

async def gui_anh_cat_dog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("upload_photo")  # Hiển thị trạng thái "Đang tải ảnh..."
    
    # Chọn ngẫu nhiên một API
    api_choice = random.choice([
        "https://api.thecatapi.com/v1/images/search"
    ])
    
    if api_choice == "https://api.thecatapi.com/v1/images/search":
        data = await xuly_image(api_choice)
        image_url = data[0]["url"]

    await update.message.reply_photo(photo=image_url)

#Lệnh /timanh
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_query = ' '.join(context.args)
    
    if not search_query:
        await update.message.reply_text("/timanh [Mô tả ảnh]")
        return

    await update.message.chat.send_action("upload_photo")

    url = f"https://api.kenliejugarap.com/pinterestbymarjhun/?search={search_query}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data['status'] and len(data['data']) > 0:
                    images = data['data']
                    
                    # Chọn ngẫu nhiên 10 ảnh từ danh sách
                    selected_images = random.sample(images, min(10, len(images)))  # Lấy tối đa 10 ảnh
                    
                    media = [InputMediaPhoto(media=image_url) for image_url in selected_images]
                    await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)
                else:
                    await update.message.reply_text("Không thấy ảnh.")
            else:
                await update.message.reply_text("LỖI RỒI.")

#Lệnh /taoanhnhanh
async def taoanhnhanh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    description = ' '.join(context.args)
    if not description:
        await update.message.reply_text("/taoanhnhanh [Mô tả tiếng anh]")
        return

    # Tạo URL hình ảnh từ mô tả
    image_url = f"https://image.pollinations.ai/prompt/{description.replace(' ', '%20')}"

    await update.message.chat.send_action("upload_photo")

    # Gửi ảnh từ URL
    await update.message.reply_photo(photo=image_url)

#Lệnh /camhung
async def fetch_quote():
    url = "https://dummyjson.com/quotes/random"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None

async def cam_hung(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("typing")  # Hiển thị trạng thái "Đang gõ..."
    
    quote_data = await fetch_quote()
    
    if quote_data:
        quote = quote_data['quote']
        formatted_quote = f"<tg-spoiler><blockquote><i>┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n  {quote}\n┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛</i></blockquote></tg-spoiler>"
        await update.message.reply_text(formatted_quote, parse_mode='HTML')
    else:
        await update.message.reply_text("LỖI khi lấy câu trích dẫn.")

#Lệnh /laytheme
async def laytheme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Vui lòng cung cấp link web.")
        return

    link_web = context.args[0]
    api_url = f"https://teleservicesapi.vercel.app/copy?url={link_web}"

    await update.message.chat.send_action("upload_document")

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                if data["status"] == "Success":
                    # Lấy URL từ phản hồi
                    file_url = data["url"]
                    file_id = file_url.split('/')[-1]  # Lấy phần cuối của URL
                    download_link = f"https://copier.saveweb2zip.com/api/downloadArchive/{file_id}"

                    # Tải file zip
                    async with session.get(download_link) as zip_response:
                        if zip_response.status == 200:
                            zip_content = await zip_response.read()
                            # Gửi file zip cho người dùng
                            await update.message.reply_document(document=zip_content, filename="archive.zip")
                        else:
                            await update.message.reply_text("Không thể tải file zip.")
            else:
                await update.message.reply_text("LỖI khi truy cập API.")

#lệnh /tuoi
async def tuoi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("<blockquote>❓Sử dụng /tuoi [tên].\n💭 Ví dụ: <code>/tuoi Khang</code></blockquote>", parse_mode="HTML")
        return

    full_name = " ".join(context.args)
    api_url = f"https://api.agify.io/?name={full_name}"

    await update.message.chat.send_action("typing")  # Hiển thị trạng thái "Đang gõ..."

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                age = data.get("age", "Không xác định")
                
                # Xác định câu nhận xét dựa trên độ tuổi
                if age < 10:
                    comment = "Còn non lắm bé ơi"
                elif age < 20:
                    comment = "Trẻ trâu"
                elif age < 30:
                    comment = "Tạm trẻ đó"
                elif age < 40:
                    comment = "Hơi già nhé"
                elif age < 50:
                    comment = "Cũng gần xuống lỗ"
                elif age < 70:
                    comment = "Xuống lỗ chưa"
                else:
                    comment = "Sao sống nhây vcl"

                # Tạo tin nhắn định dạng
                message = (
                    "<blockquote>\n"
                    "┏━━━━━━━━━━━━┓\n"
                    "    ━━━━Độ Tuổi━━━━\n"
                    f"│» <b>Tên</b> : <u>{full_name}</u>\n"
                    f"│» <b>Tuổi</b> : <tg-spoiler>{age}</tg-spoiler>\n"
                    f"│» <b><tg-spoiler>{comment}</tg-spoiler></b>\n"
                    "┗━━━━━━━━━━━━┛\n"
                    "</blockquote>"
                )

                await update.message.reply_text(message, parse_mode='HTML')
            else:
                await update.message.reply_text("LỖI khi truy cập API.")

#Lệnh /down tải đa nền tảng
async def lay_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) == 0:
            await update.message.reply_text("/down {link video}.")
            return

        link_video = context.args[0]
        api_url = f"https://tele-social.vercel.app/down?url={link_video}"

        await update.message.chat.send_action("upload_video")  # Hiển thị trạng thái "Đang tải video..."

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    platform = data.get("platform")

                    if platform in ["TikTok", "Facebook"]:
                        video_url = data["data"]["urls"][0]
                        caption = f"Video từ {platform}"

                        # Tạo nút nằm ngang
                        keyboard = [
                            [
                                InlineKeyboardButton("➕ ADD ME", url='https://t.me/chuyenittest_bot?startgroup=true'),
                                InlineKeyboardButton("👤 ADMIN", url='https://t.me/chuyenit')
                            ]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        # Gửi video với nút nằm ngang
                        await context.bot.send_video(
                            chat_id=update.effective_chat.id,
                            video=video_url,
                            caption=caption,
                            supports_streaming=True,
                            reply_to_message_id=update.message.message_id,
                            reply_markup=reply_markup
                        )

                    elif platform == "Instagram":
                        urls = data["data"]["urls"]

                        # Tạo danh sách các InputMediaPhoto
                        media_group = [InputMediaPhoto(media=url) for url in urls]

                        # Gửi media group
                        await context.bot.send_media_group(
                            chat_id=update.effective_chat.id,
                            media=media_group,
                            reply_to_message_id=update.message.message_id
                        )

                        # Tạo nút nằm ngang
                        keyboard = [
                            [
                                InlineKeyboardButton("➕ ADD ME", url='https://t.me/chuyenittest_bot?startgroup=true'),
                                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                            ]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        # Gửi tin nhắn mới với nút nằm ngang
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="",
                            reply_markup=reply_markup,
                            reply_to_message_id=update.message.message_id
                        )

                else:
                    await update.message.reply_text("LỖI khi truy cập API.")

    except Exception:
        pass

#Lệnh /spotify 
async def fetch_audio_link(spotify_url):
    api_url = f"https://dl.pikaapis.my.id/spotify.php?url={spotify_url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("<blockquote>❓Sử dụng /spotify [link nhạc]\n💭 Ví dụ: <code>/spotify https://open.spotify.com/track/ABC</code></blockquote>", parse_mode="HTML")
        return

    spotify_url = context.args[0]
    await update.message.chat.send_action("upload_audio")

    audio_data = await fetch_audio_link(spotify_url)

    if audio_data and "result" in audio_data:
        result = audio_data['result']
        download_link = result['url']
        image_url = result['image']
        song_name = result['name']
        artist_name = result['artists']
        duration_ms = result['duration_ms']

        # Tạo thông điệp với thông tin bài hát
        song_info_message = (
            f"<blockquote><b>Tên bài hát:</b> {song_name}\n"
            f"<b>Tác giả:</b> {artist_name}\n"
            f"<b>Thời lượng:</b> {duration_ms // 1000} giây</blockquote>"
        )

        # Tạo bàn phím inline
        keyboard = [
            [
                InlineKeyboardButton("🎧 TẢI NHẠC", url=download_link),
                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Gửi ảnh và thông tin bài hát trong cùng một tin nhắn
        await update.message.reply_photo(photo=image_url, caption=song_info_message, parse_mode='HTML', reply_markup=reply_markup)

        # Gửi file audio trực tiếp từ link
        await update.message.reply_audio(audio=download_link)
    else:
        await update.message.reply_text("<blockquote>KHÔNG THỂ GỬI NHẠC.</blockquote>", parse_mode="HTML")

#Lệnh /timnhac
async def fetch_song_data(song_name):
    api_url = f"https://spotifyapi.nepdevsnepcoder.workers.dev/?songname={song_name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

async def timnhac(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("<blockquote>❓Sử dụng /timnhac [Tên bài hát]\n💭 Ví dụ: <code>/timnhac Hoàng hôn nhớ</code></blockquote>", parse_mode="HTML")
        return

    song_name = " ".join(context.args)
    
    # Gửi hành động "typing"
    await update.message.chat.send_action("typing")

    song_data = await fetch_song_data(song_name)

    if song_data and isinstance(song_data, list):
        # Lấy tối đa 3 bài hát
        for song in song_data[:3]:  # Chỉ lấy 3 bài hát đầu tiên
            image_url = song['image_url']
            song_name = song['song_name']
            artist_name = song['artist_name']
            release_date = song['release_date']
            popularity = song['popularity']
            song_url = song['song_url']
            download_link = song['download_link']

            # Tạo nội dung tin nhắn
            message = (
                f"<blockquote><b>Tên bài hát:</b> {song_name}\n"
                f"<b>Tác giả:</b> {artist_name}\n"
                f"<b>Ngày phát hành:</b> {release_date}\n"
                f"<b>Phổ biến:</b> {popularity}%\n"
                f"<a href='{song_url}'>Nghe nhạc</a>\n"
                f"<a href='{download_link}'>Tải nhạc</a></blockquote>"
            )

            # Gửi ảnh và nội dung
            await update.message.reply_photo(photo=image_url, caption=message, parse_mode='HTML')
    else:
        await update.message.reply_text("<blockquote>Không tìm thấy bài hát</blockquote>", parse_mode="HTML")


async def check_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip = context.args[0] if context.args else None
    if not ip:
        await update.message.reply_text(f"<blockquote>❓Sử dụng /checkip [ip]\n💭 Ví dụ: <code>/checkip 103.123.123.123</code></blockquote>", parse_mode="HTML")
        return

    await update.message.chat.send_action("typing")

    api_url = f"https://bj-devs.serv00.net/Ip-Info.php?ip={ip}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                photo_url = data['country_flag']
                message = (
                    "<blockquote expandable>\n"
                    "┌────⭓\n"
                    f"│        ━━━IP━━━\n"
                    f"│» <b>IP :</b> {data['ip']}\n"
                    f"│» <b>Mã lục địa :</b> {data['continent_code']}\n"
                    f"│» <b>Tên lục địa :</b> {data['continent_name']}\n"
                    f"│» <b>Mã quốc gia :</b> {data['country_code2']}\n"
                    f"│» <b>Tên quốc gia :</b> {data['country_name']}\n"
                    f"│» <b>Biểu ngữ :</b> {data['country_name_official']}\n"
                    f"│» <b>Thủ đô :</b> {data['country_capital']}\n"
                    f"│» <b>Thành phố :</b> {data['state_prov']}\n"
                    f"│» <b>Mã thành phố :</b> {data['state_code']}\n"
                    f"│» <b>Mã zip :</b> {data['zipcode']}\n"
                    f"│» <b>Vĩ độ :</b> {data['latitude']}\n"
                    f"│» <b>Kinh độ :</b> {data['longitude']}\n"
                    f"│» <b>Link bản đồ :</b> <a href=\"https://www.google.com/maps/search/?api=1&query={data['latitude']},{data['longitude']}\">Xem bản đồ</a>\n"
                    f"│» <b>Đầu số :</b> {data['calling_code']}\n"
                    f"│» <b>Thuộc EU :</b> {'có' if data['is_eu'] else 'không'}\n"
                    f"│» <b>Đuôi miền quốc gia :</b> {data['country_tld']}\n"
                    f"│» <b>Ngôn ngữ :</b> {data['languages']}\n"
                    f"│» <b>ID địa lý :</b> {data['geoname_id']}\n"
                    f"│» <b>Nhà cung cấp :</b> {data['isp']}\n"
                    f"│» <b>Kiểu kết nối :</b> {data['connection_type']}\n"
                    f"│» <b>Tổ chức :</b> {data['organization']}\n"
                    f"│» <b>Biểu tượng :</b> {data['country_emoji']}\n"
                    f"│» <b>Tiền tệ</b>\n"
                    f"│»          ✪ <b>Đơn vị :</b> {data['currency']['code']}\n"
                    f"│»          ✪ <b>Tên gọi :</b> {data['currency']['name']}\n"
                    f"│»          ✪ <b>Ký hiệu :</b> {data['currency']['symbol']}\n"
                    f"│» <b>Múi giờ</b>\n"
                    f"│»          ✪ <b>Tên :</b> {data['time_zone']['name']}\n"
                    f"│»          ✪ <b>Chênh lệch :</b> {data['time_zone']['offset_with_dst']}\n"
                    f"│»          ✪ <b>Thời gian hiện tại :</b> {data['time_zone']['current_time']}\n"
                    "└───────────⭓\n"
                    "</blockquote>"
                )

                await update.message.reply_photo(photo=photo_url, caption=message, parse_mode='HTML')
            else:
                await update.message.reply_text("Không thấy thông tin IP.")

async def check_car_info(bsx: str):
    url = f'https://vietcheckcar.com/api/api.php?api_key=sfund&bsx={bsx}&bypass_cache=0&loaixe=1&vip=0'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def bsx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Gửi hành động "typing"
    await update.message.chat.send_action("typing")

    try:
        # Lấy biển số từ tin nhắn
        bsx = context.args[0] if context.args else None
        if not bsx:
            await update.message.reply_text(f"<blockquote>❓ /bsx [BIỂN SỐ]\n💭 Ví dụ : /bsx 60C-628.72</blockquote>", parse_mode="HTML")
            return

        # Gọi API và lấy kết quả
        car_info = await check_car_info(bsx)

        # Kiểm tra nếu có vi phạm
        if car_info.get('totalViolations', 0) > 0:
            # Lấy thông tin vi phạm đầu tiên
            violation = car_info['violations'][0]

            # Trích xuất thông tin từ JSON
            bien_so = violation.get('bien_kiem_sat', 'N/A')
            trang_thai = violation.get('trang_thai', 'N/A')
            mau_bien = violation.get('mau_bien', 'N/A')
            loai_phuong_tien = violation.get('loai_phuong_tien', 'N/A')
            thoi_gian_vi_pham = violation.get('thoi_gian_vi_pham', 'N/A')
            dia_diem_vi_pham = violation.get('dia_diem_vi_pham', 'N/A')
            hanh_vi_vi_pham = violation.get('hanh_vi_vi_pham', 'N/A')
            don_vi_phat_hien_vi_pham = violation.get('don_vi_phat_hien_vi_pham', 'N/A')
            noi_giai_quyet_vu_viec = violation.get('noi_giai_quyet_vu_viec', 'N/A').replace('\\n', '\n')
            so_dien_thoai = violation.get('so_dien_thoai', 'N/A')
            muc_phat = violation.get('muc_phat', 'N/A')

            # Lấy kinh độ và vĩ độ từ địa điểm vi phạm
            coords = re.search(r'\(([^;]+); ([^)]+)\)', dia_diem_vi_pham)
            latitude = coords.group(1) if coords else '0'
            longitude = coords.group(2) if coords else '0'

            # Định dạng tin nhắn
            message_text = f'''
<blockquote expandable>
┌────⭓
│        ━━━<b>THÔNG TIN VI PHẠM</b>━━━
│» <b> Biển số:</b> {bien_so}
│» <b> Trạng thái:</b> {trang_thai}
│» <b> Màu biển:</b> {mau_bien}
│» <b> Loại phương tiện:</b> {loai_phuong_tien}
│» <b> Thời gian vi phạm:</b> {thoi_gian_vi_pham}
│» <b> Địa điểm vi phạm:</b> {dia_diem_vi_pham}
│» <b>Link bản đồ:</b> <a href="https://www.google.com/maps/search/?api=1&query={latitude},{longitude}">Xem nơi vi phạm</a>
│» <b> Hành vi vi phạm:</b> {hanh_vi_vi_pham}
│» <b> Đơn vị phát hiện vi phạm:</b> {don_vi_phat_hien_vi_pham}
│» <b> Nơi giải quyết vụ việc:</b><tg-spoiler><i><u>{noi_giai_quyet_vu_viec}</u></i></tg-spoiler>│» <b> Số điện thoại:</b> {so_dien_thoai}
│» <b> Mức phạt:</b> {muc_phat}
└───────────⭓
</blockquote>'''

            # Gửi tin nhắn với thông tin
            await update.message.reply_text(message_text, parse_mode="HTML")
        else:
            await update.message.reply_text(f"<blockquote>Biển số xe {bsx} không có lỗi vi phạm.</blockquote>", parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text(f"LỖI: {str(e)}")

# Hàm xử lý lệnh /qr
async def qr(update: Update, context: CallbackContext) -> None:
    # Lấy văn bản từ lệnh
    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("<blockquote>❓Sử dụng /qr [văn bản]\n💭 Ví dụ: <code>/qr KMB247</code></blockquote>", parse_mode="HTML")
        return

    # Gọi API để tạo QR code
    api_url = f"https://api.pikaapis.my.id/QrMaker.php?text={text}"
    response = requests.get(api_url)
    data = response.json()

    # Lấy URL của ảnh QR code
    qr_image_url = data.get("qrImageUrl")
    if qr_image_url:
        # Gửi ảnh QR code
        await update.message.chat.send_action("upload_photo")
        await update.message.reply_photo(photo=qr_image_url)
    else:
        await update.message.reply_text("<blockquote>Không được tạo QR code.</blockquote>", parse_mode="HTML")

# Hàm xử lý lệnh /ytb_audio
async def ytb_audio(update: Update, context: CallbackContext) -> None:
    # Lấy link video từ lệnh
    if not context.args:
        await update.message.reply_text("<blockquote>❓Sử dụng /ytb_audio [Link video].\n💭 Ví dụ: <code>/ytb_audio https://www.youtube.com/watch?v=ABC</code></blockquote>", parse_mode="HTML")
        return

    video_url = ' '.join(context.args)

    # Gọi API để lấy audio từ video YouTube
    api_url = f"https://api.bots.business/v2/bots/1718425/web-app/downloader_ytAudio?url={video_url}"
    response = requests.get(api_url)
    data = response.json()

    # Kiểm tra trạng thái và lấy link audio
    if data.get("status"):
        audio_result = data["data"][0]["result"]
        
        # Gửi trạng thái đang tải audio
        await update.message.chat.send_action("upload_audio")
        
        try:
            # Gửi audio cho người dùng
            await update.message.reply_audio(audio=audio_result)
        except Exception as e:
            # Nếu có lỗi xảy ra, gửi thông báo với nút tải nhạc
            await update.message.reply_text(
                "Audio quá dài, tự tải nghe đi",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🎧 TẢI NHẠC", url=audio_result),
                        InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                    ]
                ])
            )
            print(f"LỖI: {e}")
    else:
        await update.message.reply_text("<blockquote>Không thể tải lấy audio.</blockquote>", parse_mode="HTML")

# Hàm xử lý lệnh /downx
async def downx(update: Update, context: CallbackContext) -> None:
    # Kiểm tra nếu có link video được cung cấp
    if not context.args:
        await update.message.reply_text("<blockquote>❓Sử dụng /downx [link video]\n💭 Ví dụ: <code>/downx https://x.com/ABC</code></blockquote>", parse_mode="HTML")
        return

    video_url = ' '.join(context.args)

    # Gọi API để tải video từ X (Twitter)
    api_url = f"https://api.bots.business/v2/bots/1718425/web-app/downloader_twitter?url={video_url}"
    response = requests.get(api_url)
    data = response.json()

    # Kiểm tra trạng thái và lấy link video
    if data.get("status"):
        video_result = data["data"][0]["result"]

        # Gửi trạng thái đang tải video
        await update.message.chat.send_action("upload_video")

        try:
            # Tạo keyboard với các nút "Thêm bot" và "Admin"
            keyboard = [
                [
                    InlineKeyboardButton("➕ ADD ME", url='https://t.me/kmb_tienich_bot?startgroup=true'),
                    InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Gửi video cho người dùng
            await update.message.reply_video(video=video_result, reply_markup=reply_markup)
        except Exception as e:
            # Nếu video quá dài hoặc timeout, gửi đường link cho người dùng
            await update.message.reply_text(
                "<blockquote>VIDEO QUÁ DÀI, XEM Ở LINK DƯỚI</blockquote>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📹 TẢI VIDEO", url=video_result),
                        InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                    ]
                ])
            )
            print(f"Lỗi gửi video: {e}")
    else:
        await update.message.reply_text("<blockquote>Không thể tải video.</blockquote>", parse_mode="HTML")

# Hàm xử lý lệnh /downig
async def downig(update: Update, context: CallbackContext) -> None:
    # Kiểm tra nếu có link video được cung cấp
    if not context.args:
        await update.message.reply_text("<blockquote>❓Sử dụng /downig [link video]\n💭 Ví dụ: <code>/downig https://www.instagram.com/reel/ABC</code></blockquote>", parse_mode="HTML")
        return

    video_url = ' '.join(context.args)

    # Gọi API để tải video từ X (Twitter)
    api_url = f"https://api.bots.business/v2/bots/1718425/web-app/downloader_instagram?url={video_url}"
    response = requests.get(api_url)
    data = response.json()

    # Kiểm tra trạng thái và lấy link video
    if data.get("status"):
        video_result = data["data"][0]["result"]

        # Gửi trạng thái đang tải video
        await update.message.chat.send_action("upload_video")

        try:
            # Tải video vào tệp tin tạm thời
            with open('video.mp4', 'wb') as f:
                f.write(requests.get(video_result).content)

            # Tạo keyboard với các nút "Thêm bot" và "Admin"
            keyboard = [
                [
                    InlineKeyboardButton("➕ ADD ME", url='https://t.me/kmb_tienich_bot?startgroup=true'),
                    InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Gửi video cho người dùng
            with open('video.mp4', 'rb') as f:
                await update.message.reply_video(video=f, filename='video.mp4', reply_markup=reply_markup)

            # Xóa tệp tin tạm thời
            os.remove('video.mp4')
        except Exception as e:
            # Nếu video quá dài hoặc timeout, gửi đường link cho người dùng
            await update.message.reply_text(
                "<blockquote>VIDEO QUÁ DÀI, XEM Ở LINK DƯỚI</blockquote>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📹 XEM VIDEO", url=video_result),
                        InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                    ]
                ])
            )
            print(f"Lỗi gửi video: {e}")
    else:
        await update.message.reply_text("<blockquote>Không thể tải video.</blockquote>", parse_mode="HTML")

# Hàm xử lý lệnh /downfb
async def downfb(update: Update, context: CallbackContext) -> None:
    # Kiểm tra nếu có link video được cung cấp
    if not context.args:
        await update.message.reply_text("<blockquote>❓Sử dụng /downfb [link video]\n💭 Ví dụ: <code>/downfb https://www.facebook.com/share/ABC</code></blockquote>", parse_mode="HTML")
        return

    video_url = ' '.join(context.args)

    # Gọi API để tải video từ X (Twitter)
    api_url = f"https://api.bots.business/v2/bots/1718425/web-app/downloader_facebook?url={video_url}"
    response = requests.get(api_url)
    data = response.json()

    # Kiểm tra trạng thái và lấy link video
    if data.get("status"):
        video_result = data["data"][0]["result"]

        # Gửi trạng thái đang tải video
        await update.message.chat.send_action("upload_video")

        try:
            # Tải video vào tệp tin tạm thời
            with open('video.mp4', 'wb') as f:
                f.write(requests.get(video_result).content)

            # Tạo keyboard với các nút "Thêm bot" và "Admin"
            keyboard = [
                [
                    InlineKeyboardButton("➕ ADD ME", url='https://t.me/kmb_tienich_bot?startgroup=true'),
                    InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Gửi video cho người dùng
            with open('video.mp4', 'rb') as f:
                await update.message.reply_video(video=f, filename='video.mp4', reply_markup=reply_markup)

            # Xóa tệp tin tạm thời
            os.remove('video.mp4')
        except Exception as e:
            # Nếu video quá dài hoặc timeout, gửi đường link cho người dùng
            await update.message.reply_text(
                "<blockquote>VIDEO QUÁ DÀI, XEM Ở LINK DƯỚI</blockquote>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📹 XEM VIDEO", url=video_result),
                        InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
                    ]
                ])
            )
            print(f"Lỗi gửi video: {e}")
    else:
        await update.message.reply_text("<blockquote>Không thể tải video.</blockquote>", parse_mode="HTML")

async def ig(update: Update, context: CallbackContext) -> None:
    # Kiểm tra nếu có username được cung cấp
    if not context.args:
        await update.message.reply_text("<blockquote>❓Sử dụng /ig [username]\n💭 Ví dụ: /ig KMB247</blockquote>", parse_mode="HTML")
        return

    username = ' '.join(context.args)

    # Gửi trạng thái đang gõ
    await update.message.chat.send_action("typing")

    # Gọi API để lấy thông tin Instagram
    api_url = f"https://api.pikaapis.my.id/instadp.php?username={username}"
    response = requests.get(api_url)
    data = response.json()

    if data.get("status") == "success":
        # Lấy thông tin từ API
        profile_pic_url = data["profile_pic_url"]
        full_name = data["full_name"]
        biography = data["biography"]
        follower_count = data["follower_count"]
        following_count = data["following_count"]
        facebook_id = data["facebook_id"]
        is_verified = data["is_verified"]

        # Tạo nội dung thông tin
        info_text = f"<blockquote>"\
                    f"╭─────────────⭓\n"\
                    f"│ <b>User:</b> {username}\n"\
                    f"│ <b>Tên:</b> {full_name}\n"\
                    f"│ <b>Tiểu sử:</b> {biography}\n"\
                    f"│ <b>Người theo dõi:</b> {follower_count}\n"\
                    f"│ <b>Đang theo dõi:</b> {following_count}\n"\
                    f"│ <b>ID Facebook:</b> {facebook_id}\n"\
                    f"│ <b>Trạng thái:</b> {'Đã xác minh✅' if is_verified else 'Chưa xác minh❌'}\n"\
                    f"╰─────────────⭓</blockquote>"

        # Tạo keyboard với các liên kết từ "biography_links"
        keyboard = []
        for link in data["biography_links"]:
            if link["url"] and link["title"]:
                keyboard.append([InlineKeyboardButton(link["title"], url=link["url"])])
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Gửi ảnh và thông tin
        await update.message.reply_photo(photo=profile_pic_url, caption=info_text, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await update.message.reply_text("<blockquote>Không thể lấy thông tin Instagram.</blockquote>", parse_mode="HTML")



# Danh sách đen số điện thoại
blacklist = ["112", "113", "114", "115", "116", "117", "118", "119", "0", "1", "2", "3", "4"]
# Khởi tạo một từ điển để theo dõi số lần sử dụng lệnh
user_usage = defaultdict(list)
async def smskmb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    current_time = time.time()

    # Kiểm tra xem người dùng có phải là ADMIN không
    if user_id == ADMIN_ID:
        # Tiến hành như bình thường cho ADMIN
        return await handle_smskmb(update, context)

    # Lọc ra các lần sử dụng trong 1 phút qua
    user_usage[user_id] = [timestamp for timestamp in user_usage[user_id] if current_time - timestamp < 60]

    # Kiểm tra số lần sử dụng
    if len(user_usage[user_id]) >= 3:
        await update.message.reply_text("<blockquote><i>Spam quá 3 lần 1p. Vui lòng thử lại sau 3p.</i></blockquote>", parse_mode='HTML')
        return

    # Thêm thời gian hiện tại vào danh sách sử dụng
    user_usage[user_id].append(current_time)

    # Gọi hàm xử lý chính
    await handle_smskmb(update, context)

async def handle_smskmb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    params = context.args
    if len(params) != 2:
        await update.message.reply_text("<blockquote>/smskmb [số điện thoại] [số lần]\n💭Ví dụ : <code>/smskmb 0942424242</code></blockquote>", parse_mode='HTML')
        return
    sdt, count = params
    if not count.isdigit():
        await update.message.reply_text("<blockquote><i>Số lần spam không hợp lệ.</i></blockquote>", parse_mode='HTML')
        return
    count = int(count)
    if count > 30:
        await update.message.reply_text("<blockquote><i>TỐI ĐA 30 LẦN.</i></blockquote>", parse_mode='HTML')
        return
    if sdt in blacklist:
        await update.message.reply_text(f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    diggory_chat3 = f'''
<b>🚀SPAM THÀNH CÔNG</b>
<blockquote>
╭─────────────⭓
│ SỐ LẦN : {count}
│ SỐ SPAM :  {sdt}
├─────────────⭔
│ TỐI ĐA 20 LẦN
│ HẠN CHẾ SPAM
╰─────────────⭓
</blockquote>
'''

    script_filename = "api.py"  # Tên file Python trong cùng thư mục
    try:
        if os.path.isfile(script_filename):
            with open(script_filename, 'r', encoding='utf-8') as file:
                script_content = file.read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
                temp_file.write(script_content.encode('utf-8'))
                temp_file_path = temp_file.name

            process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
            # Gửi thông báo vào nhóm
            await context.bot.send_message(GROUP_ID_KIN, f'''
<b>THÔNG BÁO SMS</b>\n
<blockquote>
╭─────────────⭓
│ 👮@{update.message.from_user.username} 
│ 🔰Số điện thoại: {sdt} 
│ ❌Lặp lại: {count} lần.
╰─────────────⭓
</blockquote>
            ''', parse_mode='HTML')
            await update.message.reply_text(diggory_chat3, parse_mode='HTML')
        else:
            await update.message.reply_text("Tập tin không tìm thấy.")
    except Exception as e:
        await update.message.reply_text(f"Lỗi xảy ra: {str(e)}")


async def demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effect_id = '5104841245755180586'  # ID hiệu ứng bạn muốn sử dụng
    demo_text = "🌟 Đây là tin nhắn demo với hiệu ứng! 🔥"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=demo_text,
        reply_markup=None,
        disable_notification=False,
        message_effect_id=effect_id  # Sử dụng ID hiệu ứng
    )

###########
async def on_update(data, bot_api):
    if 'message' in data:
        content = data['message']
        chat_id = content['chat']['id']
        message_id = content['message_id']
        text = content.get('text', '')

        # Gọi hàm xử lý lệnh proxy
        if text == "/code":
            await code(content, bot_api)
        if text == "/id":
            await id(content, bot_api)
        if text == "/tv":
            await tieng_viet(content, bot_api)
        if text == "/2fa":
            await send_2fa(content, bot_api)
        if text == "/tiktok":
            await luuvideo_tiktok(content, bot_api)
        if text == "/thoitiet":
            await thoitiet(content, bot_api)
###########
# Đăng ký lệnh
async def start_bot():
    bot_api = TelegramBotAPI(TOKEN)
    application = ApplicationBuilder().token(TOKEN).build()

    # Thêm các handler cho các lệnh
    application.add_handler(CommandHandler("start", help))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("trollvn", trollvn))
    application.add_handler(CommandHandler("voice", voice))
    application.add_handler(CommandHandler('time', thoigianhdbot))
    application.add_handler(CommandHandler("code", lambda update, context: code(update, context, bot_api)))
    application.add_handler(CommandHandler("id", lambda update, context: id(update, context, bot_api)))
    application.add_handler(CommandHandler("tv", lambda update, context: tieng_viet(update, context, bot_api)))
    application.add_handler(CommandHandler("2fa", lambda update, context: send_2fa(update, context, bot_api)))
    application.add_handler(CommandHandler("upanh", cmd_upanh))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(CommandHandler("tiktok", lambda update, context: luuvideo_tiktok(update, context, bot_api)))
    application.add_handler(CommandHandler("thoitiet", lambda update, context: thoitiet(update, context, bot_api)))
    application.add_handler(CommandHandler('hoi', hoi))
    application.add_handler(MessageHandler(filters.REPLY, reply_handler))
    application.add_handler(CommandHandler('bank', lenhbank))
    application.add_handler(CommandHandler("proxy", proxy))
    application.add_handler(CommandHandler("fb", fb))
    application.add_handler(CommandHandler("tt", tt))
    application.add_handler(CommandHandler("checkvar", checkvar))
    application.add_handler(CommandHandler("bb", bb_command))
    application.add_handler(CommandHandler("tbp", tbp_command))
    application.add_handler(CommandHandler("gpt", gpt_command))
    application.add_handler(CommandHandler("gemi", gemi))
    application.add_handler(CommandHandler("php", php_command))
    application.add_handler(CommandHandler("bing", bing_command))
    application.add_handler(CommandHandler("llama", llama_command))
    application.add_handler(CommandHandler("qwen", qwen_command))
    application.add_handler(CommandHandler("yt", yt_command))
    application.add_handler(CommandHandler("lyrics", lyrics_command))
    application.add_handler(CommandHandler("rd_cat", gui_anh_cat_dog))
    application.add_handler(CommandHandler("timanh", search))
    application.add_handler(CommandHandler("taoanhnhanh", taoanhnhanh))
    application.add_handler(CommandHandler("camhung", cam_hung))
    application.add_handler(CommandHandler("laytheme", laytheme))
    application.add_handler(CommandHandler("tuoi", tuoi))
    application.add_handler(CommandHandler("down", lay_video))
    application.add_handler(CommandHandler("spotify", spotify))
    application.add_handler(CommandHandler("timnhac", timnhac))
    application.add_handler(CommandHandler("checkip", check_ip))
    application.add_handler(CommandHandler("bsx", bsx))
    application.add_handler(CommandHandler("qr", qr))
    application.add_handler(CommandHandler("ytb_audio", ytb_audio))
    application.add_handler(CommandHandler("downx", downx))
    application.add_handler(CommandHandler("downig", downig))
    application.add_handler(CommandHandler("downfb", downfb))
    application.add_handler(CommandHandler("ig", ig))
    application.add_handler(CommandHandler("smskmb", smskmb))
    application.add_handler(CommandHandler("demo", demo))
    application.add_handler(CommandHandler('users', users_command))
    application.add_handler(CommandHandler('thongke', thongke))   
    application.add_handler(CommandHandler('zhelp', zhelp))
    application.add_handler(CommandHandler('send', send))

    # Bắt tin nhắn trong nhóm và riêng
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_message))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Bắt đầu chạy bot
    await asyncio.gather(get_updates(bot_api), application.run_polling())

if __name__ == "__main__":
    asyncio.run(start_bot())
