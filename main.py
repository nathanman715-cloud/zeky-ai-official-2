import telebot
import requests
import os
import urllib.parse
from flask import Flask
from threading import Thread

# 1. ቦት ዝግጅት
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Zeky AI is officially FIXED!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ናታን! ዜኪ (Zeky AI) አሁን ሙሉ በሙሉ ዝግጁ ነኝ። አማርኛም ሆነ እንግሊዝኛ መጠየቅ ትችላለህ።")

@bot.message_handler(func=lambda message: True)
def chat(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    # ምስል ከሆነ
    image_keys = ["ሳልልኝ", "ምስል", "draw", "image"]
    if any(word in user_text.lower() for word in image_keys):
        encoded_prompt = urllib.parse.quote(user_text)
        img_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&model=flux"
        bot.send_photo(message.chat.id, img_url, caption="ይኸው የጠየቅከው ምስል!")
        return

    try:
        # የአማርኛ ፊደላት እንዳይበላሹ 'urllib.parse.quote' እንጠቀማለን
        system_msg = "You are Zeky AI, a genius assistant. Answer accurately in the language the user uses. Be conversational."
        encoded_text = urllib.parse.quote(user_text)
        api_url = f"https://text.pollinations.ai/{encoded_text}?model=openai&system={urllib.parse.quote(system_msg)}"
        
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200 and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ አእምሮዬ ጋር መገናኘት አልቻልኩም። ድጋሚ ሞክር።")
            
    except Exception:
        bot.reply_to(message, "ኔትወርክ ተቋርጧል፣ እባክህ ቆይተህ ሞክር።")

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    bot.infinity_polling(non_stop=True)
