import datetime

from aiogram import types
import aiohttp
import asyncio

from main import logger


async def weather_handler(message: types.Message):
    start_time = datetime.datetime.now()
    try:
        logger.info(f'Weather request from @{message.from_user.username} sucessful, total time: {datetime.datetime.now() - start_time}')
        weather = await get_weather()
        await message.answer(f'Погода в Москве: {weather["temperature"]}°C')

    except (
        DuckException, 
        asyncio.exceptions.TimeoutError, 
        aiohttp.client_exceptions.ClientConnectorError
        )  as e:
        logger.warning(f'{e.__class__.__name__}: {e}')
        logger.info(f'Weather request from @{message.from_user.username} failed')
        await message.answer(f'😥 Сервис временно не доступен, попробуйте позже.')

def get_keyboard():
    button1 = types.KeyboardButton(text='Погода в Москве')
    button2 = types.KeyboardButton(text='Поговорить с уткой')
    keyboard = [[button1, button2]]
    markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    return markup

async def get_weather():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        async with session.get('http://localhost:8000/weather') as response:
            if response.status == 200:
                json = await response.json()
                return json
            raise DuckException('Weather API did not return the weather')

class DuckException(Exception):
    pass