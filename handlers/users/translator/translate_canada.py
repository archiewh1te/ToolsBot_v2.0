from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu import kb_menu_panel, kb_back
from loader import dp
from googletrans import Translator
from utils.misc import rate_limit


translator = Translator()


# Перевод на Канадский язык
@dp.callback_query_handler(text='back', state='translate_canada')
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='canada_lang')
async def ready_translation(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    global msg_text_bulgarian
    msg_text_bulgarian = await call.message.edit_text(f'Пожалуйста, введите слово или текст для перевода: ', reply_markup=kb_back)
    await state.set_state("translate_canada")


@dp.message_handler(state='translate_canada')  # ---- получаем стейт translates (который назаначен выше)
async def get_translate(message: types.Message, state: FSMContext):
    await msg_text_bulgarian.delete()
    text = message.text
    result = translator.translate(f'{text}', dest='kn').text
    await message.reply(f'<b>Результат перевода:</b> <i>{result}</i> \n')
    await state.finish()  # ------ Сбрасываем состояние
    await message.answer('Воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)
