from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline import kb_menu_panel, kb_back
from loader import dp
from utils.misc import rate_limit
import uuid
from states.downld_youtube import Dowload
from pytube import YouTube
import os


def dowload_video(url, type='audio'):
    yt = YouTube(url)
    audio_id = uuid.uuid4().fields[-1]
    if type =='audio':
        yt.streams.filter(only_audio=True).first().download("media/audio", f"{audio_id}.mp3")
        return f"{audio_id}.mp3"
    elif type == 'video':
        return f"{audio_id}.mp4"


@dp.callback_query_handler(text='back', state=[Dowload.dowload])
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='downloadyoutube')
async def start_dow(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    global msg_download
    msg_download = await call.message.edit_text(text=f"Введите ссылку с YouTube для скачивания аудио: ", reply_markup=kb_back)
    await Dowload.dowload.set()

@dp.message_handler(state=Dowload.dowload)
async def dowload(message: types.Message, state: FSMContext):
    await msg_download.delete()
    title = dowload_video(message.text)
    audio = open(f'media/audio/{title}', 'rb')
    await dp.bot.send_audio(message.chat.id, audio)
    await message.delete()
    os.remove(f'media/audio/{title}')
    await message.answer(text="Готово!\n"
                              "Воспользуйтесь кнопками меню", reply_markup=kb_menu_panel)
    await state.finish()