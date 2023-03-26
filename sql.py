from datetime import datetime
from sqlite3 import Error
import logger as log

def create_connection_mysql_db(db):
    """метод создания БД и подключения к ней"""
    try:
        cursor = db.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS personNotary (id INT, telephone_number INT, "
                       "first_name VARCHAR(255), last_name VARCHAR(255), data_filing VARCHAR(255),"
                       "first_name_of_death VARCHAR(255), last_name_of_death VARCHAR(255), "
                       "data_of_death VARCHAR(255), data_sms VARCHAR(255), srok VARCHAR(255), "
                       "notarius VARCHAR(255), notification VARCHAR(255))")
        print("\nDatabase created successfully!!!")
    except Error as db_error:
        print("Error: %s" % db_error)
        log.log_error_connection_mysql_db("Error: %s" % db_error)

    db.commit()
    cursor.close()


# def create_id_2(message):
#     """в ms положит введённые данные, если они введены корректно, например ['Гертман', '1523']"""
#     try:
#         ms = message.text.split(" ")
#         print("ms", ms)
#         return ms
#     except Exception as e:
#         log.log_error2(message, e)
#         print("Error: " + str(e))
#         return 0
#     cursor.close()
# def create_id_3(message, ms, db):
#     """в res из ['Гертман', '1523'] возмет первый индекс и присвоит к фамилии, второй индекс к телефону
#     и в таблице найдёт совпадения и нужному человеку присвоит id"""
#
#     cursor = db.cursor()
#     res = []
#     try:
#         if ms[0].isdigit():
#             l_name = ms[1]
#             tel = int(ms[0])
#         else:
#             l_name = ms[0]
#             tel = int(ms[1])
#         print(l_name, tel)
#         log.person_in_db(message, l_name, tel)
#
#     except Exception as e:
#         log.log_error2(message, e)
#         print("Error: " + str(e))
#
#         return None
#
#     try:
#         sql = """select * from personNotary where last_name = ? """
#
#         cursor.execute(sql, (l_name,))
#         query_result = cursor.fetchall()
#         print(len(query_result))
#
#         for user in query_result:
#             print("user:", user)
#             t = user[1] % 10000
#             print("tel:", tel)
#             print("t:", t)
#             count = 0
#             if t == tel:
#                 count += 1
#                 id = int(message.chat.id)
#                 print("id", id)
#                 if count == 1:
#                     sql = f"""UPDATE personNotary SET id = {id} WHERE telephone_number = ?"""
#                     cursor.execute(sql, (user[1],))
#                     print("добавили id")
#                     db.commit()
#                     res.append(user[8])
#                     res.append(user[10])
#                     return res
#     except db.Error as error:
#         log.log_error3(message, error)
#         print("Failed to get record from MySQL table: {}".format(error))
#         return None
#     cursor.close()
def otm(id, db):
    """если в базе найден человек, которого необходимо уведомить,
    бот уведомляет и ставит отметку "уведомлены и дата" """

    print("7...")
    text = "уведомлен "
    data = str(datetime.now().strftime("%d.%m.%Y"))
    data_sms = text + data
    print("data_sms ", data_sms)

    """изменение значения ячейки"""

    cursor = db.cursor()
    try:

        sql_update_query = """Update personNotary set data_sms = ? where id = ?"""
        data = (data_sms, id)
        cursor.execute(sql_update_query, data)
        db.commit()
        print("Запись успешно обновлена")
        db.commit()
        cursor.close()

    except db.Error as error:

        print("Failed to get record from MySQL table: {}".format(error))

def info_srok(id, db):
    """
    ответ на запрос пользователя о предоставлении онформации по делу
    по ID находим в базе человека, берём значение "нотариус"
    """
    cursor = db.cursor()
    try:
        sql_update_query = """SELECT srok FROM personNotary WHERE id = ? """
        cursor.execute(sql_update_query, (id,))
        # cursor.execute(sql_update_query, id)
        query_result = cursor.fetchall()
        for srok in query_result:
            print("info ", srok)
            return srok[0]
    except db.Error as error:
        log.error_info(id, db.Error)
        print("Failed to get record from MySQL table: {}".format(error))

def info_notarius(id, db):
    """ответ на запрос пользователя о предоставлении онформации по делу """
    cursor = db.cursor()
    try:
        sql_update_query = """SELECT notarius FROM personNotary WHERE id = ? """
        cursor.execute(sql_update_query, (id,))
        query_result = cursor.fetchall()
        for notarius in query_result:
            if (len(query_result)) == 1:
                return notarius[0]
    except db.Error as error:
        log.error_info(id, db.Error)
        print("Failed to get record from MySQL table: {}".format(error))

def info_zapros(id, db):
    """
    ответ на запрос пользователя о предоставлении онформации по делу
    по ID находим в базе человека
    если ячейка пустая (ответы не пришли на запросы) - возвращаем None
    если ячейка с отметкой, что человек уже уведомлен, берём это значение для отправки
    """
    cursor = db.cursor()
    try:
        sql_update_query = """SELECT notification FROM personNotary WHERE id = ? """
        cursor.execute(sql_update_query, (id,))
        query_result = cursor.fetchall()
        if query_result:
            if (len(query_result)) == 1:
                for notification in query_result:
                    if notification == ("", ):
                        print("None")
                        return None
                    else:
                        print("notification", notification)
                        notification = notification[0]
                        return notification

    except db.Error as error:

        log.error_info(id, db.Error)
        print("Failed to get record from MySQL table: {}".format(error))

def create_reg(telephon, id_tel, db):
    cursor = db.cursor()
    result = []
    try:
        sql = """select * from personNotary where telephone_number = ? """

        cursor.execute(sql, (telephon,))
        query_result = cursor.fetchall()
        print(len(query_result))

        if len(query_result) == 0:
            return False
        else:

            for user in query_result:
                sql = f"""UPDATE personNotary SET id = {id_tel} WHERE telephone_number = ?"""
                cursor.execute(sql, (telephon,))
                print(user)
                result.append(user[2])
                result.append(user[3])
                result.append(user[9])
                result.append(user[10])
                print(result)
                print("добавили id")

                db.commit()


            return result
    except db.Error as error:
        # log.log_error3(error)
        print("Failed to get record from MySQL table: {}".format(error))
        return None
    cursor.close()

def create_new_person(id, tel, name, l_name, db):
    """
    метод регистрации человека, добавившегося в бота не по наследственному делу
    :param id: идентификационный номер человека
    :param tel: номер телефона
    :param name: имя
    :param l_name: фамилия
    :param db: даза данных
    :return:
    """
    cursor = db.cursor()
    try:
        sql = """INSERT INTO personNotary (id, telephone_number, first_name, last_name) VALUES (?, ?, ?, ?) """
        cursor.execute(sql, (id, tel, name, l_name))
        query_result = cursor.fetchall()
        db.commit()

    except db.Error as error:
        # log.log_error3(error)
        print("Failed to get record from MySQL table: {}".format(error))

    cursor.close()
