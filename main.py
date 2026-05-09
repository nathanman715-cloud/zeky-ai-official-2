import telebot
import requests
import os
from flask import Flask
from threading import Thread

# 1. ቦት ዝግጅት
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

# Render እንዳይዘጋ የሚያደርግ
app = Flask('')
@app.route('/')
def home(): return "Zeky AI is Super Fast!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ሰላምታ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ Zeky AI ነኝ። አሁን እጅግ ፈጣን ሆኛለሁ! ማንኛውንም ጥያቄ ይጠይቁኝ። ምስል ለመሳል 'ሳልልኝ' ይበሉኝ።")

# ዋናው የንግግር እና ምስል መፍጠሪያ ክፍል
@bot.message_handler(func=lambda message: True)
def chat(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    # 1. ምስል የመፍጠር ትዕዛዝ ከሆነ
    image_keywords = ["ሳልልኝ", "አሳይኝ", "ምስል", "draw", "image", "picture"]
    if any(word in user_text.lower() for word in image_keywords):
        # ጥያቄውን ወደ እንግሊዝኛ ቀይረን ለምስል መፍጠሪያው እንልካለን
        img_url = f"https://pollinations.ai/p/{user_text.replace(' ', '%20')}?width=1024&height=1024&model=flux&seed=42"
        bot.send_photo(message.chat.id, img_url, caption="ይኸው የጠየቁት ምስል!")
        return

    # 2. ለጽሁፍ ጥያቄዎች (እጅግ ፈጣን የሆነ API)
    try:
        # ይህ API በጣም ፈጣን እና አስተማማኝ ነው
        system_prompt = "You are Zeky AI, a smart assistant. Always answer in Amharic. Be helpful and fast. User asks: "
        api_url = f"https://text.pollinations.ai/{system_prompt}{user_text}?model=openai"
        
        response = requests.get(api_url, timeout=15)
        if response.status_code == 200:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ አሁን ትንሽ ተቸግሬያለሁ። እባክህ ድጋሚ ጠይቀኝ።")
            
    except Exception:
        bot.reply_to(message, "ኔትወርክ ተቋርጧል፣ እባክህ ድጋሚ ሞክር።")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
