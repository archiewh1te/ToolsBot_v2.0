from aiogram import types
from keyboards.inline import kb_menu_panel, kb_back
from loader import dp
from aiogram.dispatcher import FSMContext
from time import sleep
from youtubesearchpython import CustomSearch, VideoUploadDateFilter
from utils.misc import rate_limit


@dp.callback_query_handler(text='back', state='youtube')
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='searchyoutube')
async def search_youtube(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    global msg_youtube
    msg_youtube = await call.message.edit_text(f'Пожалуйста, введите название видео(Выдаст 5 ссылок): ', reply_markup=kb_back)
    await state.set_state("youtube")  # --- назначем состояние


@dp.message_handler(state="youtube")  # ---- получаем стейт youtube (который назаначен выше)
async def get_youtube(message: types.Message, state: FSMContext):
    await msg_youtube.delete()
    try:
        customSearch = CustomSearch(f'{message.text.lower()}', VideoUploadDateFilter.thisYear, limit=20)
        for i in range(5):
            search = customSearch.result()['result'][i]['link']
            print(search)
            sleep(1.5)
            await message.answer(f'{search}')
            await state.finish()  # ------ Сбрасываем состояние
    except Exception:
        await message.reply("Проверьте правильно ли написано название")
        await state.finish()  # ------ Сбрасываем состояние

    await message.answer('Поиск видео завершен!\n'
                         'Воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)
