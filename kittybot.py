import os
from dotenv import load_dotenv
from telebot import TeleBot, types
import requests


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = TeleBot(token=TELEGRAM_TOKEN)
    
URL = os.getenv('URL')
dog_url = os.getenv('dog_url')
chat_id = os.getenv('chat_id')

@bot.message_handler(commands=['cat', 'dog'])
def say_hi(message):
    response = requests.get(URL).json()
    comanda = message.text
    chat = message.chat
    name = message.chat.first_name
    if comanda == '/cat':
        guest = 'кошечка'
        random_url = response[0].get('url')
    else:
        response = requests.get(dog_url).json()
        guest = 'собачка'
        random_url = response[0].get('url')
    bot.send_message(chat_id=chat.id, text = f'{name} к вам в гости пришла {guest}')
    bot.send_photo(chat_id, random_url) 

@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создаём объект клавиатуры:
    button_cat = types.KeyboardButton('/cat')  # Создаём объект кнопки:
    button_dog = types.KeyboardButton('/dog')  # Создаём объект кнопки:
    keyboard.add(button_cat, button_dog)  # Добавляем объект кнопки на клавиатуру:
    bot.send_message(chat_id=chat.id, text = f'{name} начинаем показ животных. Жмите на кнопочки', reply_markup=keyboard, )

# message = 'Вам телеграмма!'
bot.polling(interval=1)
# Вызываем метод send_message, с помощью этого метода отправляются сообщения:
# bot.send_message(chat_id, message)
# say_hi('asd')