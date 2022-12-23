import requests
import datetime
from keyboards.inline import kb_menu_panel, kb_back
from loader import dp
from data.config import weather_key
from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.misc import rate_limit


@dp.callback_query_handler(text='back', state='weather')
async def quit(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.edit_text('Для продолжения воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)


@rate_limit(limit=5)
@dp.callback_query_handler(text='infoweather')
async def start_weather(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    global msg_weather
    msg_weather = await call.message.edit_text("Привет! напиши мне название города и я пришлю сводку погоды!", reply_markup=kb_back)
    await state.set_state("weather")


@dp.message_handler(state="weather")
async def get_weather(message: types.Message, state: FSMContext):
    await msg_weather.delete()
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        # --------------------- данный запрос синхронный, что делает данную функцию блокирующей
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_key}&units=metric"
        )
        data = r.json()
        # --------------------------------------------------------------------------------------
        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            f"***Хорошего дня***"
                            )
        await state.finish()  # ------ Сбрасываем состояние
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")
    await message.answer('Воспользуйтесь кнопками меню', reply_markup=kb_menu_panel)