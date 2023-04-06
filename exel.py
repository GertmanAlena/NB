import os
from pathlib import Path
import openpyxl
import logger as log
from openpyxl.comments import Comment
import name_file as nf

def x_file(d, notarius):
    """
    метод выбора свободного времени для записи
    :param d: выбранный день
    :param notarius: выбранный нотариус
    :return: free_time список свободного времени
    """
    try:
        sheet = activ_list(notarius, d) # получаем нужный акривный лист нужного нотариуса
        max_rows = sheet.max_row
        max_cols = sheet.max_column
        free_time = data_z(sheet, max_rows, max_cols, d) # выбираем свободное время
        return free_time
    except Exception as e:
        print("Error x_file", e)
        return False
def data_z(sheet, max_rows, max_cols, d):
    """
    метод поиска нужной ячейки для записи принимает параметры
    :param sheet: активный лист
    :param max_rows: максимальное количество строк в листе
    :param max_cols: максимальное количество колонок в листе
    :param d: день для записи
    :return:  free_time список со свободным временем для записи
    """
    free_time = []
    for i in range(1, max_cols + 1):
        # print(sheet.cell(row=1, column=i).value)
        if sheet.cell(row=1, column=i).value != None and d == sheet.cell(row=1, column=i).value.strftime("%d.%m.%Y"):
            print(sheet.cell(row=1, column=i).value.strftime("%d.%m.%Y"))
            free_time.append(sheet.cell(row=2, column=i).value)
            # x = sheet.cell(row=1, column=i)
            # x = i
            for j in range(2, max_rows+1):
                if sheet.cell(row=j, column=i).value == None:
                    free_time.append(sheet.cell(row=j, column=1).value.strftime("%H:%M"))
                    # print(sheet.cell(row=j, column=1).value)
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
        if notarius == "Гоголь":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')
            worksheet = wb.active
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')
        elif notarius == "Сойка":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Soyka.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Soyka.xlsx')
        elif notarius == "Думанова":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Dumanova.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Dumanova.xlsx')
        elif notarius == "Ковалевская":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Kovalevskaya.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Kovalevskaya.xlsx')
        elif notarius == "Сильченко":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Silchenco.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Silchenco.xlsx')
        elif notarius == "Бондаренко":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Bondarenco.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Bondarenco.xlsx')
        elif notarius == "Чикан":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Chikan.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Chikan.xlsx')
        elif notarius == "Котикова":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Koticova.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Koticova.xlsx')
        elif notarius == "Шинкевич":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Shinkevich.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Shinkevich.xlsx')
        elif notarius == "Позднякова":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Pozdnyakova.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Pozdnyakova.xlsx')
        elif notarius == "Демидова":
            wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Demidova.xlsx')
            worksheet = wb.active
            print("worksheet ", worksheet)
            save_file(worksheet, time, day, power_of_attorney, name, last_name, tel)
            wb.save('D:/studies/BotNotaryMy/Notarius/Demidova.xlsx')

        return True
    except Exception as e:
        log.log_zapis_not(e, notarius)
        return False

def activ_list(notarius, day):
    month = day.split('.')[1]
    try:
        wb = openpyxl.load_workbook(nf.search_file(notarius))


        # if notarius == 'Гоголь':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')
        # elif notarius == 'Сойка':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Soyka.xlsx')
        # elif notarius == 'Демидова':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Demidova.xlsx')
        # elif notarius == 'Думанова':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Dumanova.xlsx')
        # elif notarius == 'Ковалевская':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Kovalevskaya.xlsx')
        # elif notarius == 'Сильченко':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Silchenco.xlsx')
        # elif notarius == 'Бондаренко':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Bondarenco.xlsx')
        # elif notarius == 'Чикан':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Chikan.xlsx')
        # elif notarius == 'Котикова':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Koticova.xlsx')
        # elif notarius == 'Шинкевич':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Shinkevich.xlsx')
        # elif notarius == 'Позднякова':
        #     wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Pozdnyakova.xlsx')

        if month == "01":
            worksheet = wb['Январь']
            print(worksheet)
        elif month == "02":
            worksheet = wb['Февраль']
            print("worksheet ", worksheet)
        elif month == "03":
            worksheet = wb['Март']
            print("worksheet ", worksheet)
        elif month == "04":
            worksheet = wb['Апрель']
            print("worksheet ", worksheet)
        elif month == "05":
            worksheet = wb['Май']
            print("worksheet ", worksheet)
        elif month == "06":
            worksheet = wb['Июнь']
            print("worksheet ", worksheet)
        elif month == "07":
            worksheet = wb['Июль']
            print("worksheet ", worksheet)
        elif month == "08":
            worksheet = wb['Август']
            print("worksheet ", worksheet)
        elif month == "09":
            worksheet = wb['Сентябрь']
            print("worksheet ", worksheet)
        elif month == "10":
            worksheet = wb['Октябрь']
            print("worksheet ", worksheet)
        elif month == "11":
            worksheet = wb['Ноябрь']
            print("worksheet ", worksheet)
        elif month == "12":
            worksheet = wb['Декабрь']
            print("worksheet ", worksheet)
        return worksheet
    except Exception as e:
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
def search_month(l):
    if l == 1:
        return 'Январь'
    elif l == 2:
        return 'Февраль'
    elif l == 3:
        return 'Март'
    elif l == 4:
        return 'Апрель'
    elif l == 5:
        return 'Май'
    elif l == 6:
        return 'Июнь'
    elif l == 7:
        return 'Июль'
    elif l == 8:
        return 'Август'
    elif l == 9:
        return 'Сентябрь'
    elif l == 10:
        return 'Октябрь'
    elif l == 11:
        return 'Ноябрь'
    elif l == 12:
        return 'Декабрь'
def search(telephone):
    """
    метод поиска записи
    :param telephone: принимает номер телефона гражданина по которому будет искать куда он записан
    :return: дату время и к какому нотариусу записан гражданин
    """
    result_zapis = []
    directory = nf.directory
    pathlist = Path(directory).glob('*.xlsx')
    result = ''
    try:
        for path in pathlist:       # перебираем файлы в директории
            wb = openpyxl.load_workbook(path)           # открываем файлы в директории поочерёдно
            for l in range(1, 13):          # проходим по листам в файле
                mes = search_month(l)
                worksheet = wb[search_month(l)]
                max_rows = worksheet.max_row
                max_cols = worksheet.max_column
                for i in range(1, max_rows + 1):            # по строкам
                    for j in range(1, max_cols + 1):            # по столбцам
                        if worksheet.cell(row=i, column=j).comment:         # если комментарий есть
                            com = worksheet.cell(row=i, column=j).comment
                            result = str(com).split("\n")[1]
                            tel = ""
                            for k in range(0, len(result)):
                                print("k ", result[k])
                                if result[k].isnumeric():
                                    tel += result[k]
                            print("tel ", tel)
                        if result == str(telephone):
                            n = path
                            notar = nf.notar_file(n)
                            time_zapis = str(worksheet.cell(row=i, column=1).value)
                            data_zapis = str(worksheet.cell(row=1, column=j).value.strftime("%d.%m.%Y"))
                            result_zapis.append(notar)
                            result_zapis.append(time_zapis)
                            result_zapis.append(data_zapis)
                            print("result_zapis ", result_zapis)
                            return result_zapis
    except Exception as e:
        print(e)
        return False