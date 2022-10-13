from aiogram import types
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
browser_is_busy = None


async def parsing(message: types.Message,browser_is_busy):
    print(f'{message.from_user.id},'
          f'Запрос:{message.text},'
          f'{message.from_user.first_name} {message.from_user.last_name}')
    while 1:
        if browser_is_busy:
            await asyncio.sleep(5)
        else:
            browser_is_busy = True
            break

    driver.get(f'https://yandex.ru/images/search?text={message.text}')
    kotik = driver.find_element(By.XPATH, '//div/div/div/a/img')
    kotik.click()
    spisok_ssilok = []
    a = 0
    while a < 3:
        button = driver.find_element(By.XPATH,
                                     '/html/body/div/div[2]/div/div/div/div[3]/div/div[3]/div/div/div[1]/div[4]/div[1]/a')
        spisok_ssilok.append(types.InputMediaPhoto(button.get_attribute('href')))
        strelka = driver.find_element(By.XPATH,
                                      '/html/body/div/div[2]/div/div/div/div[3]/div/div[2]/div[1]/div[4]/i')
        strelka.click()
        a += 1
    browser_is_busy = False
    print(f'результатов:{len(spisok_ssilok)},'
          f'{message.from_user.id},'
          f'Запрос:{message.text},')

    return spisok_ssilok


async def sand_picturs(message):
    reply = await message.reply('Ваш запрос обрабатывается. Пожалуйста подождите ..... минут')
    await message.reply_media_group(types.MediaGroup(await parsing(message)))
    await reply.delete()


def register_handlers(dp):
    dp.register_message_handler(sand_picturs)
