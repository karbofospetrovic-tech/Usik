import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot is running!"

@app.route('/health')
def health():
    return "OK"

def run_web_server():
    port = int(os.environ.get('PORT', 8080))  # ← БЫЛО: os.envdron.get
    app.run(host='0.0.0.0', port=port)        # ← БЫЛО: bost='0.0.0.0'

# Ваш существующий код бота оставьте ниже
import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from gtts import gTTS  # ← БЫЛО: from gits import gITS
import speech_recognition as sr
from pydub import AudioSegment  # ← БЫЛО: from pyAub import AudioSegment

# 📞 Ваш TOKEN
TOKEN = "8083120011:AAHs2PDQSalGmOH27kzfoXDiC3QB7I74YNJ"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

recognizer = sr.Recognizer()

# === Обработка голосовых сообщений ===
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... ваш код обработки голоса ...

if __name__ == '__main__':
    # Запускаем веб-сервер
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    # Здесь запуск вашего бота
    # application = Application.builder().token(TOKEN).build()
    # application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    # application.run_polling()
