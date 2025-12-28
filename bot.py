import os
import telebot
import requests
from flask import Flask, request

# Configuration - Railway will add these automatically
TELEGRAM_TOKEN = os.environ.get("8268214914:AAGuEeRY2QnzArz2C8THpcKhOAn9TJbxEa4", "")
GROQ_KEY = os.environ.get("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", "")

bot = telebot.TeleBot(8268214914:AAGuEeRY2QnzArz2C8THpcKhOAn9TJbxEa4)
app = Flask(__name__)

def ask_ai(question):
    """Get response from Groq AI"""
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": [{"role": "user", "content": question}],
            "model": "llama-3.1-8b-instant",
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=20)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "🤖 خطای سرور. لطفاً بعداً تلاش کنید."
    except:
        return "🤖 مشکل اتصال. لطفاً بعداً تلاش کنید."

@bot.message_handler(commands=['start'])
def start(message):
    welcome = """
🇦🇫 سلام! من ChatAfg هستم.

پرسش خود را به دری، پشتو یا انگلیسی بنویسید.
هر روز ۱۵ پیام رایگان دارید.

دستورات:
/help - راهنما
"""
    bot.reply_to(message, welcome)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response = ask_ai(message.text)
    bot.reply_to(message, response)

# Webhook for Railway
@app.route('/')
def home():
    return "🤖 ChatAfg Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return 'ok'

if __name__ == "__main__":
    # Set webhook for Telegram
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.environ.get('RAILWAY_STATIC_URL', '')}/webhook")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
