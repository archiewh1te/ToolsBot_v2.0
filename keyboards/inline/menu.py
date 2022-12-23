from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура панели
kb_menu_panel = InlineKeyboardMarkup(row_width=2)
btn_info_ip_site = InlineKeyboardButton(text='🌐Узнать IP сайта', callback_data='infoipsite',)
btn_weather = InlineKeyboardButton(text='🌤Узнать погоду', callback_data='infoweather')
btn_info_ip = InlineKeyboardButton(text='📄Информация об IP', callback_data='ipinfo')
btn_search_youtube = InlineKeyboardButton(text='🎥Поиск в YouTube', callback_data='searchyoutube')
btn_search_google = InlineKeyboardButton(text='🔍Поиск в Google', callback_data='searchgoogle')
btn_translate = InlineKeyboardButton(text='💡Переводчик', callback_data='translate')
btn_send_video = InlineKeyboardButton(text='🎵Конвертация в аудио', callback_data='video')
btn_download_video_youtube = InlineKeyboardButton(text='⬇️Скачать Аудио с YouTube', callback_data='downloadyoutube')

kb_menu_panel.add(btn_info_ip_site, btn_weather, btn_info_ip, btn_search_youtube, btn_search_google, btn_translate, btn_send_video, btn_download_video_youtube)

kb_back = InlineKeyboardMarkup(row_width=1)
btn_back = InlineKeyboardButton(text='⬅Назад', callback_data='back')

kb_back.add(btn_back)


# Клавиатура Стран Переводчика
kb_menu_translation = InlineKeyboardMarkup(row_width=2)
btn_english = InlineKeyboardButton(text='🇬🇧Английский', callback_data='eng_lang')
btn_belarus = InlineKeyboardButton(text='🇧🇾Белорусский', callback_data='belarussian_lang')
btn_bolgaria = InlineKeyboardButton(text='🇧🇬Болгарский', callback_data='bulgarian_lang')
btn_spanish = InlineKeyboardButton(text='🇪🇸Испанский', callback_data='spanish_lang')
btn_italia = InlineKeyboardButton(text='🇮🇹Итальянский', callback_data='italian_lang')
btn_kazakh = InlineKeyboardButton(text='🇰🇿Казахский', callback_data='kazakh_lang')
btn_canada = InlineKeyboardButton(text='🇨🇦Канадский', callback_data='canada_lang')
btn_korea = InlineKeyboardButton(text='🇰🇷Корейский', callback_data='korean_lang')
btn_china = InlineKeyboardButton(text='🇨🇳Китайский(традиционный)', callback_data='chinese_lang')
btn_deutsch = InlineKeyboardButton(text='🇩🇪Немецкий', callback_data='german_lang')
btn_romania = InlineKeyboardButton(text='🇷🇴Румынский', callback_data='romanian_lang')
btn_russia = InlineKeyboardButton(text='🇷🇺Русский', callback_data='russian_lang')
btn_francia = InlineKeyboardButton(text='🇫🇷Французский', callback_data='french_lang')
btn_japan = InlineKeyboardButton(text='🇯🇵Японский', callback_data='japanese_lang')

kb_menu_translation.add(btn_english, btn_belarus, btn_bolgaria,btn_spanish, btn_italia, btn_kazakh, btn_canada,
                        btn_korea, btn_china, btn_deutsch, btn_romania, btn_russia, btn_francia, btn_japan)

btn_back = InlineKeyboardButton(text='⬅Назад', callback_data='back')

kb_menu_translation.add(btn_back)

