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
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Ваш существующий код бота оставьте ниже
# ... ваш текущий код ...
import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment

# 🔑 Ваш токен
TOKEN = "8083120011:AAHs2PDQSa1GmOHJ7RzfoXbIc3Q87174VYU"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

recognizer = sr.Recognizer()

# === Обработка голосовых сообщений ===
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"Голосовое от {user.first_name} (ID: {user.id})")

    voice_file = await update.message.voice.get_file()
    ogg_path = f"{voice_file.file_id}.ogg"
    wav_path = f"{voice_file.file_id}.wav"

    try:
        await voice_file.download_to_drive(ogg_path)
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(wav_path, format="wav")

        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = None
            detected_lang = None

            try:
                text = recognizer.recognize_google(audio_data, language="de-DE")
                detected_lang = "de"
            except sr.UnknownValueError:
                try:
                    text = recognizer.recognize_google(audio_data, language="ru-RU")
                    detected_lang = "ru"
                except sr.UnknownValueError:
                    await update.message.reply_text("❌ Не удалось распознать речь.")
                    return

        await process_translation(update, text, detected_lang)

    except Exception as e:
        logger.error(f"Ошибка в голосовом: {e}")
        await update.message.reply_text("⚠️ Ошибка при обработке голосового.")
    finally:
        for f in [ogg_path, wav_path]:
            if os.path.exists(f):
                os.remove(f)

# === Обработка текстовых сообщений ===
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text:
        return

    user = update.message.from_user
    logger.info(f"Текст от {user.first_name}: {text}")

    try:
        # Определяем язык по символам (эвристика)
        has_cyrillic = any('а' <= c.lower() <= 'я' or c in 'ёЁ' for c in text)
        detected_lang = "ru" if has_cyrillic else "de"

        await process_translation(update, text, detected_lang)

    except Exception as e:
        logger.error(f"Ошибка в тексте: {e}")
        await update.message.reply_text("⚠️ Не удалось определить язык или перевести текст.")

# === Общая функция перевода и озвучки ===
async def process_translation(update: Update, text: str, src_lang: str):
    try:
        if src_lang == "de":
            translation = GoogleTranslator(source='de', target='ru').translate(text)
            target_lang = 'ru'
            reply_text = f"🇩🇪 → 🇷🇺\n{text}\n\nПеревод:\n{translation}"
        else:
            translation = GoogleTranslator(source='ru', target='de').translate(text)
            target_lang = 'de'
            reply_text = f"🇷🇺 → 🇩🇪\n{text}\n\nÜbersetzung:\n{translation}"

        # Отправляем текст
        await update.message.reply_text(reply_text)

        # Генерируем и отправляем голосовое
        tts = gTTS(text=translation, lang=target_lang, slow=False)
        mp3_path = f"reply_{hash(text)}.mp3"
        tts.save(mp3_path)

        with open(mp3_path, 'rb') as audio:
            await update.message.reply_voice(voice=audio)

        # Удаляем файл
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

    except Exception as e:
        logger.error(f"Ошибка при переводе/озвучке: {e}")
        await update.message.reply_text("⚠️ Ошибка при переводе или озвучке.")

# === Запуск бота ===
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("✅ Бот запущен! Отправляйте ГОЛОСОВЫЕ или ТЕКСТ — получите перевод и озвучку.")
    app.run_polling()

if __name__ == '__main__':
    if __name__ == '__main__':
    # Запускаем веб-сервер
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    
    # Здесь запуск вашего бота
    # Например: bot.polling() или bot.infinity_polling()

    main()
