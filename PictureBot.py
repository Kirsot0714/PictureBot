import aiogram
import asyncio
from functions_for_picturebot import register_handlers


BOT_KEY = '5755493253:AAHm-J87KioNywaomgOhGemBOSojZtkAByw'
async def main(BOT_KEY):
    loop = asyncio.get_event_loop()
    bot = aiogram.Bot(BOT_KEY,loop = loop)
    # bot['semofor'] = asyncio.Lock()
    bot['semofor'] = asyncio.Semaphore(1)
    dp = aiogram.Dispatcher(bot,loop = loop)

    register_handlers(dp)

    print('bot running')
    await dp.start_polling()


asyncio.run(main(BOT_KEY))