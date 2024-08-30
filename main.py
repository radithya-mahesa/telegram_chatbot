import os
import logging
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)

TOKEN: Final[str] = os.getenv('TOKEN')
BOT_USERNAME: Final[str] = os.getenv('USERNAME')
PORT: Final[int] = int(os.getenv('PORT', 9001))

if TOKEN is None or BOT_USERNAME is None:
    raise ValueError("Token & Username tidak ditemukan :(")

keep_alive()

# /commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hola! selamat datang di Bot Telegramku✨\nkamu bisa ngobrol bebas selayaknya Character AI🥳\nMohon ketik atau tekan "/help" dan /important terlebih dahulu sebelum mulai! ⚠')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('/start = Pengenalan awal saja\n/help = Berupa deskripsi atau penjelaan dari sebuah command\n/about = Keterangan dari bot ini\n/important = Penting!\n\nSudah baca ini? mohon lanjut dengan menekan -> /important')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('AI Model : Llama 70b 🤖\nCharacter Name : Sparkle 🌸\nLanguage : Python 🐍\nCreated By : @RadithyaMS 😏\nCredit API : Zanixon 🔥')

async def important_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ketik apa saja jika ingin aku merespon😏\n\nJika aku tidak membalas selama lebih dari 30 detik atau jawaban aku ngaco, coba ketik ulang🤕\n\nTerkadang jika kamu mengetik isu sensitif seperti organisasi terror atau memuat isu rasis kemungkinan tidak merespon dan error🤯, dan jawaban yang diberikan bisa tidak sesuai(rusak)🥱\n\nKadang tidak semua aku mengerti kosakata bahasa gaul😥, jadi kalo ngetik sebisa mungkin lebih jelas dan mudah dimengerti, oke😉\n\nSatu lagi, melakukan perbincangan yang mengarah ke hal seksual dapat membuat Llama3 menggantikan jawabanku menjadi default, maka dari itu kamu harus mencoba merangkai kata kata seunik mungkin agar terByPass oleh regulasi yang ditetapkan oleh Google, he he he...')

# external API
def handle_response(text: str) -> str:
    api_url = 'https://llama3-enggan-ngoding.vercel.app/api/llama'
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": "Your name is Sparkle from honkai star rail. You don't speak English, you only speak Indonesian. You use the word 'I'/'me' as 'aku' instead of 'saya' when answering. reply as usodere's feminine, cunning, and naughty girlfriend!"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "model": "70b"
    }

    try:
        response = requests.post(api_url, json=request_body)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status"):
            return data.get("output", "API tidak merespon")
        else:
            return "API mengembalikan false."
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        reason = e.response.reason
        return f"Api nya Capek Wak! : Status_Code:{status_code} {reason}(I can't breathe~) coba lagi nanti"
    except requests.exceptions.RequestException as e:
        return f"Api Error!: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = handle_response(text)
    
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
    app.add_handler(CommandHandler('important', important_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    # polls
    print('polling...')
    app.run_polling(poll_interval=3)

    
