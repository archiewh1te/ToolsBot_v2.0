import socket
from keyboards.inline import kb_menu_panel, kb_back
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.misc import rate_limit


@dp.callback_query_handler(text='back', state='get_ip')
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='infoipsite')
async def ip_by_hostname(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    global msg_url
    msg_url = await call.message.edit_text(f'Пожалуйста, введите URL-адрес веб-сайта: ', reply_markup=kb_back)
    await state.set_state("get_ip")  # --- назначем состояние


@dp.message_handler(state='get_ip')  # ---- получаем стейт get_ip (который назаначен выше)
async def get_ip_hostname(message: types.Message, state: FSMContext):
    await msg_url.delete()
    try:
        await message.reply(f'Hostname: {message.text}\nIP адрес: {socket.gethostbyname(message.text)}')
        await state.finish()  # ------ Сбрасываем состояние
    except socket.gaierror as error:
        await message.reply(f'Неверный хост - {error}')

    await message.answer('Воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)

