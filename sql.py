from datetime import datetime
from sqlite3 import Error
import logger as log

class Sql_Class():

    def create_connection_mysql_db(self, db):
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
    def otmetka_uvedomlen(self, id, db):
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
            log.log_otmetka_uvedomlen(id)
        except db.Error as error:
            log.log_otmetka_uvedomlen_except("Failed to get record from MySQL table: {}".format(error))
            print("Failed to get record from MySQL table: {}".format(error))

    def info_srok(self, id, db):
        """
        ответ на запрос пользователя о предоставлении онформации по делу
        по ID находим в базе человека, берём значение "нотариус"
        :return срок уведомления
        """
        cursor = db.cursor()
        try:
            sql_update_query = """SELECT srok FROM personNotary WHERE id = ? """
            cursor.execute(sql_update_query, (id,))
            query_result = cursor.fetchall()
            if query_result is None:
                return None
            else:
                for srok in query_result:
                    print("info ", srok)
                    return srok[0]
        except db.Error as error:
            log.error_info(id, "Error: %s" % error)
            print("Ошибка в методе info_srok: {}".format(error))

    def info_notarius(self, id, db):
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
            log.error_info(id, "Error: %s" % error)
            print("Ошибка в методе info_notarius: {}".format(error))

    def info_zapros(self, id, db):
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

            log.error_info(id, "Ошибка в методе info_zapros: %s" % error)
            print("Failed to get record from MySQL table: {}".format(error))

    def create_reg(self, telephon, id_tel, db):
        """
        поиск по номеру телефона человека, если не нашёл, возвращает False
        :param telephon:
        :param id_tel:
        :param db:
        :return: False или result
        """
        cursor = db.cursor()
        result = []
        try:
            sql = """select * from personNotary where telephone_number = ? """
            cursor.execute(sql, (telephon,))
            query_result = cursor.fetchall()
            if len(query_result) == 0:
                return False
            else:
                for user in query_result:
                    sql = f"""UPDATE personNotary SET id = {id_tel} WHERE telephone_number = ?"""
                    cursor.execute(sql, (telephon,))
                    result.append(user[2])
                    result.append(user[3])
                    result.append(user[9])
                    result.append(user[10])
                    db.commit()
                return result
        except db.Error as error:
            log.log_error4("Ошибка в методе create_reg: %s" % error, telephon, id_tel)
            return None
        cursor.close()

    def create_new_person(self, id, tel, name, l_name, db):
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
            sql = """INSERT INTO personNotary (id, telephone_number, first_name, last_name) 
                    VALUES (?, ?, ?, ?) """
            cursor.execute(sql, (id, tel, name, l_name))
            query_result = cursor.fetchall()
            db.commit()

        except db.Error as error:
            log.log_error5("Ошибка в методе create_new_person: %s" % error, id, tel, name, l_name)
            print("Failed to get record from MySQL table: {}".format(error))

        cursor.close()

    def info_id(self, id, db):
        """
        поиск телефона по id для записи
        """
        cursor = db.cursor()
        try:
            sql_update_query = """SELECT telephone_number FROM personNotary WHERE id = ? """
            cursor.execute(sql_update_query, (id,))
            # cursor.execute(sql_update_query, id)
            query_result = cursor.fetchall()
            for tel in query_result:
                print("tel ", tel[0])
                return tel[0]
        except db.Error as error:
            log.error_info(id, "Ошибка в методе info_id: %s" % error)
            print("Failed to get record from MySQL table: {}".format(error))

    def info_telephone(self, id, db):
        """ответ на запрос пользователя о предоставлении онформации о записи """
        cursor = db.cursor()
        try:
            sql_update_query = """SELECT telephone_number FROM personNotary WHERE id = ? """
            cursor.execute(sql_update_query, (id,))
            query_result = cursor.fetchall()
            for tel in query_result:
               return tel[0]

        except db.Error as error:
            log.error_info(id, "Ошибка в методе info_telephone: %s" % error)
            print("Failed to get record from MySQL table: {}".format(error))

    def otmetka_NO_uvedomlen(self, tel, db):
        """если в базе найден человек, которого необходимо уведомить,
        НО бот не может уведомить, потому что нет ID " """

        text = " НЕ УВЕДОМЛЕН!!! "
        data = str(datetime.now().strftime("%d.%m.%Y"))
        data_sms = text + data
        print("data_sms ", data_sms)

        """изменение значения ячейки"""
        cursor = db.cursor()
        try:
            sql_update_query = """Update personNotary set data_sms = ? where telephone_number = ?"""
            data = (data_sms, tel)
            cursor.execute(sql_update_query, data)
            db.commit()
            print("Запись успешно обновлена")
            db.commit()
            cursor.close()
            log.no_identification(f"пользователь с номером телефона {tel} "
                                  f"не зарегистрировался в боте. Уведомить не получилось")
        except db.Error as error:
            log.log_otmetka_uvedomlen_except("Failed to get record from MySQL table: {}".format(error))
            print("Failed to get record from MySQL table: {}".format(error))