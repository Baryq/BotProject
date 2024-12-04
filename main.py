import telebot
from important_vars import token, file_ids, admins_ids
from datetime import datetime

# file_ids словарь с id картинок в виде
# file_ids = {'Вышмат': 'id',
#             'Геодезия': 'id',
#             'Термех': 'id',
#             'Сопромат': 'id',
#             'Физика': 'id',
#             'Моделирование': 'id',
#             'Информатика': 'id',
#             'Начерт': 'id',
#             'интро': 'id',
#             'другое': 'id'}

# admins_ids список с id пользователей, которые считаются админами

bot = telebot.TeleBot(token)
report = dict()
is_on = True # включен бот или нет

# Для логов в консоль
# def print_logs(message: telebot.types.Message, reply: str):
#     print(f'--------------------------------------------------------------------------------\n'
#           f'Текст сообщения: "{message.text}"\n'
#           f'Ответ бота: "{reply}"\n'
#           f'ID чата: {message.chat.id}\n'
#           f'ID пользователя: {message.from_user.id}\n'
#           f'Имя пользователя: {message.from_user.username}\n'
#           f'Время получения сообщения: {datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')}')


def print_logs(message: telebot.types.Message, reply: str):
    pass

# Формирует отчет, который потом получит админ
def make_report(username: str):
    global report
    report_text = (f'Запрос от пользователя @{username}:\n'
                   f'Семестр: {report[username]['Семестр'] if 'Семестр' in report[username] else '???'}\n'
                   f'Дисциплина: {report[username]['Дисциплина'] if 'Дисциплина' in report[username] else '???'}\n'
                   f'Работа: {report[username]['Работа'] if 'Работа' in report[username] else '???'}\n'
                   f'Тип: {report[username]['Тип'] if 'Тип' in report[username] else '???'}')
    return report_text


# Обработчик сообщений пользователя
@bot.message_handler(commands=['start', 'help'], func=lambda message: is_on)
def welcome_handler(message):
    reply = 'Привет, какой предмет тебя интересует?'
    keyboard = telebot.types.InlineKeyboardMarkup([
        [telebot.types.InlineKeyboardButton('Начерт (или инжграф)', callback_data='Начерт')],
        [telebot.types.InlineKeyboardButton('Вышмат', callback_data='Вышмат')],
        [telebot.types.InlineKeyboardButton('Геодезия', callback_data='Геодезия')],
        [telebot.types.InlineKeyboardButton('Термех', callback_data='Термех')],
        [telebot.types.InlineKeyboardButton('Сопромат', callback_data='Сопромат')],
        [telebot.types.InlineKeyboardButton('Физика', callback_data='Физика')],
        [telebot.types.InlineKeyboardButton('Моделирование', callback_data='Моделирование')],
        [telebot.types.InlineKeyboardButton('Информатика', callback_data='Информатика')],
        [telebot.types.InlineKeyboardButton('Другой предмет', callback_data='другое')],
    ])

    bot.send_photo(message.chat.id, file_ids['интро'], reply, reply_markup=keyboard)
    print_logs(message, reply)


# Обработчик callback_query от пользователя
@bot.callback_query_handler(func=lambda call: is_on and call.data not in ['Включить бота', 'Выключить бота'])
def inline_callback_handler(call):
    global report
    message = call.message
    data = call.data

    try:
        report[call.from_user.username]
    except KeyError:
        report[call.from_user.username] = {}

    if data in ['Начерт', 'Вышмат', 'Геодезия', 'Моделирование', 'Термех', 'Сопромат', 'Физика',
                'Информатика', 'другое']:
        report[call.from_user.username]['Дисциплина'] = data
        reply = 'Отлично, какая работа тебя интересует?'
        keyboard = telebot.types.InlineKeyboardMarkup([
            [telebot.types.InlineKeyboardButton('Д/з', callback_data='Д/з')],
            [telebot.types.InlineKeyboardButton('РГР', callback_data='РГР')],
            [telebot.types.InlineKeyboardButton('Помощь с экзаменом / ср', callback_data='Помощь с экзаменом / ср')],
            [telebot.types.InlineKeyboardButton('В начало <-', callback_data='В начало')]
        ])

        bot.edit_message_media(telebot.types.InputMediaPhoto(file_ids[data], reply), message.chat.id,
                               message.message_id, reply_markup=keyboard)

    elif data == 'Д/з' and report[call.from_user.username]['Дисциплина'] == 'Начерт':
        report[call.from_user.username]['Работа'] = data
        reply = 'На каком ты семестре?'
        keyboard = telebot.types.InlineKeyboardMarkup([
            [telebot.types.InlineKeyboardButton('1 семестр', callback_data='1 семестр'),
             telebot.types.InlineKeyboardButton('2 семестр', callback_data='2 семестр')],
        ])
        bot.edit_message_caption(reply, message.chat.id, message.message_id, reply_markup=keyboard)

    elif data == '1 семестр':
        report[call.from_user.username]['Семестр'] = data
        reply = 'Что тебе нужно сделать?'
        keyboard = telebot.types.InlineKeyboardMarkup([
            [telebot.types.InlineKeyboardButton('1 эпюр — 1200 руб', callback_data='1 эпюр')],
            [telebot.types.InlineKeyboardButton('2 эпюр — 1000 руб', callback_data='2 эпюр')],
            [telebot.types.InlineKeyboardButton('3 эпюр — 1000 руб', callback_data='3 эпюр')],
            [telebot.types.InlineKeyboardButton('План — 2500 - 3500 руб', callback_data='План')],
            [telebot.types.InlineKeyboardButton('Разрез — 800 руб', callback_data='Разрез')],
            [telebot.types.InlineKeyboardButton('В начало <-', callback_data='В начало')]
        ])
        bot.edit_message_caption(reply, message.chat.id, message.message_id, reply_markup=keyboard)

    elif data == '2 семестр':
        report[call.from_user.username]['Семестр'] = data
        reply = 'Что тебе нужно сделать?'
        keyboard = telebot.types.InlineKeyboardMarkup([
            [telebot.types.InlineKeyboardButton('Топоплан — 1500', callback_data='Топоплан')],
            [telebot.types.InlineKeyboardButton('Разрез — 800', callback_data='Разрез')],
            [telebot.types.InlineKeyboardButton('Отмывка — 800', callback_data='Отмывка')],
            [telebot.types.InlineKeyboardButton('В начало <-', callback_data='В начало')]
        ])
        bot.edit_message_caption(reply, message.chat.id, message.message_id, reply_markup=keyboard)

    elif data == 'Д/з' and report[call.from_user.username]['Дисциплина'] != 'Начерт':
        report[call.from_user.username]['Работа'] = data
        reply = 'Пришлите фотографии работы, в ближайшее время с вами свяжутся'
        keyboard = telebot.types.InlineKeyboardMarkup()
        bot.edit_message_caption(reply, message.chat.id, message.message_id, reply_markup=keyboard)

    elif data in ['1 эпюр', '2 эпюр', '3 эпюр', 'План', 'Разрез', 'Топоплан', 'Отмывка']:
        report[call.from_user.username]['Тип'] = data
        reply = 'Пришлите фотографии работы, в ближайшее время с вами свяжутся'
        keyboard = telebot.types.InlineKeyboardMarkup()
        bot.edit_message_caption(reply, message.chat.id, message.message_id, reply_markup=keyboard)

    elif data in ['РГР', 'Помощь с экзаменом / ср']:
        report[call.from_user.username]['Работа'] = data
        reply = 'Записал ответы, в ближайшее время с вами свяжется менеджер'
        keyboard = telebot.types.InlineKeyboardMarkup()
        bot.edit_message_caption(reply, message.chat.id, message.message_id, reply_markup=keyboard)

        for admin_id in admins_ids:
            text = make_report(call.from_user.username)
            bot.send_message(admin_id, text)

        report[call.from_user.username] = {}

    elif data == 'В начало':
        report[call.from_user.username] = {}
        reply = 'Начнем с начала, какой предмет тебя интересует?'
        keyboard = telebot.types.InlineKeyboardMarkup([
            [telebot.types.InlineKeyboardButton('Начерт (или инжграф)', callback_data='Начерт')],
            [telebot.types.InlineKeyboardButton('Вышмат', callback_data='Вышмат')],
            [telebot.types.InlineKeyboardButton('Геодезия', callback_data='Геодезия')],
            [telebot.types.InlineKeyboardButton('Термех', callback_data='Термех')],
            [telebot.types.InlineKeyboardButton('Сопромат', callback_data='Сопромат')],
            [telebot.types.InlineKeyboardButton('Физика', callback_data='Физика')],
            [telebot.types.InlineKeyboardButton('Моделирование', callback_data='Моделирование')],
            [telebot.types.InlineKeyboardButton('Информатика', callback_data='Информатика')],
            [telebot.types.InlineKeyboardButton('Другой предмет', callback_data='другое')],
        ])
        bot.edit_message_media(telebot.types.InputMediaPhoto(file_ids['интро'], reply), message.chat.id,
                               message.message_id, reply_markup=keyboard)
    else:
        pass

    bot.answer_callback_query(call.id)


# Для загрузки новых изображений на сервера Telegram
# @bot.message_handler(func=lambda call: call.from_user.id in admins_ids, content_types=['photo'])
# def file_id_handler(message):
#     reply = message.photo[0].file_id
#     bot.send_message(message.chat.id, reply)
#     print_logs(message, reply)


# Обработчик фото и документов от пользователя
@bot.message_handler(content_types=['photo', 'document'], func=lambda message: is_on)
def photo_handler(message):
    global report
    if message.from_user.username in report:
        reply = 'Записал ответы, в ближайшее время с вами свяжется менеджер'
        bot.reply_to(message, reply)

        for admin_id in admins_ids:
            text = make_report(message.from_user.username)
            bot.forward_message(admin_id, message.chat.id, message.message_id)
            bot.send_message(admin_id, text)

        del report[message.from_user.username]
    else:
        welcome_handler(message)


# Обработчик сообщений от админа
@bot.message_handler(func=lambda message: message.from_user.id in admins_ids, commands=['admin'])
def admin_message_handler(message):
    reply = 'Привет, бог'
    if is_on:
        keyboard = telebot.types.InlineKeyboardMarkup(
            [[telebot.types.InlineKeyboardButton('Выключить бота', callback_data='Выключить бота')]])
    else:
        keyboard = telebot.types.InlineKeyboardMarkup(
            [[telebot.types.InlineKeyboardButton('Включить бота', callback_data='Включить бота')]])
    bot.send_message(message.chat.id, reply, reply_markup=keyboard)
    print_logs(message, reply)


# Обработчик callback_query от админа
@bot.callback_query_handler(func=lambda call: call.from_user.id in admins_ids)
def admin_callback_handler(call):
    global is_on
    message = call.message
    if call.data == 'Выключить бота':
        is_on = False
        reply = 'Бот выключен. Включить обратно?'
        keyboard = telebot.types.InlineKeyboardMarkup(
            [[telebot.types.InlineKeyboardButton('Включить бота', callback_data='Включить бота')]])
        bot.edit_message_text(reply, chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    if call.data == 'Включить бота':
        is_on = True
        reply = 'Бот включен. Выключить обратно?'
        keyboard = telebot.types.InlineKeyboardMarkup(
            [[telebot.types.InlineKeyboardButton('Выключить бота', callback_data='Выключить бота')]])
        bot.edit_message_text(reply, chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

    bot.answer_callback_query(call.id)


# Обработчик сообщений, для которых нет отдельного обработчика
@bot.message_handler(func=lambda m: True)
def wrong_message_handler(message):
    reply = '<No response>'
    print_logs(message, reply)


bot.infinity_polling()
