from aiogram import types
from keyboards.inline import kb_menu_panel, kb_back
from loader import dp
from aiogram.dispatcher import FSMContext
from time import sleep
from googlesearch import search
from utils.misc import rate_limit


@dp.callback_query_handler(text='back', state='google')
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='searchgoogle')
async def search_google(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    global msg_google
    msg_google = await call.message.edit_text(f'Пожалуйста, введите текст для поиска(Выдаст 5 ссылок): ', reply_markup=kb_back)
    await state.set_state("google")  # --- назначем состояние


@dp.message_handler(state="google")  # ---- получаем стейт google (который назаначен выше)
async def get_google(message: types.Message, state: FSMContext):
    await msg_google.delete()
    src_google = f'{message.text.lower()}'
    for item in search(src_google, num=5, stop=5, pause=2):
        print(item)
        sleep(2)
        await message.answer(f'{item}')
        await state.finish()  # ------ Сбрасываем состояние

    await message.answer('Поиск завершен!\n'
                         'Воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)