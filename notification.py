import datetime as DT

now_time = DT.datetime.now()
from aifc import Error
import logger as log

def notif(db, id):
    '''метод поиска в базе людей, которым пришли все ответы на запросы
    но нет отметки, что человек получал уведовление
    text - тексат записи в ячейке в БД (уведомлен 05.02.2023)
    если в БД есть запись в столбце notification, записываем text'''

    cursor = db.cursor()
    t = "уведомлены "
    data_now = str(DT.datetime.now().strftime("%d.%m.%Y"))
    text = t + data_now
    try:
        sql_update_query = """Update personNotary set notification = ? where id = ?"""
        data = (text, id)
        cursor.execute(sql_update_query, data)
        db.commit()
        return True

    except Error as e:
        log.log_error(e)
