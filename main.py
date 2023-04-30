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
import sql
import notification as n
from _locale import Error
from myTime import then
from myTime import then3
from exel import x_file
from exel import save_file
import search_notar_doc as C
import text_messages_bot_photo
import button_file
import exel as ex
import url

bot = telebot.TeleBot(token=config.TOKEN, threaded=True)
now_time = DT.datetime.now()

sql_ = sql.Sql_Class()
bf = button_file.Button()
tm_info_delo = text_messages_bot_photo.Info_Delo()
tm_info_zapis = text_messages_bot_photo.Info_Zapis()
tm_info_notification = text_messages_bot_photo.Info_Notification()
tm_start = text_messages_bot_photo.Start()
tm_help = text_messages_bot_photo.Help()
tm_cancel_recording = text_messages_bot_photo.Info_Zapis()
url = url.URL()

print('server started')
log.server_started(now_time)

db = dbcon()
sql_.create_connection_mysql_db(db)
log.log_Connect_sql()

calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')


def do_work():
    """метод ожидания нужного времени и даты для уведомления второй поток"""
    print("processing requests starting")
    while True:
        """уведомление, когда пришли ответы на все запросы по НД"""
        print("while True requests...")
        if DT.datetime.now().strftime("%H:%M") == then3:
            res = n.notif(db)
            try:
                if res is not None:
                    for i in res:
                        if i[3] is None:  # если графа с фамилией пуста, фамилию не пишем
                            params = {
                                'chat_id': i[0],
                                'text': f'{i[2]} {tm_info_notification.text_otvet}{tm_info_notification.text_zapis} {i[10]} в срок до {i[9]}',
                            }
                        else:
                            params = {
                                'chat_id': i[0],
                                'text': f'{i[2]} {i[3]} {tm_info_notification.text_otvet}{tm_info_notification.text_zapis} {i[10]} в срок до {i[9]}',
                            }
                        response = requests.get('https://api.telegram.org/bot' + config.TOKEN + '/sendMessage',
                                                params=params)
                        log.replies_received(i[2], i[0])
            except Error as e:
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
                            'text': f'{row[2]} {row[3]}\n\n{tm_info_notification.text_zapis} {row[10]} в срок до {row[9]}',
                        }
                        response = requests.get('https://api.telegram.org/bot' + config.TOKEN + '/sendMessage',
                                                params=params)
                        sql_.otm(row[0], db)
                    time.sleep(65)
                else:
                    time.sleep(30)
            except Error as e:
                log.log_error(e)
        else:
            time.sleep(30)
            print(DT.datetime.now().strftime("%H:%M"))


print("processing bot started...")

@bot.message_handler(commands=['start'])
def start(message):
    """при переходе в меню /start пользователь подтверждает свой телефон для его
    идентификации в таблице."""
    log.log_start(message, now_time)

    photo = tm_start.photo()
    name = message.from_user.first_name
    if message.from_user.last_name is None:
        last_name = ""
    else:
        last_name = message.from_user.last_name

    mess = f'<b>Здравствуйте, {name} {last_name}</b>' + tm_start.text_start()

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

        markup.add(bf.button_website, bf.button_mail, bf.button_info_delo, bf.button_entry, bf.button_info_zapisi,
                   bf.back, bf.button_cancel_recording)
        if message.from_user.first_name is not None:
            name = message.from_user.first_name
        else:
            name = ""
        if message.from_user.last_name is not None:
            last_name = message.from_user.last_name
        else:
            last_name = ""
        mess = f'{name} {last_name}' + tm_start.message_reg_ok()
        bot.send_message(message.chat.id, mess + '\U0001f600', reply_markup=markup, parse_mode="html")
    else:
        if res[3] is None:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            markup.add(bf.button_website, bf.button_mail, bf.button_info_delo, bf.button_entry, bf.button_info_zapisi,
                       bf.backbf.button_website, bf.button_mail, bf.button_info_delo,
                       bf.button_entry, bf.button_info_zapisi, bf.back, bf.button_cancel_recording)
            mess = f'<b>{res[0]} {res[1]}</b>' + tm_start.reg_ok() + tm_start.reg_ok2()
            bot.send_message(message.chat.id, mess + '\U0001f600', reply_markup=markup, parse_mode="html")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            markup.add(bf.button_website, bf.button_mail, bf.button_info_delo,
                       bf.button_entry, bf.button_info_zapisi, bf.back, bf.button_cancel_recording)

            mess = f'{res[0]} {res[1]} \n{tm_start.message_reg_ok()}' \
                   f'\nВаш нотариус <u><b>{res[3]}</b></u>\n' \
                   f'Ожидайте уведомление до <u><b>{res[2]}</b></u>\n{tm_start.reg_ok2()}'
            bot.send_message(message.chat.id, mess + '\U0001f600', reply_markup=markup, parse_mode="html")


@bot.message_handler(commands=['help'])
def help_command(message):
    log.log_help(message)
    l_name = message.from_user.last_name
    if l_name is None:
        l_name = " "
    mess = f'<b>{message.from_user.first_name} <u>{l_name}</u></b>\n {tm_help.text_help}'
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
    try:
        if message.chat.type == 'private':
            name = message.from_user.first_name
            if message.from_user.last_name is None:
                last_name = ""
            else:
                last_name = message.from_user.last_name

            if message.text == 'Найти сведения о моей записи':
                telephone = sql_.info_telephone(message.from_user.id, db)
                spisok = ex.search(telephone)
                if len(spisok) == 0:
                    mess = f'<b>Записи не найдены!!.</b> \n {tm_info_zapis.tel()}'
                    bot.send_message(message.chat.id, mess, parse_mode="html")
                else:
                    for i in spisok:
                        action = i[0]
                        notarius = i[1]
                        time_zapis = i[2]
                        data_zapis = i[3]
                        mess = f'Вот что я нашёл, посмотрите. \n' \
                               f'Вы записаны на <b>{action}</b> к нотариусу <u>{notarius} в {time_zapis} {data_zapis}</u>' \
                               + tm_info_zapis.tel()
                        bot.send_message(message.chat.id, mess, parse_mode="html")

            elif message.text == 'Информация о моём деле':
                log.log_res(message)
                sign_up_for_a_month = sql_.info_srok(message.from_user.id, db)
                notarius = sql_.info_notarius(message.from_user.id, db)
                zapros = sql_.info_zapros(message.from_user.id, db)
                if notarius is None:
                    mess = tm_info_delo.text_not_delo
                    bot.send_message(message.chat.id, mess)

                elif zapros is None:
                    zapros = tm_info_delo.text_not_zapros
                    mess = f'<b>{name} <u>{last_name}</u></b>\n\nв срок до <b>{sign_up_for_a_month}</b>' \
                           f'{tm_info_delo.text_zapis_not} <b>{notarius}</b>' \
                           f'\n{zapros}💁'
                    bot.send_message(message.chat.id, mess, parse_mode="html")
                    bot.send_message(message.from_user.id,
                                     tm_info_delo.text_zapis_not2 + '\u261E' + '[НАЖМИ ТУТ](https://enotary.by/#/legacy/)',
                                     parse_mode='Markdown')
                else:
                    zapros = f'<b>Ответы на запросы получены, \nоб этом Вы были уведомлены</b> --> {zapros.split(" ")[1]}'
                    mess = f'<b>{name} <u>{last_name}</u></b>\n\nв срок до <b>{sign_up_for_a_month}</b>' \
                           f'{tm_info_delo.text_zapis_not} <b>{notarius}</b>' \
                           f'\n{zapros}💁'
                    bot.send_message(message.chat.id, mess, parse_mode="html")
                    bot.send_message(message.from_user.id,
                                     tm_info_delo.text_zapis_not2 + '\u261E' + '[НАЖМИ ТУТ](https://enotary.by/#/legacy/)',
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
                       f'Выберите в какую контору Вы хотите написать письмо или позвонить?'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

                markup.add(bf.button_office_Minsk_obl, bf.button_office_Minsk_gor, bf.button_office_Vitebsk,
                           bf.button_office_Gomel,
                           bf.button_office_Grodno, bf.button_office_Brest, bf.button_office_Mogilev, bf.back)
                bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode="html")

            elif message.text == "Назад":
                log.log_res(message)
                # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                #
                # markup.add(bf.button_website, bf.button_mail, bf.button_info_delo,
                #            bf.button_entry, bf.button_info_zapisi, bf.back, bf.button_cancel_recording)
                bot.send_message(message.chat.id, "Выберите что Вам необходимо", reply_markup=start_button())

            elif message.text == "Минский городской нотариальный округ":
                bot.send_message(message.chat.id, 'в разработке')
            elif message.text == "Минский областной нотариальный округ":
                bot.send_message(message.chat.id, 'в разработке')
            elif message.text == "Брестский нотариальный округ":
                bot.send_message(message.chat.id, 'в разработке')
            elif message.text == "Гомельский нотариальный округ":
                bot.send_message(message.chat.id, 'в разработке')
            elif message.text == "Гродненский нотариальный округ":
                bot.send_message(message.chat.id, 'в разработке')
            elif message.text == "Могилёвский нотариальный округ":
                bot.send_message(message.chat.id, 'в разработке')

            elif message.text == "Витебский нотариальный округ":
                log.log_res(message)
                mess = f'<b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>\n' \
                       f'Выберите в какую нотариальную контору' \
                       f'\nВы хотите написать письмо'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                markup.add(bf.button_office_Orsha, bf.button_office_Baran, bf.back)
                bot.send_message(message.chat.id, mess, reply_markup=markup, parse_mode="html")

            elif message.text == "Нотариальная контора Оршанского района и г.Орши":
                log.log_res(message)
                markup = types.InlineKeyboardMarkup(row_width=2)
                button1 = InlineKeyboardButton("Написать письмо",
                                               url=url.url_notariat_orsha)
                button2 = InlineKeyboardButton("Перейти на сайт и Позвонить",
                                               url=url.url_belnotary)
                markup.add(button1, button2)

                bot.send_message(message.chat.id, "написать письмо или позвонить?", reply_markup=markup)

            elif message.text == "Нотариальная контора г.Барани Оршанского района":
                log.log_res(message)
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Написать письмо",
                                                      url=url.url_notariat_baran))

                bot.send_message(message.chat.id, "написать письмо?", reply_markup=markup)
            elif message.text == 'Записаться на приём к нотариусу':
                log.log_zapis_bot(message)
                mess = f'<b>{name} <u>{last_name}</u>\n\nчто Вы хотите оформить у нотариуса?</b>📄'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

                markup.add(bf.button_power_of_attorney, bf.button_will, bf.button_agreement, bf.button_statement,
                           bf.button_consultation, bf.button_other_action, bf.back)

                bot.send_message(message.from_user.id, mess, reply_markup=markup, parse_mode="html")
            elif message.text == '✔️Отмена записи':

                telephone = sql_.info_telephone(message.from_user.id, db)
                spisok = ex.search(telephone)
                if len(spisok) == 0:
                    mess = f'<b>Записи не найдены!!.</b> \n {tm_info_zapis.tel()}'
                    bot.send_message(message.chat.id, mess, parse_mode="html")
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    print(spisok, "spisok")
                    print(len(spisok), "len(spisok)")

                    for i in range(0, len(spisok)):
                        res = f'нотариус {spisok[i][1]} - {spisok[i][0]} время {spisok[i][2]} дата {spisok[i][3]}'
                        print(res, "res")

                        button = types.KeyboardButton(res)
                        markup.add(button)
                    back = types.KeyboardButton('Назад')
                    markup.add(back)

                    mess = bot.send_message(message.from_user.id,
                                            text=f'<b>{name} <u>{last_name}</u></b>\n\nЧто удалять?',
                                            reply_markup=markup, parse_mode="html")
                    bot.register_next_step_handler(mess, delete_file)

            elif message.text == '✔️Доверенность':
                log.log_res(message)
                power_of_attorney = "Доверенность"
                mess = f'<b>{name} <u>{last_name}</u>\n\n{tm_info_zapis.data_zapis()} {power_of_attorney} ??🗓️</b>'

                bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                    name=calendar_1.prefix,
                    year=now_time.year,
                    month=now_time.month), parse_mode="html")
            elif message.text == '✔️Завещание':
                log.log_res(message)
                power_of_attorney = "Завещание"
                mess = f'<b>{name} <u>{last_name}</u>\n\n{tm_info_zapis.data_zapis()} {power_of_attorney} ??🗓️</b>'
                bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                    name=calendar_1.prefix,
                    year=now_time.year,
                    month=now_time.month), parse_mode="html")
            elif message.text == '✔️Согласие':
                log.log_res(message)
                power_of_attorney = "Согласие"

                mess = f'<b>{name} <u>{last_name}</u>\n\n{tm_info_zapis.data_zapis()} {power_of_attorney} ??🗓️</b>'
                bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                    name=calendar_1.prefix,
                    year=now_time.year,
                    month=now_time.month), parse_mode="html")
            elif message.text == '✔️Заявление':
                log.log_res(message)
                power_of_attorney = "Заявление"
                mess = f'<b>{name} <u>{last_name}</u>\n\n{tm_info_zapis.data_zapis()} {power_of_attorney} ??🗓️</b>'

                bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                    name=calendar_1.prefix,
                    year=now_time.year,
                    month=now_time.month), parse_mode="html")
            elif message.text == '✔️Консультация':
                log.log_res(message)
                power_of_attorney = "Консультация"
                mess = f'<b>{name} <u>{last_name}</u>\n\n{tm_info_zapis.data_zapis()} {power_of_attorney} ??🗓️</b>'

                bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                    name=calendar_1.prefix,
                    year=now_time.year,
                    month=now_time.month), parse_mode="html")
            elif message.text == '✔️иное действие':
                log.log_res(message)
                mess = f'<u>{name} {last_name}</u>\n\nДля оформление болеее сложного действия ' \
                       f'Вам необходимо записаться на консультацию для получения необходимого ' \
                       f'Вам перечня документов либо уточнить информацию по телефону 📞 +375 216 56-88-94'
                # markup_all = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                #
                # markup_all.add(bf.button_info_delo, bf.button_website, bf.button_mail, bf.button_entry,
                #                bf.button_info_zapisi, bf.back)
                bot.send_message(message.chat.id, mess, reply_markup=start_button(), parse_mode="html")
            else:
                log.log_res(message)
                mess = f'{message.text}\n\n<b>{name} <u>{last_name}</u></b>' \
                       f'\n\nЯ Вас не понимаю!! '
                # markup_all = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
                #
                # markup_all.add(bf.button_info_delo, bf.button_website, bf.button_mail, bf.button_entry,
                #                bf.button_info_zapisi, bf.back)
                bot.send_message(message.chat.id, mess + '\U0001F534', reply_markup=start_button(), parse_mode="html")
                # bot.send_message(message.chat.id, mess + '\U0001F534', parse_mode="html")

    except Exception as e:
        log.log_bot(message, e)
def delete_file(message):
    print("mess", message.text)
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, 'Удаляем......', reply_markup=a)
    if message.text == "Назад":
        bot_message(message)
    else:
        try:
            del_ok = ex.delete_file(message.text)
            if del_ok is True:
                bot.send_message(message.from_user.id, f'Запись успешно удалена?', reply_markup=start_button())
        except Exception as e:
            log.log_bot(message, e)

def start_button():
    markup_all = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

    markup_all.add(bf.button_info_delo, bf.button_website, bf.button_mail, bf.button_entry,
                   bf.button_info_zapisi, bf.back, bf.button_cancel_recording)
    return markup_all

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
    if message.chat.type == 'private':
        log.log_res(message)
        name = message.from_user.first_name
        if message.from_user.last_name is None:
            last_name = ""
        else:
            last_name = message.from_user.last_name
    try:
        if message.text == "Назад":
            bot_message(message)

        elif message.text == "🟡️ Гоголь Н.А." or message.text == "🟡️ Сойка Е.Я." \
                or message.text == "🟡️ Думанова И.Н." or message.text == '🟡️ Ковалевская А.Г.' \
                or message.text == "🟡️ Сильченко А.В." or message.text == "🟡️ Бондаренко Ю.П." \
                or message.text == "🟡️ Чикан Н.М." or message.text == "🟡️ Котикова О.В." \
                or message.text == "🟡️ Шинкевич Е.А." or message.text == "🟡️ Позднякова С.Е." \
                or message.text == "🟡️ Демидова В.Г.":
            notarius = message.text.split(" ")[1]
            free_time = x_file(d, notarius)
            print("free_time main ", free_time)
            if free_time is None:
                mess = f'‼ На эту дату нет записи попробуйте ещё раз ‼\n' \
                       f'\n{d}  \nпопробуйте выбрать другую дату чтобы оформить {power_of_attorney} ??🗓️'
                bot.send_message(message.chat.id, mess, reply_markup=calendar.create_calendar(
                    name=calendar_1.prefix,
                    year=now_time.year,
                    month=now_time.month), parse_mode="html")
                log.log_timeout(message)
            elif free_time[0] == "воскресенье":
                log.log_day_off(message)
                mess2 = f'\n{name} {last_name}\n\n{d} <b>{tm_info_zapis.sunday()}</b>'
                bot.send_message(message.chat.id, mess2, reply_markup=start_button(), parse_mode="html")
            elif free_time[0] == "выходной":
                log.log_day_off(message)
                mess2 = f'\n{name} {last_name}\n\n' \
                        f'Нотариус <b>{C.notarius_name(notarius)}</b>  {d} <b>{tm_info_zapis.day_off()}</b>'
                bot.send_message(message.chat.id, mess2, reply_markup=start_button(), parse_mode="html")
            elif len(free_time) == 1:
                log.log_busy(message)
                mess = bot.send_message(message.from_user.id,
                                        text=f'<b>{name} <u>{last_name}</u>\n\n️'
                                             f'У нотариуса {C.notarius_name(notarius)}</b>\n'
                                             f'{d} ‼ нет свободного времени для записи ‼\n️'
                                             f'\nпопробуйте выбрать другую дату',
                                        parse_mode="html")
                mess2 = f'\n<b>{name} <u>{last_name}</u>\n\nНа какую дату Вы хотите записаться,' \
                        f' чтобы оформить {power_of_attorney} ??🗓️</b>'
                bot.send_message(message.chat.id, mess2, reply_markup=calendar.create_calendar(
                    name=calendar_1.prefix,
                    year=now_time.year,
                    month=now_time.month), parse_mode="html")
            elif notarius == '':
                log.log_notarius_time(message)
                mess = f'\n<b>{name} <u>{last_name}</u>\n\nВы ввели что-то не так, попробуйте снова</b>'
                markup_exception = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton('Назад')
                markup_exception.add(button1)
                bot.send_message(message.chat.id, mess, reply_markup=markup_exception, parse_mode="html")

            elif free_time is not None:
                time_work = free_time[0]

                if time_work == "выходной":
                    log.log_day_off(message)
                    mess2 = f'\n<b>{name} <u>{last_name}</u>\n\n' \
                            f'Нотариус {C.notarius_name(notarius)}</b>\n' \
                            f'{d} ‼ НЕ РАБОТАЕТ ‼\n' \
                            f'\nпопробуйте выбрать другую дату чтобы оформить {power_of_attorney} ??🗓️</b>'
                    bot.send_message(message.chat.id, mess2, reply_markup=calendar.create_calendar(
                        name=calendar_1.prefix,
                        year=now_time.year,
                        month=now_time.month), parse_mode="html")

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
        log.log_eception_notarius_time(message, e)
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
    try:
        log.log_zapis(message)
        if message.chat.type == 'private':
            name = message.from_user.first_name
            if message.from_user.last_name is None:
                last_name = ""
            else:
                last_name = message.from_user.last_name
        if message.text == "start":
            start(message)
        elif message.text == "Назад":
            bot_message(message)
        elif message.text != "start":
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
            bol = save_file(time_records, notarius, d, notarial_document, name, last_name, tel)
            print(bol)
            if bol:
                mess = f'<b>{name} <u>{last_name}</u>\n\n✔Вы записаны к нотариусу {C.notarius_name(notarius)} \n{d} в {time_records}</b>' \
                       f'\n{C.documents(notarial_document)}'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                back = types.KeyboardButton('Назад')
                markup.add(back)
                bot.send_message(message.from_user.id, mess, reply_markup=markup, parse_mode="html")
            else:
                bot_message(message)
    except Exception as e:
        log.log_zapis(message, e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: types.CallbackQuery):
    """
    сюда приходит выбранная пользователем дата для записи
    :param call: сообщение пользователя
    :return:
    """
    try:
        power_of_attorney = call.message.text.split(" ")[9]

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
            d = date.strftime("%d.%m.%Y")

            if d.split(".")[2] > DT.datetime.now().strftime("%d.%m.%Y").split(".")[2]:
                message_day = bot.send_message(chat_id=call.from_user.id,
                                               text=f'Вы выбрали <b>{date.strftime("%d.%m.%Y")}</b> '
                                                    f'\n<u>УКАЖИТЕ</u> к какому нотариусу вы хотите '
                                                    f'записаться?',
                                               reply_markup=markup, parse_mode="html")
                bot.register_next_step_handler(message_day, notarius_time, d, power_of_attorney)

            elif d.split(".")[2] == DT.datetime.now().strftime("%d.%m.%Y").split(".")[2] and \
                    d.split(".")[1] > DT.datetime.now().strftime("%d.%m.%Y").split(".")[1]:
                message_day = bot.send_message(chat_id=call.from_user.id,
                                               text=f'Вы выбрали <b>{date.strftime("%d.%m.%Y")}</b> '
                                                    f'\n<u>УКАЖИТЕ</u> к какому нотариусу вы хотите '
                                                    f'записаться?',
                                               reply_markup=markup, parse_mode="html")
                bot.register_next_step_handler(message_day, notarius_time, d, power_of_attorney)

            elif d.split(".")[2] == DT.datetime.now().strftime("%d.%m.%Y").split(".")[2] and \
                    d.split(".")[1] == DT.datetime.now().strftime("%d.%m.%Y").split(".")[1] and \
                    d.split(".")[0] >= DT.datetime.now().strftime("%d.%m.%Y").split(".")[0]:
                message_day = bot.send_message(chat_id=call.from_user.id,
                                               text=f'Вы выбрали <b>{date.strftime("%d.%m.%Y")}</b> '
                                                    f'\n<u>УКАЖИТЕ</u> к какому нотариусу вы хотите '
                                                    f'записаться?',
                                               reply_markup=markup, parse_mode="html")
                bot.register_next_step_handler(message_day, notarius_time, d, power_of_attorney)
            else:

                bot.send_message(chat_id=call.from_user.id, text=f'<b>Вы выбрали прошедшую дату</b>\n\n'
                                                                 f'‼ <u>{tm_start.again()}</u> ‼ ',
                                 reply_markup=start_button(), parse_mode="html")

        elif action == 'CANCEL':
            # markup_all = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
            # markup_all.add(bf.button_info_delo, bf.button_website, bf.button_mail, bf.button_entry,
            #                bf.button_info_zapisi, bf.back)
            bot.send_message(chat_id=call.from_user.id, text='Отмена', reply_markup=start_button())
    except Exception as e:
        log.log_error_callback_inline(call.message.text, e)


if __name__ == '__main__':
    threaded = threading.Thread(target=do_work, daemon=True).start()
    bot.polling(none_stop=True)
