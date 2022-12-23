from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu import kb_menu_panel, kb_back
from loader import dp
from googletrans import Translator
from utils.misc import rate_limit


translator = Translator()


# Перевод на Румынский язык
@dp.callback_query_handler(text='back', state='translate_romanian')
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='romanian_lang')
async def ready_translation(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    global msg_text_romanian
    msg_text_romanian = await call.message.edit_text(f'Пожалуйста, введите слово или текст для перевода: ', reply_markup=kb_back)
    await state.set_state("translate_romanian")


@dp.message_handler(state='translate_romanian')  # ---- получаем стейт translates (который назаначен выше)
async def get_translate(message: types.Message, state: FSMContext):
    await msg_text_romanian.delete()
    text = message.text
    result = translator.translate(f'{text}', dest='ro').text
    await message.reply(f'<b>Результат перевода:</b> <i>{result}</i> \n')
    await state.finish()  # ------ Сбрасываем состояние
    await message.answer('Воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)