import telebot
import requests
import os
from flask import Flask
from threading import Thread

# 1. Bot Setup
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Zeky AI is officially SMART!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    Thread(target=run).start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ናታን! አሁን አእምሮዬ ተስተካክሏል። ማንኛውንም ነገር ጠይቀኝ፣ በዝርዝር እመልስልሃለሁ!")

@bot.message_handler(func=lambda message: True)
def chat(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    # ምስል ከሆነ
    if any(word in user_text.lower() for word in ["ሳልልኝ", "ምስል", "draw"]):
        img_url = f"https://pollinations.ai/p/{user_text.replace(' ', '%20')}?width=1024&height=1024&seed=123"
        bot.send_photo(message.chat.id, img_url, caption="ይኸው የጠየቅከው ምስል!")
        return

    try:
        # ይሄኛው API በጣም አስተማማኝ ነው (Blackbox AI)
        api_url = "https://text.pollinations.ai/"
        payload = {
            "messages": [
                {"role": "system", "content": "You are Zeky AI, a brilliant assistant. Answer everything in Amharic unless asked otherwise. Be detailed."},
                {"role": "user", "content": user_text}
            ],
            "model": "openai"
        }
        
        # ጥያቄውን መላክ
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ይቅርታ፣ አእምሮዬ ላይ ትንሽ ችግር ተፈጥሯል። ድጋሚ ጠይቀኝ።")
            
    except Exception as e:
        bot.reply_to(message, "ኔትወርክ ተቋርጧል። እባክህ ትንሽ ቆይተህ ሞክር።")

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    bot.infinity_polling()
