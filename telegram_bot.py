from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
import os
from os.path import join, dirname
from dotenv import load_dotenv

env = os.environ.get('ENV')
if(env != 'production'):
    # dotenv file
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path, verbose=True)

TOKEN = os.environ.get('TOKEN')
PORT = os.environ.get('PORT')
HEROKU_APP = os.environ.get('HEROKU_APP')

updater = Updater(token=TOKEN)

if(env == 'production'):
    update.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://"+ HEROKU_APP  +".herokuapp.com/" + token).start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)

dispatcher = updater.dispatcher

try:
    def start(bot, update):
        contact_keyboard = KeyboardButton(text="Enviar meu número de telefone", request_contact=True)
        custom_keyboard = [[ contact_keyboard ]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id, text="Preciso do seu número de telefone", reply_markup=reply_markup)

    def echo(bot, update):
        texto = update.message.text[::-1] + '<b> xaxa oioi</b>'
        print(texto)
        print(update.message.from_user.username)

        bot.send_message(chat_id=update.message.chat_id, text=texto, parse_mode=telegram.ParseMode.HTML)

    def voice(bot, update):
        print("Audio recebido: " + update.message.voice.file_id)
        newFile = bot.get_file(update.message.voice.file_id)
        newFile.download('voz.ogg')

        bot.send_message(chat_id=update.message.chat_id, text='audio recebido')

    def contact(bot, update):
        telefone = update.message.contact.phone_number
        reply_markup = telegram.ReplyKeyboardRemove()
        print("Contato recebido: " + telefone)

        bot.send_message(chat_id=update.message.chat_id, text='contato recebido', reply_markup=reply_markup)

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text, echo)
    voice_handler = MessageHandler(Filters.voice, voice)
    contact_handler = MessageHandler(Filters.contact, contact)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(voice_handler)
    dispatcher.add_handler(contact_handler)

    if(env == 'production'):
        updater.start_polling()
    else:
        updater.idle()
except Exception as e:
    print(e)
