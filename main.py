import requests
import threading

import telebot
from telebot import types
from telebot.types import InlineKeyboardButton

import logger as log

import datetime as DT
import time
import config

from data_base import dbcon
import sql as sql_

import notification as n
from _locale import Error
from myTime import then
from myTime import then3

bot = telebot.TeleBot(token=config.TOKEN, threaded=True)
now_time = DT.datetime.now()

print('server started')
log.server_started(now_time)

db = dbcon()
sql_.create_connection_mysql_db(db)
log.log_Connect_sql()

def do_work():
    """метод ожидания нужного времени и даты для уведомления второй поток"""
    print("...1...")
    while True:
        """уведомление, когда пришли ответы на все запросы по НД"""
        print("...3...")
        if DT.datetime.now().strftime("%H:%M") == then3:
            res = n.notif(db)
            try:
                if res != None:
                    for i in res:
                        params = {
                            'chat_id': i[0],
                            'text': f'{i[2]} {i[3]}\n\nНа все запросы по Вашему делу пришли ответы!!!'
                                    f'\nВам необходимо записаться к нотариусу {i[10]} в срок до {i[9]}',
                        }
                        response = requests.get('https://api.telegram.org/bot' + config.TOKEN + '/sendMessage',
                                                params=params)
                        log.replies_received(i[2], i[3])
            except Error as e:
                print('Error sending message', e)
                log.log_error(e)

        """уведомление за месяц до срока 6 месяцев"""
        if DT.datetime.now().strftime("%H:%M") == then:
            try:
                cursor = db.cursor()
                sql = """select * from personNotary where data_sms = ? """
                cursor.execute(sql, (DT.datetime.now().strftime("%d.%m.%Y"),))
                query_result = cursor.fetchall()
                if len(query_result) != 0:
                    for row in query_result:
                        params = {
                            'chat_id': row[0],
                            'text': f'{row[2]} {row[3]}\n\nВам необходимо записаться к нотариусу {row[10]} в срок до {row[9]}',
                        }
                        response = requests.get('https://api.telegram.org/bot' + config.TOKEN + '/sendMessage',
                                                params=params)
                        sql_.otm(row[0], db)
                    time.sleep(65)
                else:
                    time.sleep(30)
            except Error as e:
                print('Error sending message', e)
                log.log_error(e)
        else:
            time.sleep(30)
            print(DT.datetime.now().strftime("%H:%M"))
print("...2...")
@bot.message_handler(commands=['start'])
def start(message):
    """при переходе в меню /start пользователь подтверждает свой телефон для его
    идентификации в таблице."""
    log.log_start(message, now_time)

    photo = open('logo.jpg', 'rb')
    name = message.from_user.first_name
    if message.from_user.last_name == None:
        last_name = ""
    else:
        last_name = message.from_user.last_name

    mess = f'<b>Здравствуйте, {name} {last_name}</b>' \
           f'\n\nВас приветствует бот Нотариальной конторы Оршанского района и города Орши\n' \
           f'Для дальнейшего уведомления ВАС по Вашему наследственному делу' \
           f'\nподтвердите пожалуйста свои данные, нажав кнопку \n\n<b><u> 👇 ПРОДОЛЖИТЬ 👇 </u></b>'


    bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(row_width=1)

    tel = types.KeyboardButton(" ПРОДОЛЖИТЬ ", request_contact=True)
    markup.add(tel)
    bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode="html")

# def create_id(message):
#     """метод принимает введённые пользователем фамилию и последние 4 цифры телефона(ms) и присваивает переменным
#     l_name - имя
#     tel - телефон
#     если в таблице находит такого человека, то добавляеь id
#     и возвращает res [со значением срока = 6 месяцев, фамилией нотариуса]
#     если не нашёл, то возвращает None"""
#
#     mess_except = f'❌oooops, попробуйте ещё раз\n\nвведите внимательно' \
#            f'<b><u>{"ВАШУ ФАМИЛИЮ И ПОСЛЕДНИЕ 4 ЦИФРЫ МОБИЛЬНОГО ТЕЛЕФОНА через пробел"}</u>\n{"Например: Иванов 1234"}</b>'
#
#     ms = sql_.create_id_2(message)
#     if ms == 0:
#         bot.reply_to(message, mess_except, parse_mode="html")
#     else:
#
#         res = sql_.create_id_3(message, ms, db)
#         print("res ", res)
#         if res == None:
#             bot.reply_to(message, mess_except, parse_mode="html")
#         else:
#             markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#
#             button1 = types.KeyboardButton('Перейти на сайт и ознакомиться')
#             button2 = types.KeyboardButton('Написать e-mail')
#             button3 = types.KeyboardButton('Информация о моём деле')
#
#             markup.add(button1, button2, button3)
#
#             mess = f'{message.from_user.first_name} {message.from_user.last_name}' \
#                    f'\n✅Вы успешно зарегистрированы!\nВаш нотариус <u><b>{res[1]}</b></u>\nОжидайте уведомление до <u><b>{res[0]}</b></u>\n' \
#                    f'\nТак же вы можете найти полезную информацию на официальном сайте БНП\nи ' \
#                    f'там ознакомиться с режимами работы нотариальных контор и нотариусов'
#             bot.send_message(message.chat.id, mess + '\U0001f600', reply_markup=markup, parse_mode="html")

@bot.message_handler(content_types=["contact"])
def contact(message):
    # global telefon
    telephon = message.contact.phone_number
    id_tel = message.chat.id
    res = sql_.create_reg(telephon, id_tel, db)
    if res == False:

        mess_except = f'❌Извините, вы не найдены в базе данных\n\n' \
                       f'<b><u>{"Наберите подалуйста по номеру телефона 📞..."}</u></b>'
        bot.send_message(message.chat.id, mess_except, parse_mode="html")
    else:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton('Перейти на сайт и ознакомиться')
        button2 = types.KeyboardButton('Написать e-mail')
        button3 = types.KeyboardButton('Информация о моём деле')

        markup.add(button1, button2, button3)

        mess = f'{res[0]} {res[1]}' \
               f'\n✅Вы успешно зарегистрированы!\nВаш нотариус <u><b>{res[3]}</b></u>\nОжидайте уведомление до <u><b>{res[2]}</b></u>\n' \
               f'\nТак же вы можете найти полезную информацию на официальном сайте БНП\nи ' \
               f'там ознакомиться с режимами работы нотариальных контор и нотариусов'
        bot.send_message(message.chat.id, mess + '\U0001f600', reply_markup=markup, parse_mode="html")

@bot.message_handler(commands=['help'])
def help(message):
    log.log_help(message)
    l_name = message.from_user.last_name
    if l_name == None:
        l_name = " "
    mess = f'<b>{message.from_user.first_name} <u>{l_name}</u></b>\nЕсли Вам нужно ' \
           f'ознакомиться с режимом работы нотариусов и их контактными данными,\nперейдите на сайт, нажав на соответсвующую кнопку' \
           f'\n  "<b>{"Перейти на сайт и ознакомиться"}"</b>\n\nЕсли Вам необходимо написать письмо в нотариальную контору,' \
           f'Перейдите в меню   <b>{"Написать e-mail"}</b>'
    bot.send_message(message.chat.id, mess, parse_mode="html")

@bot.message_handler(content_types=["sticker"])
def send_sticker(message):
    """Получим ID Стикера"""

    sticker_id = message.sticker.file_id
    bot.send_sticker(message.chat.id, sticker_id)
    log.log_sticker(message, sticker_id)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        name = message.from_user.first_name
        if message.from_user.last_name == None:
            last_name = "!"
        else:
            last_name = message.from_user.last_name

        if message.text == 'Информация о моём деле':
            log.log_res(message)
            sign_up_for_a_month = sql_.info_srok(message.from_user.id, message.from_user.first_name, db)
            print('sign', sign_up_for_a_month)
            notarius = sql_.info_notarius(message.from_user.id, db)
            print('notarius', notarius)
            zapros = sql_.info_zapros(message.from_user.id, db)
            print('zapros', zapros)
            if zapros == None:
                zapros = "Ответы на запросы ожидаются от организаций! Как только все запросы будут получены," \
                         " Вам придёт уведомление от меня"

            else:
                zapros = f'<b>Ответы на запросы получены, об этом Вы были </b>'

            mess = f'<b>{name} <u>{last_name}</u></b>\n\nв срок до <b>{sign_up_for_a_month}</b>' \
                   f'\nВам необходимо записаться к нотариусу <b>{notarius}</b>' \
                   f'\n{zapros}💁'

            bot.send_message(message.chat.id, mess, parse_mode="html")
            bot.send_message(message.from_user.id,
                             'Так же вы можете найти интересующую Вас информацию о наследственном деле на '
                             'ОФИЦИАЛЬНОМ сайте нотариата Республики Беларусь\n'
                             '*Перейдя по ссылке*\n' + '\u261E' + '[НАЖМИ ТУТ](https://enotary.by/#/legacy/)',
                             parse_mode='Markdown')

        elif message.text == 'Перейти на сайт и ознакомиться':
            log.log_res(message)
            bot.send_message(message.from_user.id,
                        'Для ознакомления с режимом работы нотариальных контор\nРежимом работы нотариусов\n'
                        '*Перейдите по ссылке*\n' + '[ссылке](https://belnotary.by/nayti-notariusa/notariusy-belarusi/)',
                         parse_mode='Markdown')

        elif message.text == 'Написать e-mail':
            log.log_res(message)
            mess = f'<b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>\nвыберите в какую нотариальную контору' \
                   f'\nВ какую контору Вы хотите написать письмо или позвонить?'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton('контора Витебского нотариального округа')
            # button2 = types.KeyboardButton('контора Минского нотариального округа')
            # button3 = types.KeyboardButton('контора Брестского нотариального округа')
            # button4 = types.KeyboardButton('контора Гродненского нотариального округа')
            # button5 = types.KeyboardButton('контора Гомельского нотариального округа')
            # button6 = types.KeyboardButton('контора Могилёвского нотариального округа')
            back = types.KeyboardButton('Назад')

            markup.add(button1, back)
            bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode="html")

        elif message.text == "Назад":
            log.log_res(message)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

            button1 = types.KeyboardButton('Информация о моём деле')
            button2 = types.KeyboardButton('Перейти на сайт и ознакомиться')
            button3 = types.KeyboardButton('Написать e-mail')

            markup.add(button1, button2, button3)
            bot.send_message(message.chat.id, "Назад", reply_markup=markup)

        elif message.text == "контора Витебского нотариального округа":

            log.log_res(message)
            mess = f'<b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>\nвыберите в какую нотариальную контору' \
                   f'\nВы хотите написать письмо'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton('Нотариальная контора Оршанского района и г.Орши')
            button2 = types.KeyboardButton('Нотариальная контора г.Барани Оршанского района')

            back = types.KeyboardButton('Назад')

            markup.add(button1, button2, back)
            bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode="html")

        elif message.text == "Нотариальная контора Оршанского района и г.Орши":
            log.log_res(message)
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = InlineKeyboardButton("Написать письмо",
                                                  url='https://notariat-orsha@mail.ru')
            button2 = InlineKeyboardButton("Перейти на сайт и Позвонить",
                                                  url='https://belnotary.by/nayti-notariusa/notarialnye-kontory-i-notarialnye-byuro/notarialnaya-kontora-orshanskogo-rayona-i-goroda-orshi/')
            markup.add(button1, button2)


            bot.send_message(message.chat.id, "написать письмо или позвонить?", reply_markup=markup)

        elif message.text == "Нотариальная контора г.Барани Оршанского района":

            log.log_res(message)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Написать письмо",
                                                  url='https://nk_barnf@mail.ru'))

            bot.send_message(message.chat.id, "написать письмо?", reply_markup=markup)

        else:
            mess = f'{message.text}\n\n<b>{name} <u>{last_name}</u></b>' \
                   f'\n\nЯ Вас не понимаю!! '

            bot.send_message(message.chat.id, mess + '\U0001F534', parse_mode="html")

# stop = True
# bot.polling(none_stop=True, interval=0)
if __name__ == '__main__':
    threaded = threading.Thread(target=do_work, daemon=True).start()
    bot.polling(none_stop=True)
    # bot.start_polling(bot, skip_updates=True)