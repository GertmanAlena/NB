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

    db.commit()
    cursor.close()


def create_id_2(message):
    """в ms положит введённые данные, если они введены корректно, например ['Гертман', '1523']"""
    try:

        ms = message.text.split(" ")
        print("ms", ms)
        return ms
    except Exception as e:
        log.log_error2(message, e)
        print("Error: " + str(e))
        return 0
    cursor.close()
def create_id_3(message, ms, db):
    """в res из ['Гертман', '1523'] возмет первый индекс и присвоит к фамилии, второй индекс к телефону
    и в таблице найдёт совпадения и нужному человеку присвоит id"""

    cursor = db.cursor()
    res = []
    try:
        if ms[0].isdigit():
            l_name = ms[1]
            tel = int(ms[0])
        else:
            l_name = ms[0]
            tel = int(ms[1])
        print(l_name, tel)
        log.person_in_db(message, l_name, tel)

    except Exception as e:
        log.log_error2(message, e)
        print("Error: " + str(e))

        return None

    try:
        sql = """select * from personNotary where last_name = ? """

        cursor.execute(sql, (l_name,))
        query_result = cursor.fetchall()
        print(len(query_result))

        for user in query_result:
            print("user:", user)
            t = user[1] % 10000
            print("tel:", tel)
            print("t:", t)
            count = 0
            if t == tel:
                count += 1
                id = int(message.chat.id)
                print("id", id)
                if count == 1:
                    sql = f"""UPDATE personNotary SET id = {id} WHERE telephone_number = ?"""
                    cursor.execute(sql, (user[1],))
                    print("добавили id")
                    db.commit()
                    res.append(user[8])
                    res.append(user[10])
                    return res
    except db.Error as error:
        log.log_error3(message, error)
        print("Failed to get record from MySQL table: {}".format(error))
        return None
    cursor.close()
def otm(id, db):
    """если в базе найден человек, которого необходимо уведомить,
    бот уведомляет и ставит отметку "уведомлен и дата" """

    print("7...")
    text = "уведомлен "
    data = str(datetime.now().strftime("%d.%m.%Y"))
    data_sms = text + data
    print("data_sms ", data_sms)
    """метод изменения ячейки"""

    cursor = db.cursor()

    try:

        sql_update_query = """Update personNotary set data_sms = ? where id = ?"""
        data = (data_sms, id)
        cursor.execute(sql_update_query, data)
        db.commit()
        print("Запись успешно обновлена")
        db.commit()
        cursor.close()

        # sql = f"""UPDATE personNotary SET data_sms = {data_sms} WHERE id = ?"""
        #
        # cursor.execute(sql, (id,))
        # print("изменили ...")
    except db.Error as error:

        print("Failed to get record from MySQL table: {}".format(error))

def info(id, db):
    """ответ на запрос пользователя о предоставлении онформации по делу """

    cursor = db.cursor()

    try:

        sql_update_query = """SELECT srok FROM personNotary WHERE id = ? """
        cursor.execute(sql_update_query, id)
        query_result = cursor.fetchall()


        for user in query_result:
            print(user)

    except db.Error as error:

        print("Failed to get record from MySQL table: {}".format(error))