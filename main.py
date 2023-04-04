import requests
import threading
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

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
from exel import x_file
from exel import zapis_not
import case as C
import text_messages as tm
import button_file as bf

bot = telebot.TeleBot(token=config.TOKEN, threaded=True)
now_time = DT.datetime.now()

print('server started')
log.server_started(now_time)

db = dbcon()
sql_.create_connection_mysql_db(db)
log.log_Connect_sql()

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')

def do_work():
    """метод ожидания нужного времени и даты для уведомления второй поток"""
    print("...1...")
    while True:
        """уведомление, когда пришли ответы на все запросы по НД"""
        print("...3...")
        if DT.datetime.now().strftime("%H:%M") == then3:
            res = n.notif(db)
            try:
                if res is not None:
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

        # уведомление за месяц до срока 6 месяцев
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
    if message.from_user.last_name is None:
        last_name = ""
    else:
        last_name = message.from_user.last_name

    mess = f'<b>Здравствуйте, {name} {last_name}</b>' + tm.text_start()


    bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(row_width=1)

    tel = types.KeyboardButton(" ПРОДОЛЖИТЬ \n и поделиться контактом", request_contact=True)
    markup.add(tel)

    bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode="html")


@bot.message_handler(content_types=["contact"])
def contact(message):
    telephone = message.contact.phone_number
    id_tel = message.chat.id
    res = sql_.create_reg(telephone, id_tel, db)
    if res is False:
        sql_.create_new_person(id_tel, telephone, message.from_user.first_name, message.from_user.last_name, db)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton('Перейти на сайт и ознакомиться')
        button2 = types.KeyboardButton('Написать e-mail')
        button3 = types.KeyboardButton('Информация о моём деле')
        button4 = types.KeyboardButton('Записаться на приём к нотариусу')

        markup.add(button1, button2, button3, button4)
        if message.from_user.first_name is not None:
            name = message.from_user.first_name
        else:
            name = ""
        if message.from_user.last_name is not None:
            last_name = message.from_user.last_name
        else:
            last_name = ""
        mess = f'{name} {last_name}' + tm.reg_ok()
        bot.send_message(message.chat.id, mess + '\U0001f600', reply_markup=markup, parse_mode="html")
    else:
        if res[3] is None:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            button1 = types.KeyboardButton('Перейти на сайт и ознакомиться')
            button2 = types.KeyboardButton('Написать e-mail')
            button3 = types.KeyboardButton('Информация о моём деле')
            button4 = types.KeyboardButton('Записаться на приём к нотариусу')
            markup.add(button1, button2, button3, button4)
            mess = f'<b>{res[0]} {res[1]}</b>' + tm.reg_ok() + tm.reg_ok2()
            bot.send_message(message.chat.id, mess + '\U0001f600', reply_markup=markup, parse_mode="html")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            button1 = types.KeyboardButton('Перейти на сайт и ознакомиться')
            button2 = types.KeyboardButton('Написать e-mail')
            button3 = types.KeyboardButton('Информация о моём деле')
            button4 = types.KeyboardButton('Записаться на приём к нотариусу')

            markup.add(button1, button2, button3, button4)

            mess = f'{res[0]} {res[1]} \n{tm.reg_ok()}' \
                   f'\nВаш нотариус <u><b>{res[3]}</b></u>\n' \
                   f'Ожидайте уведомление до <u><b>{res[2]}</b></u>\n{tm.reg_ok2()}'
            bot.send_message(message.chat.id, mess + '\U0001f600', reply_markup=markup, parse_mode="html")

@bot.message_handler(commands=['help'])
def help_command(message):
    log.log_help(message)
    l_name = message.from_user.last_name
    if l_name is None:
        l_name = " "
    mess = f'<b>{message.from_user.first_name} <u>{l_name}</u></b>\nЕсли Вам нужно ' \
           f'ознакомиться с режимом работы нотариусов и их контактными данными,\nперейдите на сайт, ' \
           f'нажав на соответсвующую кнопку' \
           f'\n  "<b>{"Перейти на сайт и ознакомиться"}"</b>\n\n' \
           f'Если Вам необходимо написать письмо в нотариальную контору,' \
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
    """
    :param message:
    :return:
    sign_up_for_a_month срок извещения
    """
    if message.chat.type == 'private':
        name = message.from_user.first_name
        if message.from_user.last_name is None:
            last_name = ""
        else:
            last_name = message.from_user.last_name

        if message.text == 'Информация о моём деле':
            log.log_res(message)
            sign_up_for_a_month = sql_.info_srok(message.from_user.id, db)
            print('sign', sign_up_for_a_month)
            notarius = sql_.info_notarius(message.from_user.id, db)
            print('notarius', notarius)
            zapros = sql_.info_zapros(message.from_user.id, db)
            print('zapros', zapros)
            if notarius is None:
                mess = 'не найдено наследственное дело в базе. ' \
                       'Уточните информацияю по телефону 📞 +375 216 56-88-94'
                bot.send_message(message.chat.id, mess)

            elif zapros is None:
                zapros = "Ответы на запросы ожидаются от организаций! Как только все запросы будут получены," \
                         " Вам придёт уведомление от меня"
                mess = f'<b>{name} <u>{last_name}</u></b>\n\nв срок до <b>{sign_up_for_a_month}</b>' \
                       f'\nВам необходимо записаться к нотариусу <b>{notarius}</b>' \
                       f'\n{zapros}💁'
                bot.send_message(message.chat.id, mess, parse_mode="html")
                bot.send_message(message.from_user.id,
                                 'Так же вы можете найти интересующую Вас информацию о наследственном деле на '
                                 'ОФИЦИАЛЬНОМ сайте нотариата Республики Беларусь\n'
                                 '*Перейдя по ссылке*\n' + '\u261E' + '[НАЖМИ ТУТ](https://enotary.by/#/legacy/)',
                                 parse_mode='Markdown')
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
            mess = f'<b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>\n' \
                   f'Выберите в какую нотариальную контору' \
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
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)

            button1 = types.KeyboardButton('Информация о моём деле')
            button2 = types.KeyboardButton('Перейти на сайт и ознакомиться')
            button3 = types.KeyboardButton('Написать e-mail')
            button4 = types.KeyboardButton('Записаться на приём к нотариусу')

            markup.add(button1, button2, button3, button4)
            bot.send_message(message.chat.id, "Выберите что Вам необходимо", reply_markup=markup)

        elif message.text == "контора Витебского нотариального округа":
            log.log_res(message)
            mess = f'<b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>\n' \
                   f'Выберите в какую нотариальную контору' \
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
        elif message.text == 'Записаться на приём к нотариусу':
            # log.log_res(message)
            mess = f'<b>{name} <u>{last_name}</u>\n\nчто Вы хотите оформить у нотариуса?</b>📄'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

            markup.add(bf.button_power_of_attorney, bf.button_will, bf.button_agreement, bf.button_statement,
                       bf.button_consultation, bf.button_other_action, bf.back)

            bot.send_message(message.from_user.id, mess, reply_markup=markup, parse_mode="html")
        elif message.text == '✔️Доверенность':
            print(">>>1")
            # log.log_res(message)
            power_of_attorney = "Доверенность"
            mess = f'<b>{name} <u>{last_name}</u>\n\nНа какую дату Вы хотите записаться,' \
                   f' чтобы оформить {power_of_attorney} ??🗓️</b>'

            bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                name=calendar_1.prefix,
                year=now_time.year,
                month=now_time.month), parse_mode="html")
        elif message.text == '✔️Завещание':
            # log.log_res(message)
            power_of_attorney = "Завещание"
            mess = f'<b>{name} <u>{last_name}</u>\n\nНа какую дату Вы хотите записаться,' \
                   f' чтобы оформить {power_of_attorney} ??🗓️</b>'

            bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                name=calendar_1.prefix,
                year=now_time.year,
                month=now_time.month), parse_mode="html")
        elif message.text == '✔️Согласие':
            # log.log_res(message)
            power_of_attorney = "Согласие"
            mess = f'<b>{name} <u>{last_name}</u>\n\nНа какую дату Вы хотите записаться,' \
                   f' чтобы оформить {power_of_attorney} ??🗓️</b>'

            bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                name=calendar_1.prefix,
                year=now_time.year,
                month=now_time.month), parse_mode="html")
        elif message.text == '✔️Заявление':
            # log.log_res(message)
            power_of_attorney = "Заявление"
            mess = f'<b>{name} <u>{last_name}</u>\n\nНа какую дату Вы хотите записаться,' \
                   f' чтобы оформить {power_of_attorney} ??🗓️</b>'

            bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                name=calendar_1.prefix,
                year=now_time.year,
                month=now_time.month), parse_mode="html")
        elif message.text == '✔️Консультация':
            print(">>>1")
            # log.log_res(message)
            power_of_attorney = "Консультация"
            mess = f'<b>{name} <u>{last_name}</u>\n\nНа какую дату Вы хотите записаться,' \
                   f' чтобы оформить {power_of_attorney} ??🗓️</b>'

            bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                name=calendar_1.prefix,
                year=now_time.year,
                month=now_time.month), parse_mode="html")
        elif message.text == '✔️иное действие':
            # log.log_res(message)
            mess = f'<u>{name} {last_name}</u>\n\nДля оформление болеее сложного действия ' \
                   f'Вам необходимо записаться на консультацию для получения необходимого ' \
                   f'Вам перечня документов либо уточнить информацию по телефону 📞 +375 216 56-88-94'
            markup_all = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

            markup_all.add(bf.button_info_delo, bf.button_website, bf.button_mail, bf.button_entry, bf.back)
            bot.send_message(message.chat.id, mess, reply_markup=markup_all, parse_mode="html")
        else:
            mess = f'{message.text}\n\n<b>{name} <u>{last_name}</u></b>' \
                   f'\n\nЯ Вас не понимаю!! '
            bot.send_message(message.chat.id, mess + '\U0001F534', parse_mode="html")


def notarius_time(message, d, power_of_attorney):
    """
    :param power_of_attorney:
    :param message: переходим в метод с выбранным нотариусом
    :param d: принимает день для записи
    notarius сохраняет Фамилию инициалы выбранного нотариуса
    free_time список свободного времени для записи возвращается из  x_file(d, notarius)
    time_work режим работы нотариуса взят из таблицы
    по каждому нотариусу в этот метод возвращается свой список свободного времени для записи
    по которому выводятся кнопки для записи и переходим в метод zapis
    :return: список со свободным временем
    """
    notarius = ''
    free_time = []
    time_work = ''

    if message.chat.type == 'private':
        name = message.from_user.first_name
        if message.from_user.last_name is None:
            last_name = ""
        else:
            last_name = message.from_user.last_name
    try:
        if message.text == "Назад":
            bot_message(message)
        elif message.text == "🟡️ Гоголь Н.А.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)  # по дню и нотариусу найдём свободное время
            time_work = free_time[0]
        elif message.text == "🟡️ Сойка Е.Я.":
            notarius = message.text.split(" ")[1]
            print(notarius)
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == "🟡️ Думанова И.Н.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == '🟡️ Ковалевская А.Г.':
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == "🟡️ Сильченко А.В.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == "🟡️ Бондаренко Ю.П.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == "🟡️ Чикан Н.М.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == "🟡️ Котикова О.В.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == "🟡️ Шинкевич Е.А.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == "🟡️ Позднякова С.Е.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]
        elif message.text == "🟡️ Демидова В.Г.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            time_work = free_time[0]

        if time_work == "выходной":

            mess = bot.send_message(message.from_user.id,
                                    text=f'<b>{name} <u>{last_name}</u>\n\n️'
                                         f'Нотариус {C.notarius_name(notarius)}</b>\n'
                                         f'{d} ‼ НЕ РАБОТАЕТ ‼\n️'
                                         f'\nпопробуйте выбрать другую дату',
                                    parse_mode="html")
            mess2 = f'\n<b>{name} <u>{last_name}</u>\n\nНа какую дату Вы хотите записаться,' \
                    f' чтобы оформить {power_of_attorney} ??🗓️</b>'
            bot.send_message(message.chat.id, mess2, reply_markup=calendar.create_calendar(
                name=calendar_1.prefix,
                year=now_time.year,
                month=now_time.month), parse_mode="html")
        elif notarius == '':
            mess = f'\n<b>{name} <u>{last_name}</u>\n\nВы ввели что-то не так, попробуйте снова</b>'
            markup_exception = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Назад')
            markup_exception.add(button1)
            bot.send_message(message.chat.id, mess, reply_markup=markup_exception, parse_mode="html")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            for i in range(1, len(free_time)):
                button = types.KeyboardButton(free_time[i])
                markup.add(button)
            back = types.KeyboardButton('Назад')
            markup.add(back)
            mess = bot.send_message(message.from_user.id,
                                    text=f'<b>{name} <u>{last_name}</u>\n\n'
                                         f'Нотариус {C.notarius_name(notarius)}</b>\nработает {time_work}\n'
                                         f'\nвыберайте свободное время, на которое нужно Вас записать🕘',
                                    reply_markup=markup, parse_mode="html")
            bot.register_next_step_handler(mess, zapis, notarius, d, power_of_attorney)
    except Exception as e:
        print("Error>>> 397", e.args[0])
        if e.args[0] == "list index out of range":
            mess = f'\n<b>{name} <u>{last_name}</u>\n\nНа эту дату нет записи попробуйте ещё раз</b>'
            markup_exception = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Назад')
            markup_exception.add(button1)
            bot.send_message(message.chat.id, mess, reply_markup=markup_exception, parse_mode="html")
        else:
            mess = f'\n<b>{name} <u>{last_name}</u>\n\nПроизошла какая-то ошибка, попробуйте ещё раз</b>'
            markup_exception = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Назад')
            markup_exception.add(button1)
            bot.send_message(message.chat.id, mess, reply_markup=markup_exception, parse_mode="html")


def zapis(message, notarius, d, notarial_document):
    """
    метод для поиска времени записи к нотариусу
    :param notarial_document: документ, который выбрал клиент для оформления
    :param message: время
    :param notarius: нотариус
    :param d: дата для записи
    :return:
    переходим в файл exel -> zapis_not(time_records, notarius, d)
    """
    if message.chat.type == 'private':
        name = message.from_user.first_name
        if message.from_user.last_name is None:
            last_name = ""
        else:
            last_name = message.from_user.last_name
    if message.text == "start":
        start(message)
    if message.text != "start":
        if message.text == "08:00":
            time_records = message.text
        elif message.text == "09:00":
            time_records = message.text
        elif message.text == "10:00":
            time_records = message.text
        elif message.text == "11:00":
            time_records = message.text
        elif message.text == "12:00":
            time_records = message.text
        elif message.text == "13:00":
            time_records = message.text
        elif message.text == "14:00":
            time_records = message.text
        elif message.text == "15:00":
            time_records = message.text
        elif message.text == "16:00":
            time_records = message.text
        elif message.text == "17:00":
            time_records = message.text
        elif message.text == "18:00":
            time_records = message.text

        id_tel = message.chat.id
        tel = sql_.info_id(id_tel, db)
        print("+++++tel ", tel)
        bol = zapis_not(time_records, notarius, d, notarial_document, name, last_name, tel)
        if bol:
            mess = f'<b>{name} <u>{last_name}</u>\n\n✔Вы записаны к нотариусу {C.notarius_name(notarius)} \n{d} в {time_records}</b>' \
                   f'\n{C.documents(notarial_document)}'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

            back = types.KeyboardButton('Назад')

            markup.add(back)
            bot.send_message(message.from_user.id, mess, reply_markup=markup, parse_mode="html")
        else:
            bot_message(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: types.CallbackQuery):
    print("callback")
    power_of_attorney = call.message.text.split(" ")[9]
    print(">power_of_attorney>> ", power_of_attorney)
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year,
                                           month=month, day=day)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    button1 = types.KeyboardButton('🟡️ Гоголь Н.А.')
    button2 = types.KeyboardButton('🟡️ Сойка Е.Я.')
    button3 = types.KeyboardButton('🟡️ Демидова В.Г.')
    button4 = types.KeyboardButton('🟡️ Думанова И.Н.')
    button5 = types.KeyboardButton('🟡️ Ковалевская А.Г.')
    button6 = types.KeyboardButton('🟡️ Сильченко А.В.')
    button7 = types.KeyboardButton('🟡️ Бондаренко Ю.П.')
    button8 = types.KeyboardButton('🟡️ Чикан Н.М.')
    button9 = types.KeyboardButton('🟡️ Котикова О.В.')
    button10 = types.KeyboardButton('🟡️ Шинкевич Е.А.')
    button11 = types.KeyboardButton('🟡️ Позднякова С.Е.')
    back = types.KeyboardButton('Назад')

    markup.add(button1, button2, button3, button4, button5, button6,
               button7, button8, button9, button10, button11, back)

    if action == 'DAY':
        message_day = bot.send_message(chat_id=call.from_user.id, text=f'Вы выбрали <b>{date.strftime("%d.%m.%Y")}</b> '
                                                                       f'\n<u>УКАЖИТЕ</u> к какому нотариусу вы хотите '
                                                                       f'записаться?',
                                       reply_markup=markup, parse_mode="html")
        d = date.strftime("%d.%m.%Y")
        bot.register_next_step_handler(message_day, notarius_time, d, power_of_attorney)

    elif action == 'CANCEL':
        markup_all = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        markup_all.add(bf.button_info_delo, bf.button_website, bf.button_mail, bf.button_entry)
        bot.send_message(chat_id=call.from_user.id, text='Отмена', reply_markup=markup_all)

if __name__ == '__main__':
    threaded = threading.Thread(target=do_work, daemon=True).start()
    bot.polling(none_stop=True)
