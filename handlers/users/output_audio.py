import time
from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu import kb_menu_panel, kb_back
from loader import dp
from utils.misc import rate_limit
import uuid
import os
from moviepy.editor import *

@dp.callback_query_handler(text='back', state='get_audio')
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='video')
async def send_video(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    global msg_video
    msg_video = await call.message.edit_text('Пожалуйста, пришлите видео для конвертации: ', reply_markup=kb_back)
    await state.set_state("get_audio")  # ---- назначем состояние

@dp.message_handler(state='get_audio', content_types=ContentType.VIDEO)  # ---- получаем стейт get_audio (который назаначен выше)
async def get_audio(message: types.Message, state: FSMContext):
    await msg_video.delete()
    await message.delete()
    file_id = message.video.file_id  # ---- Get file id
    file = await dp.bot.get_file(file_id)  # ---- Get file path
    unique_filename = str(uuid.uuid4())
    await dp.bot.download_file(file.file_path, f"media/video/video{unique_filename}.mp4") # ---- download and save video
    await message.answer('Подождите, видео обрабатывается 🔄')
    time.sleep(0.33)

    audioclip = AudioFileClip(f"media/video/video{unique_filename}.mp4")  # ---- path to video converted
    audioclip.write_audiofile(f"media/audio/out_audio{unique_filename}.mp3", buffersize=20000) # ---- before converted out audio from video
    await dp.bot.send_audio(chat_id=message.chat.id, audio=open(f'media/audio/out_audio{unique_filename}.mp3', 'rb'))
    os.remove(f'media/video/video{unique_filename}.mp4')
    os.remove(f'media/audio/out_audio{unique_filename}.mp3')
    await message.answer('Готово!\n'
                         'Воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)
    await state.finish()  # ---- Сбрасываем состояние



