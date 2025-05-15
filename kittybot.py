import os
from dotenv import load_dotenv
from telebot import TeleBot, types
import requests


load_dotenv()

TELEGRAM_TOKEN = ''
try:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    URL_CAT = os.getenv('URL_CAT')
    URL_DOG = os.getenv('URL_DOG')
    chat_id = os.getenv('chat_id')
except Exception:
    print('Ошибка при получении данных .env')
bot = TeleBot(token=f'{TELEGRAM_TOKEN}')

zero_buttom = ('Перезапустить! 🔥', 'Старт', 'Пуск', 'Start', 'старт', 'пуск', 'start')
first_buttom = 'Позвать кошку в гости'
second_buttom = 'Позвать собачку в гости'
third_buttom = '😀 Какие то задачи актуальны'
tasks_family = ['Продать велик Марины',
                 'Расчитать стоимость дачи',
                 'Определиться с баней']


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Создаём объект клавиатуры:
    button_cat = types.KeyboardButton(first_buttom)  # Создаём объект кнопки:
    button_dog = types.KeyboardButton(second_buttom)  # Создаём объект кнопки:
    button_task = types.KeyboardButton(third_buttom)  # Создаём объект кнопки:
    button_start = types.KeyboardButton(zero_buttom[0])  # Создаём объект кнопки:
    keyboard.add(button_cat, button_dog, button_task, button_start)  # Добавляем объект кнопки на клавиатуру:
    try:
        bot.send_message(chat_id=chat.id, text = f'{name}, начинаем развлекаться. Жмите на кнопочки', reply_markup=keyboard, )
    except Exception:
        print('Ошибка отправки сообщения')


@bot.message_handler(content_types=['text'])
def say_hi(message):
    comanda = message.text
    chat = message.chat
    name = message.chat.first_name
    print(f'{name} жмет кнопку {comanda}')
    random_url = None
    user_message = None
    if comanda == first_buttom:
        response = requests.get(f'{URL_CAT}').json()
        random_url = response[0].get('url')
        user_message = f'{name} к вам в гости пришла кошечка'
    elif comanda == 'Позвать собачку в гости':
        response = requests.get(f'{URL_DOG}').json()
        random_url = response[0].get('url')
        user_message = f'{name} к вам в гости пришла собачка'
    elif comanda == third_buttom:
        user_message = f'1) {tasks_family[0]}'
        for task_number in range(1, len(tasks_family)):
            user_message += '\n' + f'{task_number+1}) {tasks_family[task_number]}'
    elif comanda in zero_buttom:
        wake_up(message)
    else:
        user_message = 'Пока эту команду не реализовали, пишите Алексею Васильевичу!'

    if user_message:
        try:
            bot.send_message(chat_id=chat.id, text = f'{user_message}')
        except Exception:
            print('Ошибка отправки сообщения')
    if random_url:
        try:
            bot.send_photo(chat_id=chat.id, photo=random_url)
        except Exception:
            print('Ошибка отправки фото')


# message = 'Вам телеграмма!'
try:
    bot.polling(interval=5)
except Exception:
    print('Вышла ошибка в polling')

# Вызываем метод send_message, с помощью этого метода отправляются сообщения:
# bot.send_message(chat_id, message)
# say_hi('asd')