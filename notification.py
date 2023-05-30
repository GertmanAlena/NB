import datetime as DT

now_time = DT.datetime.now()
from aifc import Error
import logger as log

def notif(db):
    '''метод поиска в базе людей, которым пришли все ответы на запросы
    text - тексат записи в ячейке в БД (уведомлен 05.02.2023)
    если в БД есть запись в столбце notification, записываем text'''

    cursor = db.cursor()
    t = "уведомлены "
    data_now = str(DT.datetime.now().strftime("%d.%m.%Y"))
    text = t + data_now

    try:
        sql_update_query = """Update personNotary set notification = ? where notification = ?"""
        data = (text, data_now)
        cursor.execute(sql_update_query, data)
        db.commit()

        '''выбираем из БД по столбцу notification всех с text и добавляем в res для рассылки уведомлений'''

        sql = """select * from personNotary where notification = ? """

        cursor.execute(sql, (text,))
        query_result = cursor.fetchall()

        for row in query_result:
            print("row", row)

        if len(query_result) != 0:
            res = []
            for row in query_result:
                res.append(row)

            print("res ", res)
            return res
        else:
            return None

        db.commit()
        cursor.close()


    except Error as e:
        log.log_error(e)