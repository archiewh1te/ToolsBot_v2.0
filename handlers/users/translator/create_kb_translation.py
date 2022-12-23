from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline import kb_menu_translation, kb_menu_panel
from loader import dp
from utils.misc import rate_limit


@dp.callback_query_handler(text='back')
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='translate')
async def ready_translation(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.edit_text('<b>💡Меню Переводчика</b>\n'
                                 'Выберите язык:', reply_markup=kb_menu_translation)

