import datetime as DT

now_time = DT.datetime.now()


def server_started(now_time):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'сервер запущен', file=botlogfile)
    botlogfile.close()


def log_start(message, now_time):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} пользователь {message.from_user.first_name} id-{message.from_user.id} '
        f'started bot {message.text}', file=botlogfile)
    botlogfile.close()


def log_Connect_sql():
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'соединение с базой SQL прошло успешно ', file=botlogfile)
    botlogfile.close()


def query_res(row):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(f'{now_time.strftime("%d-%m-%Y %H:%M")} в базе найдены совпадения по дате уведомления\n{row}',
          file=botlogfile)
    botlogfile.close()


def log_error(db_connection_error):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'произошла ошибка при поиске совпадений '
                                               'по дате уведомления таблицы SQL ' % db_connection_error,
          file=botlogfile)
    botlogfile.close()


def log_error_connection_mysql_db(db_connection_error):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    time_log = now_time.strftime("%d-%m-%Y %H:%M")
    text_log = 'произошла ошибка при создании таблицы '
    print(time_log, text_log, db_connection_error, file=botlogfile)
    botlogfile.close()


def log_help(message):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'перешёл в меню ->: ' + message.text, file=botlogfile)
    botlogfile.close()


def log_sticker(message, sticker_id):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'послал стикер боту: ' + sticker_id, file=botlogfile)
    botlogfile.close()


def log_res(message):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + message.from_user.first_name, message.from_user.id,
          'перешёл в меню ->: ' + message.text, file=botlogfile)
    botlogfile.close()


def replies_received(name, last_name):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'пользователь ' + name, last_name,
          'получил уведомление "на все запросы пришли ответы" ->: ', file=botlogfile)
    botlogfile.close()


def log_text_split(message, ms):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} пользователь {message.from_user.first_name} id-{message.from_user.id} '
        f'ввёл данные {ms}', file=botlogfile)
    botlogfile.close()


def person_in_db(message, l_name, tel):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} от пользователя {message.from_user.first_name} id-{message.from_user.id} из введённых данных сформированы l_name={l_name} и tel={tel}',
        file=botlogfile)
    botlogfile.close()


def log_error2(message, e):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} у пользователя {message.from_user.first_name} id-{message.from_user.id} '
        f'произошла ошибка парсинге, вернули None  {e}', file=botlogfile)
    botlogfile.close()


def log_error3(message, e):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(
        f'{now_time.strftime("%d-%m-%Y %H:%M")} у пользователя {message.from_user.first_name} id-{message.from_user.id} '
        f'произошла ошибка при добавлении id {e}', file=botlogfile)
    botlogfile.close()


def person_add_bd(now_time, user_id, first_name, last_name, date, date_sms):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"), 'в базу добавлен пользователь ' + user_id, first_name, last_name,
          file=botlogfile)
    botlogfile.close()


def log_name_none(message, now_time):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"),
          'у пользователя c id ' + {message.from_user.id} + 'имя не известно, поэтому занесено имя None',
          file=botlogfile)
    botlogfile.close()


def log_last_name_none(message, now_time):
    botlogfile = open('loggerBot.log', 'a', encoding='utf-8')
    print(now_time.strftime("%d-%m-%Y %H:%M"),
          'у пользователя c id ' + {message.from_user.id} + 'фамилия не известна, поэтому занесено имя None',
          file=botlogfile)
    botlogfile.close()
