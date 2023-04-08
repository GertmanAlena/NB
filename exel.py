import os
from pathlib import Path
import openpyxl
import logger as log
from openpyxl.comments import Comment
import search_name_file_month as snfm
import datetime as DT
def x_file(day, notarius):
    """
    метод выбора свободного времени для записи
    :param d: выбранный день
    :param notarius: выбранный нотариус
    :return: free_time список свободного времени
    """
    try:
        sheet = activ_list(notarius, day) # получаем нужный акривный лист нужного нотариуса
        print("sheet>>>>>>>>", sheet)
        max_rows = sheet.max_row
        max_cols = sheet.max_column
        free_time = data_z(sheet, max_rows, max_cols, day) # выбираем свободное время
        return free_time
    except Exception as e:
        print("Error x_file", e)
        return False
def data_z(sheet, max_rows, max_cols, day):
    """
    метод поиска нужной ячейки для записи принимает параметры
    :param sheet: активный лист
    :param max_rows: максимальное количество строк в листе
    :param max_cols: максимальное количество колонок в листе
    :param d: день для записи
    :return:  free_time список со свободным временем для записи
    """
    free_time = []
    tame_work = ''
    for i in range(1, max_cols + 1):
        if sheet.cell(row=1, column=i).value != None and day == sheet.cell(row=1, column=i).value.strftime("%d.%m.%Y"):
            print(sheet.cell(row=1, column=i).value.strftime("%d.%m.%Y"))
            free_time.append(sheet.cell(row=2, column=i).value)
            tame_work = sheet.cell(row=2, column=i).value
            for j in range(2, max_rows+1):
                if sheet.cell(row=j, column=i).value == None:
                    free_time.append(sheet.cell(row=j, column=1).value.strftime("%H:%M"))

    if day == DT.datetime.now().strftime("%d.%m.%Y"):
        print("day", day, "DT.datetime.now().strftime ", DT.datetime.now().strftime("%d.%m.%Y"))
        work_end = tame_work.split("-")[1]
        print("work_end",work_end)
        if DT.datetime.now().strftime("%H:%M") > work_end:
            print(DT.datetime.now().strftime("%H:%M"), " > ", work_end)
            return None

    else:
        print("free_time ", free_time)
        return free_time

def zapis_not(time, notarius, day, power_of_attorney, name, last_name, tel):
    """
    метод записи в xlsx выбирает нужную диреторию по нотариусу и задаёт активный лист
    передает директорию, активный лист, нотариуса, время и дату в метод записи и сохранения файла save_file
    :param time: время
    :param notarius: нотариус
    :param day: дата
    :return:
    """
    print("in zapis_not")
    try:
        wb = openpyxl.load_workbook(snfm.search_file(notarius))
        worksheet = wb.active
        save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
        wb.save(snfm.search_file(notarius))
        return True
    except Exception as e:
        log.log_zapis_not(e, notarius)
        return False

def activ_list(notarius, day):
    month = day.split('.')[1]
    print("month >>>>", month)
    try:
        wb = openpyxl.load_workbook(snfm.search_file(notarius))
        print("wb >>>>", wb)
        worksheet = wb[snfm.search_month(month)]
        print("worksheet >>>>", worksheet)

        return worksheet
    except Exception as e:
        print("e activ_list", e)
        log.activ_list(e, notarius, day)
        return False

def save_file(worksheet, time, day, power_of_attorney, name, last_name, tel):
    print("save_file")
    """
    метод записи и сохранения
    :param wb: диерктория нотариуса
    :param worksheet: активный лист месяца для записи
    :param notarius: нотариус
    :param time: время для записи
    :param day: день для записи
    :return:
    """

    res = str(name) + " " + str(last_name) + " " + str(tel)
    print("res ", res)
    max_rows = worksheet.max_row
    max_cols = worksheet.max_column
    try:
        for i in range(1, max_cols + 1):
            # ищем нужную дату в строке дат
            if worksheet.cell(row=1, column=i).value != None and day == worksheet.cell(row=1, column=i).value.strftime(
                    "%d.%m.%Y"):
                print("day", day)
                # нашли дату ищем нужную ячейку по времени в столбце с датой
                for j in range(2, max_rows + 1):
                    if worksheet.cell(row=j, column=1).value != None and time == worksheet.cell(row=j,
                                                                                                column=1).value.strftime(
                            "%H:%M"):
                        print(">>>><<<<<", worksheet.cell(row=j, column=i).value)
                        worksheet.cell(row=j, column=i).value = power_of_attorney

                        comment = Comment(text=res, author='Tori Code')
                        worksheet.cell(row=j, column=i).comment = comment

                        print(">>>>cell.value<<<<<", worksheet.cell(row=j, column=i).value)
                        return True
    except Exception as e:
        print(e)
        return False

def search(telephone):
    """
    метод поиска записи
    :param telephone: принимает номер телефона гражданина по которому будет искать куда он записан
    :return: дату время и к какому нотариусу записан гражданин
    """
    result_all = []
    directory = snfm.directory
    pathlist = Path(directory).glob('*.xlsx')
    result = ''
    try:
        for path in pathlist:       # перебираем файлы в директории
            wb = openpyxl.load_workbook(path)           # открываем файлы в директории поочерёдно
            for l in range(1, 13):          # проходим по листам в файле
                mes = snfm.search_month(str(l))
                worksheet = wb[mes]
                max_rows = worksheet.max_row
                max_cols = worksheet.max_column
                for i in range(1, max_rows + 1):            # по строкам
                    for j in range(1, max_cols + 1):            # по столбцам
                        result_zapis = []
                        if worksheet.cell(row=i, column=j).comment:         # если комментарий есть

                            com = worksheet.cell(row=i, column=j).comment
                            result = str(com).split(" ")
                            tel = ""
                            for k in range(0, len(result)):
                                # print("k ", result[k])
                                if result[k].isnumeric():
                                    tel = result[k]
                            if str(telephone) == tel:
                                # print("tel >>>>>>>>>>>>>>>>>>>>>>", tel)
                                # print("telephone >>>>>>>>>>>>>>>>>>>>>>>>", telephone)
                                n = path
                                notar = snfm.notar_file(n)
                                action = str(worksheet.cell(row=i, column=j).value)
                                time_zapis = str(worksheet.cell(row=i, column=1).value)
                                data_zapis = str(worksheet.cell(row=1, column=j).value.strftime("%d.%m.%Y"))
                                if data_zapis.split(".")[2] >= DT.datetime.now().strftime("%d.%m.%Y").split(".")[2] and \
                                        data_zapis.split(".")[1] >= DT.datetime.now().strftime("%d.%m.%Y").split(".")[
                                    1] and \
                                        data_zapis.split(".")[0] >= DT.datetime.now().strftime("%d.%m.%Y").split(".")[
                                    0]:
                                    result_zapis.append(action)
                                    result_zapis.append(notar)
                                    result_zapis.append(time_zapis)
                                    result_zapis.append(data_zapis)
                                    print("result_zapis ", result_zapis)
                                    result_all.append(result_zapis)

        print("result_all ", result_all)
        return result_all
    except Exception as e:
        print(e)
        return False