import requests
import emoji
from emoji import SMILE

import telebot
import logger as log
from telebot.types import InlineKeyboardButton
from aifc import Error
import time
import config
import datetime as DT
from data_base import dbcon
from telebot import types
import sql as sql_
import threading
import notification as n

from myTime import then
from myTime import then2
from myTime import then3

bot = telebot.TeleBot(token=config.TOKEN, threaded=True)

now_time = DT.datetime.now()
# dp = Dispatcher(bot)

print('server started')
log.server_started(now_time)

db = dbcon()
sql_.create_connection_mysql_db(db)
print("..Connect")
log.log_Connect_sql()

# stop = False
print("1...")

def do_work():

    while True:
        """метод ожидания нужного времени и даты для уведомления второй поток"""
        print("3...")
        if DT.datetime.now().strftime("%H:%M") == then3:
            print("4...")
            print("then3 ", then3)

            res = n.notif(db)
            print(res)
            for i in res:
                print("res[] ", i[2])

                params = {
                    'chat_id': i[0],
                    'text': f'{i[2]} {i[3]}\nНа все запросы по Вашему делу пришли ответы!!!'
                            f'Вам необходимо записаться к нотариусу {i[10]} в срок до {i[9]}',
                }
                response = requests.get('https://api.telegram.org/bot' + config.TOKEN + '/sendMessage',
                                        params=params)

        if DT.datetime.now().strftime("%H:%M") == then or DT.datetime.now().strftime("%H:%M") == then2:
            print("5... if == ")
            try:
                cursor = db.cursor()
                sql = """select * from personNotary where data_sms = ? """

                cursor.execute(sql, (DT.datetime.now().strftime("%d.%m.%Y"),))
                query_result = cursor.fetchall()
                print(len(query_result))
                if len(query_result) != 0:
                    for row in query_result:
                        print("найден пользователь", row)
                        # log.query_res(row)
                        print(row[0])
                        params = {
                            'chat_id': row[0],
                            'text': f'{row[2]} {row[3]}\nВам необходимо записаться к нотариусу {row[10]} в срок до {row[9]}',
                        }
                        response = requests.get('https://api.telegram.org/bot' + config.TOKEN + '/sendMessage',
                                                params=params)
                        print("6...")
                        print("row[0] ", row[0])

                        sql_.otm(row[0], db)
                    time.sleep(65)
                else:
                    break

            except Error as e:

                print('Error sending message', e)
                log.log_error(e)

        else:
            print("7...")
            print("sleep if != ")
            time.sleep(30)

            print("t 2 = ", DT.datetime.now().strftime("%H:%M"))


# threaded = threading.Thread(target=do_work).start()
print("2...")

@bot.message_handler(commands=['start'])

def start(message):
    """при переходе в меню /start пользователь вводит фамилию и последние цифры телефона для его
    идентификации в таблице. Через next_step_handler передаём в метод create_id"""
    log.log_start(message, now_time)

    photo = open('logo.jpg', 'rb')

    mess = f'<b>Здравствуйте,</b>\n <b>{message.from_user.first_name} <u>{message.from_user.last_name}' \
           f'</u></b>\nВас приветствует бот Нотариальной конторы Оршанского района и города Орши\n' \
           f'Для дальнейшего уведомления ВАС об информации по Вашему делу введите ' \
           f'<b><u>{"ВАШУ ФАМИЛИЮ И ПОСЛЕДНИЕ 4 ЦИФРЫ МОБИЛЬНОГО ТЕЛЕФОНА через пробел"}</u>\n{"Например: Иванов 1234"}</b>'

    bot.send_photo(message.chat.id, photo)
    msg = bot.reply_to(message, mess, parse_mode="html")
    bot.register_next_step_handler(msg, create_id)

def create_id(message):
    """метод принимает введённые пользователем фамилию и последние 4 цифры телефона(ms) и присваивает переменным
    l_name - имя
    tel - телефон
    если в таблице находит такого человека, то добавляеь id
    и возвращает res [со значением срока = 6 месяцев, фамилией нотариуса]
    если не нашёл, то возвращает None"""

    mess_except = f'❌oooops, попробуйте ещё раз\n\nвведите внимательно' \
           f'<b><u>{"ВАШУ ФАМИЛИЮ И ПОСЛЕДНИЕ 4 ЦИФРЫ МОБИЛЬНОГО ТЕЛЕФОНА через пробел"}</u>\n{"Например: Иванов 1234"}</b>'

    ms = sql_.create_id_2(message)
    if ms == 0:
        bot.reply_to(message, mess_except, parse_mode="html")
    else:

        res = sql_.create_id_3(message, ms, db)
        print("res ", res)
        if res == None:
            bot.reply_to(message, mess_except, parse_mode="html")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

            button1 = types.KeyboardButton('Перейти на сайт и ознакомиться')
            button2 = types.KeyboardButton('Написать e-mail')

            markup.add(button1, button2)

            mess = f'{message.from_user.first_name} {message.from_user.last_name}' \
                   f'\n✅Вы успешно зарегистрированы!\nВаш нотариус <u><b>{res[1]}</b></u>\nОжидайте уведомление до <u><b>{res[0]}</b></u>\n' \
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

        if message.text == 'Перейти на сайт и ознакомиться':
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
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button2 = types.KeyboardButton('Перейти на сайт и ознакомиться')
            button3 = types.KeyboardButton('Написать e-mail')
            markup.add(button2, button3)
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
            mess = f'{message.text}\n\n<b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>' \
                   f'\n\nЯ Вас не понимаю!! '

            bot.send_message(message.chat.id, mess + '\U0001F534', parse_mode="html")

# stop = True
# bot.polling(none_stop=True, interval=0)
if __name__ == '__main__':
    threaded = threading.Thread(target=do_work, daemon=True).start()
    bot.polling(none_stop=True)
    # bot.start_polling(bot, skip_updates=True)