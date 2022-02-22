import logging
import os
import random
import datetime

from aiogram import Bot, Dispatcher, executor, types
import aiohttp

bot = Bot(token=os.getenv('TGBOT_API_TOKEN'))
dp = Dispatcher(bot)

class DuckException(Exception):
    pass

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("🦆 <i>кря кря</i> 🦆", parse_mode='HTML', reply_markup=get_keyboard())
    logger.info(f'Message /start or /help from @{message.from_user.username}')

@dp.message_handler()
async def weather_in_Moscow(message: types.Message):
    if 'погода' in message.text.lower():
        start_time = datetime.datetime.now()
        try:
            weather = await get_weather()
            await message.answer(f'Погода в Москве: {weather["temperature"]}°C')
            logger.info(f'Weather request from @{message.from_user.username} sucessful, total time: {datetime.datetime.now() - start_time}')

        except DuckException as e:
            logger.warning(f'{e.__class__.__name__}: {e}')
            await message.answer(f'😥 Сервис временно не доступен, попробуйте позже.')
            logger.info(f'Weather request from @{message.from_user.username} failed')
    else:
        logger.info(f'Unparsed message from from @{message.from_user.username}')
        await message.answer("<i>кря</i> "*random.randint(1, 3), parse_mode='HTML')

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

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('duckbot')

    # Start polling Telegram API
    executor.start_polling(dp, skip_updates=True)