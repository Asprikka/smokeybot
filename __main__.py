import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold

import res
import tools
from filters import IsAdmin
from fsm import Form


API_TOKEN = '5757436992:AAHM3_B9OxEwq7pLk7Tpmpxd8w0pw_dTkzU'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

vapes_list = tools.load_vapes_list(path=res.VAPES_LIST_JSON_PATH)


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.finish()
    await message.reply('Дія скасована!')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(res.START_ANS)
    await message.answer(
        bold(tools.get_vapes_str(vapes_list)),
        parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('<треба_шото_вставить>')


@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    await Form.order.set()
    await message.answer('Опишіть замовлення (одним повідомленням!)')


@dp.message_handler(state=Form.order)
async def buy_fsm(message: types.Message, state: FSMContext):
    await forward_order(message)

    await message.answer('Замовлення відправлено!')
    await state.finish()


async def forward_order(message: types.Message):
    await bot.send_message(
        chat_id=res.ADMIN_ID,
        parse_mode=ParseMode.HTML,
        text=tools.build_forward_text(message)
    )


@dp.message_handler(IsAdmin(), commands=['upd'])
async def upd_admin(message: types.Message):
    await Form.vapes_str.set()
    await message.answer('Відправте мені оновлений список')


@dp.message_handler(IsAdmin(), state=Form.vapes_str)
async def upd_admin_fsm(message: types.Message, state: FSMContext):
    global vapes_list
    vapes_list = tools.get_vapes_list(message.text)
    tools.update_json(res.VAPES_LIST_JSON_PATH, vapes_list)

    await message.reply(f'Список оновлено!')
    await state.finish()


if __name__ == '__main__':
    dp.filters_factory.bind(IsAdmin)