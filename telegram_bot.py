from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram
import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging
import zapier
import bucket

logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

env = os.environ.get('ENV', 'development')
logger.info("Enviroment: " + env)

if(env != 'production'):
    # dotenv file
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path, verbose=True)

TOKEN = os.environ.get('TOKEN')
ZAPIER_URL = os.environ.get('ZAPIER_WEBHOOK')

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

try:
    def start(bot, update):
        print("Start")
        contact_keyboard = InlineKeyboardButton(text="Enviar meu número de telefone", request_contact=True)
        custom_keyboard = [[ contact_keyboard ]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text="Preciso do seu número de telefone", reply_markup=reply_markup)

    def som(bot, update):
        print("Audio recebido: " + str(update.message.chat_id))
        bot.send_voice(chat_id=update.message.chat_id, voice=open('teste_ogg.ogg', 'rb'))

    def echo(bot, update):
        texto = update.message.text[::-1] + '<b> xaxa oioi</b>'
        print(texto)
        print(update.message.from_user.username)

        bot.send_message(chat_id=update.message.chat_id, text=texto, parse_mode=telegram.ParseMode.HTML)

    def respond(bot, update):
        telegram_url = zapier.send_audio(ZAPIER_URL, bot, update)
        bot.send_message(chat_id=update.message.chat_id, text='resposta recebida')

    def voice(bot, update):
        print("Audio recebido: " + update.message.voice.file_id)
        voice_id = update.message.voice.file_id
        voice_path = '/tmp/voice-' + voice_id + '.ogg'
        voice_file = bot.getFile(voice_id)
        voice_file.download(voice_path)

        username = update.message.from_user.username
        s3_url = bucket.upload_s3(voice_path, username + '_' + voice_id)
        zapier.send_audio(ZAPIER_URL, username, s3_url)

        bot.send_message(chat_id=update.message.chat_id, text='audio recebido')

    def contact(bot, update):
        telefone = update.message.contact.phone_number
        reply_markup = telegram.ReplyKeyboardRemove()
        print("Contato recebido: " + telefone)

        bot.send_message(chat_id=update.message.chat_id, text='contato recebido', reply_markup=reply_markup)

    start_handler = CommandHandler('start', start)
    som_handler = CommandHandler('som', som)
    respond_handler = CommandHandler('respond', respond)
    echo_handler = MessageHandler(Filters.text, echo)
    voice_handler = MessageHandler(Filters.voice, voice)
    contact_handler = MessageHandler(Filters.contact, contact)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(som_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(voice_handler)
    dispatcher.add_handler(contact_handler)
    dispatcher.add_handler(respond_handler)

    if(env == 'production'):
        PORT = int(os.environ.get('PORT', '5000'))
        HEROKU_APP = os.environ.get('HEROKU_APP')
        logger.info("PORT: " + str(PORT))
        logger.info("HEROKU_APP: " + HEROKU_APP)
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://"+ HEROKU_APP +".herokuapp.com/" + TOKEN)
        updater.idle()
    else:
        updater.start_polling()
except Exception as e:
    print(e)
