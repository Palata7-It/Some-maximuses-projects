from aiogram.types import ContentType
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Data_base.db_help_class import db_help

import config

logging.basicConfig(level=logging.INFO)

# initialise bot
bot = Bot(token=config.TOKEN)
db = Dispatcher(bot, storage=MemoryStorage())

data = db_help('Data_base\subject.db')


class main_States(Helper):
    mode = HelperMode.snake_case

    EMPTY = ListItem()
    DECISIVE = ListItem()
    CLIENT = ListItem()


@db.message_handler(state='*', commands='start')
async def start_meth(message: types.message):
    await message.answer(
        'Привет, {}!\nВыберите кем вы хотите быть:\n1)Решающий\n2)Работодатель'.format(message.chat.first_name))
    state = db.current_state(user=message.from_user.id)
    print(main_States.all())
    await state.set_state(main_States.all()[2])


@db.message_handler(content_types=ContentType.TEXT, state=main_States.EMPTY)
async def picture(message: types.message):
    state = db.current_state(user=message.from_user.id)
    if message.text == '1':
        await state.set_state(main_States.DECISIVE)
        await message.answer('Добро пожаловать решающий, выбери предмет:')
    elif message.text == '2':
        await state.set_state(main_States.CLIENT)
        await message.answer('Добро пожаловать работодатель, выбери предмет:')
    else:
        await message.answer('Введите пожалуйста либо 1 либо 2')
        return 0
    for i in data.return_info('all_subjects'):
        await message.answer('{}) {}'.format(i[0],i[1]))


@db.message_handler(state=main_States.CLIENT|main_States.EMPTY)
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(db, skip_updates=True, on_shutdown=shutdown(db))
