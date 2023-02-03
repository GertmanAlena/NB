
import datetime as DT


now_time = DT.datetime.now()

from aifc import Error
import time
import logger as log


def notif(db):
    print("notif...")
    cursor = db.cursor()
    t = "уведомлен "
    data_now = str(DT.datetime.now().strftime("%d.%m.%Y"))
    text = t + data_now
    print("text...", text)

    try:

        sql_update_query = """Update personNotary set notification = ? where notification = ?"""
        data = (text, data_now)
        cursor.execute(sql_update_query, data)
        db.commit()
        print("Запись успешно обновлена")
        db.commit()

        sql = """select * from personNotary where notification = ? """

        cursor.execute(sql, (text,))
        query_result = cursor.fetchall()
        print(len(query_result))

        for row in query_result:
            print("row", row)

        if len(query_result) != 0:
            res = []
            for row in query_result:
                print("0...", row[2])

                print("найден пользователь", row)
                # log.query_res(row)
                print(row[0])
                res.append(row)

            print("res ", res)
            return res

        db.commit()
        cursor.close()


    except Error as e:

        print('Error sending message', e)
        log.log_error(e)

