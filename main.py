import telebot
import requests
import os
from flask import Flask
from threading import Thread

# 1. ቦት ዝግጅት
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Zeky AI is now a Genius!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    Thread(target=run).start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ናታን! አሁን አእምሮዬ ሙሉ በሙሉ ተስተካክሏል። አማርኛም ሆነ እንግሊዝኛ ማንኛውንም ነገር መጠየቅ ትችላለህ።")

@bot.message_handler(func=lambda message: True)
def chat(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    # ምስል ከሆነ
    if any(word in user_text.lower() for word in ["ሳልልኝ", "ምስል", "draw", "image"]):
        img_url = f"https://pollinations.ai/p/{user_text.replace(' ', '%20')}?width=1024&height=1024"
        bot.send_photo(message.chat.id, img_url, caption="ይኸው የጠየቅከው ምስል!")
        return

    try:
        # እጅግ ብልህ የሆነው AI አድራሻ
        # ይሄኛው እንግሊዝኛን በደንብ ያውቃል
        api_url = f"https://text.pollinations.ai/{user_text}?model=openai&system=You are Zeky AI, a genius assistant. Answer accurately in the language the user uses."
        
        response = requests.get(api_url, timeout=30)
        if response.status_code == 200:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "ትንሽ ችግር አጋጥሞኛል፣ ደግመህ ጠይቀኝ።")
            
    except Exception:
        bot.reply_to(message, "ኔትወርክ ተቆርጧል፣ እባክህ ቆይተህ ሞክር።")

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook()
    bot.infinity_polling()
