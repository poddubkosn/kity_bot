# kittybot/kittybot.py


import logging
import os
import requests
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup

from dotenv import load_dotenv

load_dotenv()
auth_token = os.getenv('TOKEN')
auth_token_photo = os.getenv('SNPOD_PHOTO_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


updater = Updater(token=auth_token)
updater_photo = Updater(token=auth_token_photo)
KEY = '23894052-fa6a338bf0dd164294f8adb9f'
URL = 'https://pixabay.com/api/'


COUNTER_PAGE = {'pag': 1}

def get_new_photo():

    try:
        parameters = {'key': KEY, 'page': COUNTER_PAGE['page'], 'per_page': 3,
                   'q': 'naked+girls', 'image_type': 'photo'}
        response = requests.get(URL, params=parameters)
        COUNTER_PAGE['page'] += 1
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        COUNTER_PAGE['page'] = 1
        parameters = {'key': KEY, 'page': COUNTER_PAGE['page'], 'per_page': 3,
                   'q': 'naked+girls', 'image_type': 'photo'}
        response = requests.get(URL, params=parameters)
        COUNTER_PAGE['page'] += 1
    list_of_photo = [photos.get('largeImageURL') for photos in  response.json().get('hits')]
    return list_of_photo

def new_photo(update, context):
    chat = update.effective_chat
    for foto in get_new_photo():
        context.bot.send_photo(chat.id, foto)

def wake_up_photo(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newphoto']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, каких телочек я тебе нашёл'.format(name),
        reply_markup=button)
    for foto in get_new_photo():
        context.bot.send_photo(chat.id, foto)

def get_new_image(animal):
    if animal == 'dog':
        URL = 'https://api.thedogapi.com/v1/images/search'
    else:
        URL = 'https://api.thecatapi.com/v1/images/search'
    try:
        response = requests.get(URL)
    except Exception as error:
        
        #print(error)      
        logging.error(f'Ошибка при запросе к основному API: {error}')
        if animal == 'dog':
            new_url = 'https://api.thecatapi.com/v1/images/search'
            
        else:
            new_url = 'https://api.thedogapi.com/v1/images/search'
            
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image('cat'))

def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id,get_new_image('dog'))


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,text='Привет, я KittyBot!')

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat','/sex','/newdog']], resize_keyboard=True)
    # buttons = ReplyKeyboardMarkup([
    #             ['Который час?', 'Определи мой ip'],
    #             ['/random_digit']
    #        ])
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button

        # text='Спасибо, что вы включили меня, {}!'.format(name),
        # reply_markup=buttons
        )
    context.bot.send_photo(chat.id, get_new_image('cat'))


def i_want(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id, 
                             text=f'Я хочу тебя {name} !!!')
# Регистрируется обработчик CommandHandler;
# он будет отфильтровывать только сообщения с содержимым '/start'
# и передавать их в функцию wake_up()
def main():
    updater_photo.dispatcher.add_handler(CommandHandler('start', wake_up_photo))
    updater_photo.dispatcher.add_handler(CommandHandler('newphoto', new_photo))
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))
    updater.dispatcher.add_handler(CommandHandler('sex', i_want))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater_photo.start_polling()
    updater.start_polling()
    updater.idle()
    updater_photo.idle()
if __name__ == '__main__':
    main()  