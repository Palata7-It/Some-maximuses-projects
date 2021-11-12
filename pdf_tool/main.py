import os

from aiogram.types import ContentType
from image_convert import make_pdf_file
import config
import logging
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

# initialise bot
bot = Bot(token=config.TOKEN)
db = Dispatcher(bot)

make_pdf = False
photo_for_file = []


def del_dir(path):
    for i in os.listdir(path):
        os.remove(path + '\\' + i)
    os.rmdir(path)


@db.message_handler(commands=["start"])
async def start(message: types.message):
    """The start method"""

    me = await bot.get_me()
    await message.answer('Я {} бот созданый с прихоти создателя для облегчения посылки дз 😜\n Введите /help для '
                         'получениия большей информации'.format(me.first_name))


@db.message_handler(commands=["help"])
async def help(message: types.message):
    await message.answer('Привет {}, небольшая инструкция для получения тебе нужного pdf файла с картинок:\n1) Введи '
                         'команду /home_task\n2) Отправь поочередно нужные фото\n3) Введи /end и подожди создания '
                         'файла и его отправки тебе.'.format(message.chat.first_name))


@db.message_handler(commands=["home_task"])
async def home_task(message):
    global make_pdf
    if not make_pdf:
        await message.answer('Мои соболезнования😢😢😢\nОтправляй фото в порядке каком хочешь видить их в файле pdf')
        make_pdf = True


@db.message_handler(commands=["end"])
async def end(message):
    global make_pdf, photo_for_file
    if make_pdf:
        path = 'Images\{}'.format(message.from_user.id)
        if os.path.exists(path):
            del_dir(path)
        os.mkdir(path)
        await message.answer('Молодец, как я и ожидал ты смог его сделать❤❤❤')
        make_pdf = False
        j = 0
        for i in photo_for_file:
            await i.download('{Images}\{file_name}.jpg'.format(Images=path, file_name=j))
            j += 1
        make_pdf_file('heh', path)
        doc = open('{}\heh.pdf'.format(path), 'rb')
        await bot.send_document(message.from_user.id, doc, caption='Этот файл специально для тебя!')
        doc.close()
        del_dir(path)
        photo_for_file = []


@db.message_handler(content_types=ContentType.PHOTO)
async def picture(message: types.chat_photo):
    if make_pdf:
        # await bot.send_photo(message.chat.id, message.photo[0].file_id)
        photo_for_file.append(message.photo[-1])


if __name__ == '__main__':
    executor.start_polling(db, skip_updates=True)
