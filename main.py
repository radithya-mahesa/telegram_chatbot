import os
import logging
from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from keep_alive import keep_alive

keep_alive()
port = int(os.getenv('PORT', 8080))
user_states = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token dan username disimpan ke dalam environment variable cloud server
TOKEN: final = os.getenv('TOKEN') # = 'Your Token'
BOT_USERNAME: final = os.getenv('USERNAME') # = 'Your Bot Username'
WEBHOOK_URL: final = os.getenv('WEBHOOK_URL') # Optional


if TOKEN is None or BOT_USERNAME is None:
    raise ValueError("Token atau username bot tidak ditemukan :(")


# /commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hola! selamat datang di Bot Telegramku✨\nkamu bisa ngobrol bebas selayaknya Character AI🥳\nMohon ketik "/help" terlebih dahulu sebelum mulai! ⚠')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('/start = Pengenalan awal saja\n/help = Berupa deskripsi atau penjelaan dari sebuah command\n/about = Keterangan dari bot ini\n/tsundere = Ganti personality bot menjadi tsundere (Default)\n/deredere = Ganti personality bot menjadi derder\n/important = Pokoknya Penting!\n\nSudah baca ini? mohon lanjut dengan menekan -> /important')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('AI Model : Gemini 🤖\nCharacter Name : Alya Roshidere 🌸\nLanguage : Python 🐍\nCreated By : @RadithyaMS 😏\nCredit API : NyxAltair 🔥')

async def tsundere_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_states[user_id] = 'tsundere'
    await update.message.reply_text('H-hah! Terserah sih~')

async def deredere_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_states[user_id] = 'deredere'
    await update.message.reply_text('Ah.. baiklah^^')

async def important_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ketik apa saja jika ingin aku merespon😏\n\nJika aku tidak membalas selama lebih dari 30 detik atau jawaban aku ngaco, coba ketik ulang🤕\n\nTerkadang jika kamu mengetik isu sensitif seperti organisasi terror atau memuat isu rasis kemungkinan tidak merespon dan error🤯, dan jawaban yang diberikan bisa tidak sesuai(rusak)🥱\n\nKadang tidak semua aku mengerti kosakata bahasa gaul😥, jadi kalo ngetik sebisa mungkin lebih jelas dan mudah dimengerti, oke😉\n\nSatu lagi, melakukan perbincangan yang mengarah ke hal seksual dapat membuat GeminiAI menggantikan jawabanku menjadi default, maka dari itu kamu harus mencoba merangkai kata kata seunik mungkin agar terByPass oleh regulasi yang ditetapkan oleh Google, he he he...')


# External API
def handle_response(text: str, state: str) -> str:
    if state == 'tsundere':
        api_url = f"https://api.nyx.my.id/ai/character-ai?prompt={text}&gaya=jawab%20dengan%20pacar%20tsundere%20pemarah"
    else:
        api_url = f"https://api.nyx.my.id/ai/character-ai?prompt={text}&gaya=jawab%20dengan%20pacar%20deredere%20manis"

    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Content: {response.content}")

        data = response.json()
        print(f"API JSON Response: {data}")
        
        if data.get("status") == "true":
            return data.get("result", "API tidak merespon")
        else:
            return "API mengembalikan false."
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        reason = e.response.reason
        error_message = f"Api nya Capek Wak! : Status_Code:{status_code} {reason}(I can't breathe~) coba lagi nanti"
        print(f"HTTPError occurred: {error_message}")
        return error_message
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "Api Error!: Coba lagi nanti"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    state = user_states.get(user_id, 'tsundere')  # Default
    response: str = handle_response(text, state)
    
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about_command))
    app.add_handler(CommandHandler('tsundere', tsundere_command))
    app.add_handler(CommandHandler('deredere', deredere_command))
    app.add_handler(CommandHandler('important', important_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # polls the bot
    #print('polling...')
    #app.run_polling(poll_interval=3)

    app.run_webhook(listen="0.0.0.0",
                    port=port,
                    url_path=f"/{TOKEN}",
                    webhook_url=f"{WEBHOOK_URL}/{TOKEN}")

