from aiogram import types
import asyncio
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))


def is_url_image(image_url):
    try:
        image_formats = ("image/jpeg", "image/jpg")
        r = requests.head(image_url)
        if r.headers["content-type"] in image_formats:
            return True
        return False
    except Exception:
        return False


async def parsing(message: types.Message):
    print(f'{message.from_user.id},'
          f'Запрос:{message.text},'
          f'{message.from_user.first_name} {message.from_user.last_name}')
    async with message.bot.get('semofor'):
        runner = message.bot.loop.run_in_executor
        await runner(None, driver.get, f'https://yandex.ru/images/search?text={message.text}')
        kotik = driver.find_element(By.XPATH,
                                    '//div/div/div/a/img')  # /html/body/div[3]/div[2]/div[1]/div[1]/div/div[3]/div/a/img
        # kotik.click()
        await runner(None, kotik.click)
        spisok_ssilok = []
        a = 0
        while a < 10:
            try:
                button = driver.find_element(By.CLASS_NAME, 'MMViewerButtons-OpenImageSizes')
                button = button.find_element(By.TAG_NAME, 'a')
                ssilka = button.get_attribute('href')
            except Exception as e:
                print('сломалось', e)
            if is_url_image(ssilka):
                spisok_ssilok.append(ssilka)
                a += 1
            strelka = driver.find_element(By.XPATH,
                                          '/html/body/div/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[4]/i')
            await runner(None, strelka.click)
    print(f'результатов:{len(spisok_ssilok)},'
          f'{message.from_user.id},'
          f'Запрос:{message.text},')
    print(*spisok_ssilok, sep='\n')
    return spisok_ssilok


async def sand_picturs(message):
    reply = await message.reply('Ваш запрос обрабатывается. Пожалуйста подождите ..... минут')
    spisok_ssilok = [types.InputMediaPhoto(s) for s in await parsing(message)]
    try:
        await message.reply_media_group(types.MediaGroup(spisok_ssilok))
    except Exception as e:
        print('сломалось', e)
        await message.reply('ОШИБКА:По вашему запросу произошла ошибка')
    await reply.delete()


def register_handlers(dp):
    dp.register_message_handler(sand_picturs)
