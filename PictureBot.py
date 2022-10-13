import aiogram
import asyncio
from functions_for_picturebot import register_handlers


BOT_KEY = '5755493253:AAHm-J87KioNywaomgOhGemBOSojZtkAByw'
async def main(BOT_KEY):
    bot = aiogram.Bot(BOT_KEY)
    dp = aiogram.Dispatcher(bot)

    register_handlers(dp)

    print('bot running')
    await dp.start_polling()


asyncio.run(main(BOT_KEY))