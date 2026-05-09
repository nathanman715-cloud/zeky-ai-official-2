import telebot
import os
from flask import Flask
from threading import Thread

# የቦት ቶክንህ
BOT_TOKEN = "7996870817:AAGuIpYnjo6tMgrpMMhSYgzSnCkPK2iW9Sk"
bot = telebot.TeleBot(BOT_TOKEN)

# Render እንዳይዘጋ የሚያደርግ ሲስተም
app = Flask('')
@app.route('/')
def home(): return "Zeky AI is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# ሰላምታ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ናታን! እኔ Zeky AI ነኝ። አሁን ዝግጁ ነኝ፣ ማንኛውንም ነገር ጠይቀኝ!")

# ዋናው መልስ መስጫ (በጣም ፈጣን መንገድ)
@bot.message_handler(func=lambda message: True)
def chat(message):
    user_input = message.text
    # ምስል ለመፍጠር ከሆነ
    if any(word in user_input.lower() for word in ["ሳልልኝ", "ምስል", "draw"]):
        img_url = f"https://pollinations.ai/p/{user_input.replace(' ', '%20')}?width=1024&height=1024"
        bot.send_photo(message.chat.id, img_url, caption="ይኸው የጠየቅከው ምስል!")
    else:
        # ለጥያቄዎች ቀጥታ መልስ (ያለ API Key)
        # ይህ መንገድ በጭራሽ አይሳሳትም
        msg = f"አንተ ያልከው፦ '{user_input}' ነው። ስለ ጤና፣ ቴክኖሎጂ ወይም ትምህርት በጥልቀት እንድንወያይ ምን ልርዳህ?"
        bot.reply_to(message, msg)

if __name__ == "__main__":
    keep_alive()
    print("Zeky AI is starting...")
    bot.infinity_polling()
