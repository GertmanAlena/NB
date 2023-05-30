import datetime as DT

filename = 'loggerBot.log'
now_time = DT.datetime.now()
def server_started():
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'сервер запущен', file=botlogfile)
    botlogfile.close()
def log_start(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} пользователь {message.from_user.first_name} id-{message.from_user.id} '
        f'started bot {message.text}', file=botlogfile)
    botlogfile.close()
def log_Connect_sql():
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'соединение с базой SQL прошло успешно ', file=botlogfile)
    botlogfile.close()
def query_res(row):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(f'{now_time.strftime("%d-%m-%Y %H:%M")} в базе найдены совпадения по дате уведомления\n{row}',
          file=botlogfile)
    botlogfile.close()
def log_error(db_connection_error):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'произошла ошибка при поиске совпадений '
                                               'по дате уведомления таблицы SQL ' % db_connection_error,
          file=botlogfile)
    botlogfile.close()
def log_error_connection_mysql_db(db_connection_error):
    botlogfile = open(filename, 'a', encoding='utf-8')
    time_log = now_time.strftime("%d-%m-%Y %H:%M")
    text_log = 'произошла ошибка при создании таблицы '
    print(time_log, text_log, db_connection_error, file=botlogfile)
    botlogfile.close()
def log_help(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'перешёл в меню ->: ' + message.text, file=botlogfile)
    botlogfile.close()


def log_sticker(message, sticker_id):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'послал стикер боту: ' + sticker_id, file=botlogfile)
    botlogfile.close()
def log_res(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'перешёл в меню ->: ' + message.text, file=botlogfile)
    botlogfile.close()
def replies_received(name, id):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + name, id,
          'получил уведомление "на все запросы пришли ответы" ->: ', file=botlogfile)
    botlogfile.close()
def log_text_split(message, ms):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} пользователь {message.from_user.first_name} id-{message.from_user.id} '
        f'ввёл данные {ms}', file=botlogfile)
    botlogfile.close()
def person_in_db(message, l_name, tel):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} от пользователя {message.from_user.first_name} id-{message.from_user.id} из введённых данных сформированы l_name={l_name} и tel={tel}',
        file=botlogfile)
    botlogfile.close()
def log_error2(message, e):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} у пользователя {message.from_user.first_name} id-{message.from_user.id} '
        f'произошла ошибка парсинге, вернули None  {e}', file=botlogfile)
    botlogfile.close()
def log_error3(message, e):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} у пользователя {message.from_user.first_name} id-{message.from_user.id} '
        f'произошла ошибка при добавлении id {e}', file=botlogfile)
    botlogfile.close()
def log_error4(message, telephon, id_tel):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} у пользователя {id_tel} телефон-{telephon} '
        f'произошла ошибка при поиске по номеру телефона человека в методе create_reg', file=botlogfile)
    botlogfile.close()

def log_error5(message, id, tel, name, l_name):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} у пользователя {name} {l_name} телефон-{tel} id {id} '
        f'произошла ошибка при регистрации', file=botlogfile)
    botlogfile.close()
def error_info(id, e):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} у пользователя c id-{id} '
        f'произошла ошибка {e}', file=botlogfile)
    botlogfile.close()
def person_add_bd(now_time, user_id, first_name, last_name, date, date_sms):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'в базу добавлен пользователь ' + user_id, first_name, last_name,
          file=botlogfile)
    botlogfile.close()
def log_name_none(message, now_time):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"),
          'у пользователя c id ' + {message.from_user.id} + 'имя не известно, поэтому занесено имя None',
          file=botlogfile)
    botlogfile.close()
def log_last_name_none(message, now_time):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"),
          'у пользователя c id ' + {message.from_user.id} + 'фамилия не известна, поэтому занесено имя None',
          file=botlogfile)
    botlogfile.close()
def activ_list(e, notarius, day):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(f'произошла ошибка при активации листа {notarius} {day} {e}', file=botlogfile)
    botlogfile.close()
def log_zapis_not(e, notarius):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(f'произошла ошибка в zapis_not {e} {notarius} ', file=botlogfile)
    botlogfile.close()

def log_zapis_bot(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} пользователь {message.from_user.first_name} id-{message.from_user.id} '
        f'перешёл в меню <{message.text}>', file=botlogfile)
    botlogfile.close()

def log_bot(message, e):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} пользователь {message.from_user.first_name} id-{message.from_user.id} '
        f'перешёл в меню <{message.text}> ошибка {e}', file=botlogfile)
    botlogfile.close()
def log_do_not_understand(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'Ввёл что-то не понятное: ' + message.text, file=botlogfile)
    botlogfile.close()

def log_timeout(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'Выбрал время, когда рабочий день окончен: ' + message.text, file=botlogfile)
    botlogfile.close()
def log_day_off(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'выбрал день, когда нотариус выходной: ' + message.text, file=botlogfile)
    botlogfile.close()
def log_busy(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'выбрал день, когда у нотариуса всё расписано: ' + message.text, file=botlogfile)
    botlogfile.close()
def log_notarius_time(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'Ввел что-то не так: ' + message.text, file=botlogfile)
    botlogfile.close()
def log_eception_notarius_time(message, e):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'Ввел что-то не так: ' + message.text, file=botlogfile)
    botlogfile.close()

def log_zapis(message):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} пользователь {message.from_user.first_name} id-{message.from_user.id} '
        f'перешёл в меню <{message.text}> ', file=botlogfile)
    botlogfile.close()

def log_error_zapis(message, e):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), f'{message} \nпроизошла ошибка при выборе даты записи \n{e}',
          file=botlogfile)
    botlogfile.close()

def log_error_callback_inline(message, e):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), f'{message} \nпроизошла ошибка в календаре \n{e}',
          file=botlogfile)
    botlogfile.close()
def save_file_except(e, text):

    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), f'произошла ошибка в {text}  \n{e}',
          file=botlogfile)
    botlogfile.close()
def save_file(time, notarius, day, power_of_attorney, name, last_name, tel):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), f' пользователь {name} {last_name} {tel} записался '
                                               f'к нотариусу {notarius} {day} {time} для оформления {power_of_attorney} \n',
          file=botlogfile)
    botlogfile.close()

def log_otmetka_uvedomlen(id):
    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), f' пользователь c {id} уведомлен о поступлениизапросов \n',
          file=botlogfile)
    botlogfile.close()

def log_otmetka_uvedomlen_except(text):

    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), f' ошибка в методе otmetka_uvedomlen {text}', file=botlogfile)
    botlogfile.close()
def no_identification(text):

    botlogfile = open(filename, 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), text, file=botlogfile)
    botlogfile.close()