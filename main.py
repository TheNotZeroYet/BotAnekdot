from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import requests

from random import randint

from db import Database

TOKEN = "6415358389:AAGaNRZsKJEDufAngFjNHiZUP9kaW8krU0A"


# FUNCTION
def rand_password():
    return [chr(randint(44, 122)) for _ in range(randint(7, 12))]


def rand_joke():
    joke = requests.get("https://official-joke-api.appspot.com/random_joke")
    return f"{joke.json()['setup']} {joke.json()['punchline']}"


# BUTTONS
rand_joke_btn = KeyboardButton('Рандомный Анекдот')
rand_passw_btn = KeyboardButton('Рандомный Пароль')
top_jokes_btn = KeyboardButton('Избранные Анекдоты')
top_password_btn = KeyboardButton('Сохраенные Пароли')

# KEYBOARDS
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add(rand_joke_btn, rand_passw_btn, top_jokes_btn, top_password_btn)

db_client = Database("table.db")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# bot launch handling
@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    db_client.add_user(user_id, username)
    await message.reply(
        f"Сборник анекдотов со всей наблюдаем человечеством вселенной, \nтакже из других вселенных, еще есть сборник лучших анекдотов из КВН (нет)",
        reply_markup=menu_kb)


@dp.message_handler()
async def get_rand_password(message: types.Message):
    user_id = str(message.from_user.id)
    if message.text == 'Рандомный Пароль':
        password = "".join(rand_password())
        db_client.add_password(password)
        await message.reply(password)
    elif message.text == 'Рандомный Анекдот':
        joke = rand_joke()
        db_client.add_joke(joke)
        await message.reply(joke)


if __name__ == '__main__':
    executor.start_polling(dp)
