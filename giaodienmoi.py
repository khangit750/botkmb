import aiohttp
import asyncio
import nest_asyncio #quan trọng nhất
import time
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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
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
TOKEN = '7173014638:AAHBSBbu2cTcExsQjWt4BCKcQ4BdPjpWq-8'
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
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    user_info = {
        'id': update.effective_user.id,
        'name': update.effective_user.first_name,
        'username': update.effective_user.username
    }
    
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    # Gọi hàm xử lý người dùng mới
    await on_new_user(update, user_info, context)

    help_text = '''
<b>🔖 Danh sách lệnh của bot</b>
<blockquote>
┌───────────⭓
│» /start - Bắt đầu
│» /help - Trợ giúp
│» /trollvn - Troll troll troll
│» /tiktok - Tải video tik tok (nhanh)
│» /voice + [văn bản] - Tạo voice từ văn bản
│» /upanh - Up ảnh lấy link
│» /bank + [Ngân Hàng] + [STK] - Tạo QR chuyển khoản
│» /time - Thời gian hoạt động
│» /thoitiet - Xem thời tiết
│» /code - Lấy Code HTML
│» /proxy - Get proxy IP:PORT
│» /hoi - Chat cùng bot
│» /fb - Check info Facebook
│» /tt - Check info Tiktok
│» /tv - Ngôn ngữ tiếng việt
│» /2fa - Lấy mã 2FA
│» /id - Lấy ID
└───────────⭓
</blockquote>
'''

    # Tạo nút nằm ngang
    keyboard = [
        [
            InlineKeyboardButton("➕ ADD ME", url='http://t.me/kmb_gaming_bot?startgroup=true'),
            InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=help_text, 
        parse_mode='HTML', 
        reply_markup=reply_markup,
        reply_to_message_id=update.message.message_id if update.message else None
    )
is_bot_active = True

#XỬ LÝ LỆNH TROLL
async def trollvn(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    def read_jokes():
        with open(JOKE_FILE_PATH, 'r', encoding='utf-8') as file:
            jokes = file.readlines()
        return jokes

    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
        
        vietnamese_jokes = read_jokes()
        joke = random.choice(vietnamese_jokes).strip()  # Loại bỏ ký tự xuống dòng
        await update.message.reply_text(text=f"<blockquote><i>{joke}</i></blockquote>", parse_mode='HTML')  # Sử dụng thẻ <i>
    except FileNotFoundError:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Tệp không tìm thấy.")
    except Exception as e:
        await update.message.reply_text(text=f"Có lỗi xảy ra: {e}")

# Hàm xử lý lệnh /voice
async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_api=None):
    user_id = update.effective_user.id

    if not is_bot_active:
        await update.message.reply_text(text='Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    text = ' '.join(context.args)

    if not text:
        await update.message.reply_text(text='<blockquote><i>Sử dụng: /voice {văn bản cần tạo giọng}</i></blockquote>', parse_mode='HTML')  # Sử dụng thẻ <i>
        return

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
        await update.message.reply_text(text='<blockquote><i>Sử dụng: /code.\nVí dụ: /code https://google.com </i></blockquote>', parse_mode='HTML')  # Sử dụng thẻ <i>
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
        await update.message.reply_text(text=f"<i>Đã xảy ra lỗi khi tải trang web: {e}</i>", parse_mode='HTML')

    finally:
        # Đảm bảo xóa file sau khi gửi
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                await update.message.reply_text(chat_id=update.effective_chat.id, text=f"Đã xảy ra lỗi khi xóa file: {e}")

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
                InlineKeyboardButton("➕ ADD ME", url='http://t.me/kmb_gaming_bot?startgroup=true'),
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
                    InlineKeyboardButton("➕ ADD ME", url='http://t.me/kmb_gaming_bot?startgroup=true'),
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
        await update.message.reply_text('<blockquote>Sử dụng /tiktok {link video}.</blockquote>', parse_mode='HTML')
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
                                        text='<blockquote>Sử dụng /thoitiet. Ví dụ: /thoitiet Hanoi</blockquote>', 
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
        reply = f'Đã xảy ra lỗi khi thực hiện yêu cầu: {str(e)}'
    
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
            f"<b>NGÂN HÀNG</b>: <i>{bank_name}</i>\n"
            "<b>CHECK TRƯỚC KHI GỬI CHO NGƯỜI KHÁC</b>\n"
            "</blockquote>"
        )

        # Gửi hình ảnh QR kèm theo mô tả
        await send_photo_bank(chat_id, quick_link, message_text)

    except Exception as e:
        await send_message(chat_id, f"Đã xảy ra lỗi: {str(e)}")

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
    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
            print(f"Sent reaction: {emoji_to_react}")  # In ra emoji đã gửi
    except Exception as e:
        print(f"Error sending reaction: {e}")
    # Kiểm tra nếu không có số lượng
    if not num_proxies_str or not num_proxies_str.isdigit():
        await context.bot.send_message(
            chat_id=chat_id,
            text='<blockquote><i>Sử dụng: /proxy {số lượng}</i></blockquote>',
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
                InlineKeyboardButton("➕ ADD ME", url='http://t.me/kmb_gaming_bot?startgroup=true'),
                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

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
async def fb(update: Update, context: CallbackContext, bot_api=None):
    chat_id = update.effective_chat.id
    user_id = context.args[0].strip() if context.args else None  # Lấy tham số

    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
    except Exception as e:
        print(f"Error sending reaction: {e}")  # In ra thông báo lỗi

    # Kiểm tra nếu không có ID hoặc tên người dùng
    if not user_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text='<blockquote><i>Sử dụng: /fb {id or user}</i></blockquote>',
            parse_mode='HTML',
            reply_to_message_id=update.message.message_id
        )
        return

    url = f'https://thichlaptrinh.space/info.php?fb={user_id}'

    try:
        # Gửi trạng thái chờ
        thinking_message = await context.bot.send_message(chat_id=chat_id, text='🔎')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

        profile_id = data.get('profile_id', "Không có thông tin")
        name = data.get('name', "Không có thông tin")
        username = data.get('username', "Không có thông tin")
        is_verified = "Đã xác minh ✅" if data.get('is_verified') else "Chưa xác minh ❌"
        created_time = data.get('created_time', "Không có thông tin")
        location = data.get('location', {}).get('name', "Không công khai")
        profile_link = f'<a href="{data.get("link")}">{data.get("link")}</a>'
        followers = data.get('Followers', "Không có thông tin")
        profile_pic = data.get('picture', {}).get('data', {}).get('url', "Không có ảnh đại diện")

        message = f"""
<blockquote>
╭─────────────⭓
│ <b>ID:</b> <code>{profile_id}</code>
│ <b>Name:</b> <a href="{data.get('link')}">{name}</a>
│ <b>Username:</b> <a href="{data.get('link')}">{username}</a>
│ <b>Link:</b> {data.get('link')}
│ <b>Verified:</b> {is_verified}
│ <b>Created Time:</b> {created_time}
│ <b>Gender:</b> {'Nam' if data.get('gender') == 'male' else 'Nữ'}
│ <b>Relationships:</b> {data.get('relationship_status', 'Không có thông tin')}
│ <b>Hometown:</b> {data.get('hometown', {}).get('name', 'Không có thông tin')}
│ <b>Location:</b> {location}
│ <b>Work:</b>
"""

        # Thêm thông tin công việc
        for work in data.get('work', []):
            employer_name = work['employer']['name']
            position = work.get('position', {}).get('name', 'Chưa có')
            start_date = work.get('start_date', 'Không có thông tin')
            message += f"│ -> <b>Làm việc tại</b> {employer_name} <b>với vị trí</b> {position} <b>từ</b> {start_date}\n"

        message += "│ <b>Study:</b>\n"

        # Thêm thông tin học vấn
        for education in data.get('education', []):
            school_name = education['school']['name']
            concentration = ", ".join([c['name'] for c in education.get('concentration', [])])
            message += f"│ -> <b>Học</b> {concentration} <b>tại</b> {school_name}\n"

        message += f"""│ <b>Birthday:</b> {data.get('birthday', 'Không có thông tin')}
│ <b>Followers:</b> Có {followers} người theo dõi
│ <b>About:</b> {data.get('about', 'Không có thông tin')}
├─────────────⭔
│ <b>Language:</b> {data.get('locale')}
│ <b>Last Updated:</b> {data.get('updated_time', 'Không có thông tin')}
│ <b>Time Zone:</b> GMT {data.get('timezone')}
╰─────────────⭓
</blockquote>
"""

        # Tạo nút nằm ngang
        keyboard = [
            [
                InlineKeyboardButton("➕ ADD ME", url='http://t.me/kmb_gaming_bot?startgroup=true'),
                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(chat_id=chat_id, photo=profile_pic, caption=message, parse_mode='HTML', reply_to_message_id=update.message.message_id, reply_markup=reply_markup)

        # Xóa thông báo trạng thái chờ
        await context.bot.delete_message(chat_id=chat_id, message_id=thinking_message.message_id)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Đã xảy ra lỗi: {e}")

# Hàm xử lý lệnh /tt
#https://chongluadao.x10.bz/api/other/admintiktokduyvinh09.php?user={user_id}
#https://iuhchinh.x10.mx/tt.php?user={user_id}
async def tt(update: Update, context: CallbackContext, bot_api=None):
    chat_id = update.effective_chat.id
    user_id = context.args[0].strip() if context.args else None  # Lấy tham số

    # Thêm phản ứng ngẫu nhiên cho lệnh trước khi reply
    emoji_to_react = get_random_positive_reaction()
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    
    try:
        if bot_api:  # Kiểm tra xem bot_api có được truyền vào không
            bot_api.set_message_reaction(chat_id, message_id, emoji_to_react)
            print(f"Sent reaction: {emoji_to_react}")  # In ra emoji đã gửi
    except Exception as e:
        print(f"Error sending reaction: {e}")

    # Kiểm tra nếu không có ID hoặc tên người dùng
    if not user_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text='<blockquote><i>Sử dụng: /tt user</i></blockquote>',
            parse_mode='HTML',
            reply_to_message_id=update.message.message_id
        )
        return

    url = f'https://chongluadao.x10.bz/api/other/admintiktokduyvinh09.php?user={user_id}'

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
                InlineKeyboardButton("➕ ADD ME", url='http://t.me/kmb_gaming_bot?startgroup=true'),
                InlineKeyboardButton("👤 ADMIN", url='https://t.me/khangmb247')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(chat_id=chat_id, photo=avatar, caption=message, parse_mode='HTML', reply_to_message_id=update.message.message_id, reply_markup=reply_markup)

        # Xóa thông báo trạng thái chờ
        await context.bot.delete_message(chat_id=chat_id, message_id=thinking_message.message_id)

    except Exception as error:
        await context.bot.send_message(chat_id=chat_id, text=f'Đã có lỗi xảy ra: {error}', reply_to_message_id=update.message.message_id)


###########
async def on_update(data, bot_api):
    if 'message' in data:
        content = data['message']
        chat_id = content['chat']['id']
        message_id = content['message_id']
        text = content.get('text', '')

        # Gọi hàm xử lý lệnh proxy
        if text == "/proxy":
            await proxy(content, bot_api)
        if text == "/start":
            await help(content, bot_api)
        if text == "/help":
            await help(content, bot_api)
        if text == "/trollvn":
            await trollvn(content, bot_api)
        if text == "/voice":
            await voice(content, bot_api)
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
        if text == "/fb":
            await fb(content, bot_api)
        if text == "/tt":
            await tt(content, bot_api)
###########
# Đăng ký lệnh
async def start_bot():
    bot_api = TelegramBotAPI(TOKEN)
    application = ApplicationBuilder().token(TOKEN).build()

    # Thêm các handler cho các lệnh
    application.add_handler(CommandHandler("start", lambda update, context: help(update, context, bot_api)))
    application.add_handler(CommandHandler("help", lambda update, context: help(update, context, bot_api)))
    application.add_handler(CommandHandler("trollvn", lambda update, context: trollvn(update, context, bot_api)))
    application.add_handler(CommandHandler("voice", lambda update, context: voice(update, context, bot_api)))
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
    application.add_handler(CommandHandler("proxy", lambda update, context: proxy(update, context, bot_api)))
    application.add_handler(CommandHandler("fb", lambda update, context: fb(update, context, bot_api)))
    application.add_handler(CommandHandler("tt", lambda update, context: tt(update, context, bot_api)))
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


