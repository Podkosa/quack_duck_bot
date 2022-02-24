import logging
import os
import random

from aiogram import Bot, Dispatcher, executor, types
import utils


bot = Bot(token=os.getenv('TGBOT_API_TOKEN'))
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('duckbot')


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    logger.info(f'Message /start or /help from @{message.from_user.username}')
    await message.answer("🦆 <i>кря кря</i> 🦆", parse_mode='HTML', reply_markup=utils.get_keyboard())

@dp.message_handler()
async def message_parser(message: types.Message):
    if 'погода' in message.text.lower():
        await utils.weather_handler(message)
    else:
        logger.info(f'Unparsed message from from @{message.from_user.username}')
        await message.answer("<i>кря</i> "*random.randint(1, 3), parse_mode='HTML')


if __name__ == '__main__':
    # Start long polling Telegram API
    executor.start_polling(dp, skip_updates=True)