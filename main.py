import telebot
import requests
import os
from flask import Flask
from threading import Thread

# ቶክንህ
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Zeky AI is Online!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    Thread(target=run).start()

@bot.message_handler(func=lambda message: True)
def chat(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    
    # ምስል ከሆነ
    if any(word in user_text.lower() for word in ["ሳልልኝ", "ምስል", "draw"]):
        img_url = f"https://pollinations.ai/p/{user_text.replace(' ', '%20')}?model=turbo"
        bot.send_photo(message.chat.id, img_url)
        return

    # ለጥያቄዎች ቀጥታ መልስ (በጣም ቀላሉ መንገድ)
    try:
        # ይሄ URL ለአማርኛም ለእንግሊዝኛም እጅግ ጎበዝ ነው
        url = f"https://text.pollinations.ai/{user_text}?model=openai"
        response = requests.get(url)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Error!")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
