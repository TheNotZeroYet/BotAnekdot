from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import requests
from dotenv import load_dotenv
from os import remove

from pathlib import Path
import os
from random import randint

from db import Database

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv('TOKEN')


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
top_password_btn = KeyboardButton('Сохранённые Пароли')
like_btn = KeyboardButton('В Избранное')
skip_btn = KeyboardButton('Пропустить')

# KEYBOARDS
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add(rand_joke_btn, rand_passw_btn, top_jokes_btn, top_password_btn)
joke_item_kb = ReplyKeyboardMarkup(resize_keyboard=True)
joke_item_kb.add(like_btn, skip_btn)
password_item_kb = ReplyKeyboardMarkup(resize_keyboard=True)
password_item_kb.add(like_btn, skip_btn)

db_client = Database("table.db")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# bot launch handling
@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    db_client.add_user(user_id, username, "start")
    await message.reply(
        f"Сборник анекдотов со всей наблюдаемой человечеством вселенной, \nтакже из других вселенных, еще есть сборник лучших анекдотов из КВН (нет)",
        reply_markup=menu_kb)


@dp.message_handler()
async def main_func(message: types.Message):
    user_id = str(message.from_user.id)
    if message.text == 'Рандомный Пароль' and db_client.get_state_user(int(user_id)) == "start":
        password = "".join(rand_password())
        db_client.add_password(password, int(user_id))
        db_client.set_state_user(int(user_id), 'password_menu')
        await message.reply(password, reply_markup=password_item_kb)
    elif message.text == 'Пропустить' and db_client.get_state_user(int(user_id)) == "password_menu":
        db_client.set_state_user(int(user_id), 'start')
        await message.reply('Вы успешно вернулись домой', reply_markup=menu_kb)
    elif message.text == 'В Избранное' and db_client.get_state_user(int(user_id)) == "password_menu":
        db_client.add_id_password_to_ids(int(user_id), db_client.get_last_password_id(int(user_id)))
        db_client.set_state_user(int(user_id), 'start')
        await message.reply('Вы успешно добавили пароль в избранное', reply_markup=menu_kb)
    elif message.text == 'Рандомный Анекдот' and db_client.get_state_user(int(user_id)) == "start":
        joke = rand_joke()
        db_client.add_joke(joke, int(user_id))
        db_client.set_state_user(int(user_id), 'joke_menu')
        await message.reply(joke, reply_markup=joke_item_kb)
    elif message.text == 'Пропустить' and db_client.get_state_user(int(user_id)) == "joke_menu":
        db_client.set_state_user(int(user_id), 'start')
        await message.reply('Вы успешно вернулись домой', reply_markup=menu_kb)
    elif message.text == 'В Избранное' and db_client.get_state_user(int(user_id)) == "joke_menu":
        db_client.add_id_joke_to_ids(int(user_id), db_client.get_last_joke_id(int(user_id)))
        db_client.set_state_user(int(user_id), 'start')
        await message.reply('Вы успешно добавили шутку в избранное', reply_markup=menu_kb)
    elif message.text == 'Избранные Анекдоты' and db_client.get_state_user(int(user_id)) == 'start':
        if db_client.get_joke_ids_by_user(int(user_id)):
            joke_ids = list(map(int, db_client.get_joke_ids_by_user(int(user_id)).split(',')))
            for joke_id in joke_ids:
                await message.reply(f"{db_client.get_joke_by_id(joke_id)}")
        else:
            await message.reply('как-то здесь пустовато...')
    elif message.text == 'Сохранённые Пароли' and db_client.get_state_user(int(user_id)) == 'start':
        if db_client.get_password_ids_by_user(int(user_id)):
            password_ids = list(map(int, db_client.get_password_ids_by_user(int(user_id)).split(',')))
            for password_id in password_ids:
                await message.reply(f"{db_client.get_password_by_id(password_id)}")
        else:
            await message.reply('упс, капустовато...')

if __name__ == '__main__':
    executor.start_polling(dp)
