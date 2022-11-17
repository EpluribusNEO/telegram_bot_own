from aiogram import Bot, Dispatcher, types, executor
from random import randint
from asyncio import sleep
import dotenv
from os import environ
from OWM import TOWM



dotenv.load_dotenv('.env')
bot_token = environ['bot_token']
owm_key = environ['owm']
z_owm = TOWM(owm_key)
bot = Bot(bot_token)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	username = message.from_user.username
	msg = f"<b>Hello</b>, <i>{username}!</i>\nВведите /help - для справки"
	await bot.send_message(message.chat.id, msg, parse_mode='html')

@dp.message_handler(commands=['coin'])
async def coin(message: types.Message):
	rnd = randint(0, 1001)
	coin_status = 'Ребро'
	if rnd % 2 == 0:
		coin_status = 'Орёл'
	else:
		coin_status = 'Решка'
	await bot.send_message(message.chat.id, f"<b>{coin_status}</b>", parse_mode='html')


@dp.message_handler(commands=['whoami'])
async def whoami(message: types.Message):
	first_name = message.from_user.first_name
	last_name =message.from_user.last_name
	username = message.from_user.username
	id = message.from_user.id
	whoami_msg = f"first name: {first_name}\nlast name: {last_name}\nuser name: {username}\nid: {id}"
	await bot.send_message(message.chat.id, whoami_msg)

@dp.message_handler(commands=['website'])
async def website(message: types.Message):
	myurl = "https://ds-portfolio.netlify.app"
	markup = types.InlineKeyboardMarkup()
	website = types.InlineKeyboardButton("Посетить веб сайт", url=myurl)
	markup.add(website)
	await bot.send_message(message.chat.id, f'<a href="{myurl}">Website</a>', parse_mode='html', reply_markup=markup)

@dp.message_handler(commands=['about'])
async def about(message: types.Message):
	text = f'Created by: <b>EPluribusNEO</b>\n' \
	       f'WebSite: <a href="https://ds-portfolio.netlify.app">Website</a>\n' \
	       f'GitHub: <a href="https://github.com/EpluribusNEO">GitHub</a>\n' \
	       f'Date: 14 August 2022\n' \
	       f'\nВведите /help для получения справки по командам.'
	markup = types.InlineKeyboardMarkup()
	github = types.InlineKeyboardButton("GitHub", url="https://github.com/EpluribusNEO")
	website = types.InlineKeyboardButton("Website", url="https://ds-portfolio.netlify.app")
	markup.add(website, github)
	await bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
	text_help = f'Введите одну из следующих команд:\n' \
	            f'<b>Основные команды:</b>\n' \
	            f'/start - Для начала работы\n' \
	            f'/weather <i>Название Города</i> - прогноз погоды\n' \
	            f'/погода <i>Название Города</i> - прогноз погоды\n' \
	            f'\n<b>Игра:</b>\n' \
	            f'Отправьте боту cмайлик 🎲 "игральные кости" для начала игры\n' \
	            f'\n<b>Дополнительные команды:</b>\n' \
	            f'/coin - Подбросить монетку\n' \
	            f'/whoami - Вывести имя пользователя\n' \
	            f'/website - Вывести исформацию о вебсайте разработчика\n' \
	            f'/about - Подробная информация о боте\n' \
	            f'/qr - Получить ссылку на страничку разработчика\n' \
	            f'/help - Вывести справку о доступных командах'
	await bot.send_message(message.chat.id, text_help, parse_mode='html')

@dp.message_handler(commands=['qr'])
async def photo(message: types.Message):
	photo = open('z-qr.png', 'rb')
	await bot.send_photo(message.chat.id, photo)

@dp.message_handler(content_types=['photo'])
async def get_user_photo(message: types.Message):
	usr_msg_id = message.message_id
	await bot.send_message(message.chat.id, 'Cool Photo!', reply_to_message_id=usr_msg_id)

@dp.message_handler(content_types=['sticker'])
async def sticker(message: types.Message):
	await bot.send_message(message.chat.id, "СТИКЕР")

@dp.message_handler(content_types=['dice'])
async def dice_game(message: types.Message):
	usr_point = message['dice']['value']
	usr_msg_id = message.message_id
	await sleep(5)
	bot_data = await bot.send_dice(message.chat.id, reply_to_message_id=usr_msg_id)
	bot_point = bot_data['dice']['value']
	await sleep(5)
	if usr_point > bot_point:
		await bot.send_message(message.chat.id, 'Вы победили!', reply_to_message_id=usr_msg_id)
	elif usr_point < bot_point:
		await bot.send_message(message.chat.id, "Вы проиграли!", reply_to_message_id=usr_msg_id)
	else:
		await bot.send_message(message.chat.id, "Ничья!", reply_to_message_id=usr_msg_id)


@dp.message_handler(commands=['weather', 'погода'])
async def weather(message: types.Message):
	command = message['text']
	city = command.split(maxsplit=1)[1]
	weather = z_owm.get_weather(city)
	await bot.send_message(message.chat.id, weather)

@dp.message_handler(commands=['echo'])
async def echo(message: types.Message):
	msg = message['text'].split(maxsplit=1)[1]
	await bot.send_message(message.chat.id, msg)

executor.start_polling(dp, loop=True)
