import os
import pandas as pd
from openpyxl import load_workbook

# Retrieve current working directory (`cwd`) Получить текущий рабочий каталог
cwd = os.getcwd()
cwd
def x_file(d, notarius):

    sheet = activ_list(notarius, d) # получаем нужный акривный лист нужного нотариуса
    print("sheet ", sheet)
    max_rows = sheet.max_row
    max_cols = sheet.max_column

    free_time = data_z(sheet, max_rows, max_cols, d) # выбираем свободное время
    return free_time



def data_z(sheet, max_rows, max_cols, d):

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

def zapis_not(time, notarius, day):
    print(time, notarius, day)

    sheet = activ_list(notarius, day)

    max_rows = sheet.max_row
    max_cols = sheet.max_column
    print("max_rows ", max_rows, "max_cols ", max_cols)
    for i in range(1, max_cols + 1):
        if sheet.cell(row=1, column=i).value != None and day == sheet.cell(row=1, column=i).value.strftime("%d.%m.%Y"):
            print("day", day)
            for j in range(2, max_rows + 1):
                if sheet.cell(row=j, column=1).value != None and time == sheet.cell(row=j, column=1).value.strftime("%H:%M"):
                    print(">>>><<<<<", sheet.cell(row=j, column=i).value)
                    d = sheet.cell(row=j, column=i, value=10)
                    d.value = "pfg"
                    print("d.value ", d.value)

    # print(">>>><<<<<", sheet.Cells().get(time).putValue(day))


def activ_list(notarius, day):
    month = day.split('.')[1]

    if notarius == 'Гоголь':
        wb = load_workbook('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')
        if month == "01":
            sheet = wb.get_sheet_by_name('Январь')
            print(sheet)
        elif month == "02":
            sheet = wb.get_sheet_by_name('Февраль')
            print(sheet)
        elif month == "03":

            sheet = wb.get_sheet_by_name('Март')  # sheet это лист Марта
            return sheet
    elif notarius == 'Сойка':
        wb = load_workbook('D:/studies/BotNotaryMy/Notarius/Soyka.xlsx')
        print(">>>", wb.get_sheet_names())
        if month == "01":
            sheet = wb.get_sheet_by_name('Январь')
            print(sheet)
        elif month == "02":
            sheet = wb.get_sheet_by_name('Февраль')
            print(sheet)
        elif month == "03":
            sheet = wb.get_sheet_by_name('Март')
            print(">>> ", sheet)



        # # Загружаем ваш файл в переменную `file` / вместо 'example' укажите название свого файла из текущей директории
    # file = 'Gogol.xlsx'

    # # Загружаем spreadsheet в объект pandas
    # xl = pd.ExcelFile(file)
    #
    # # Печатаем название листов в данном файле
    # print(xl.sheet_names)

    # Загрузить лист в DataFrame по его имени: df1
    # df1 = xl.parse('Март')
    # print(df1)

    # Change directory  Изменить каталог
    # os.chdir("D:/studies/BotNotaryMy/Notarius")

    # List all files and directories in current directory  Список всех файлов и каталогов в текущем каталоге
    # os.listdir('.')
    # print(os.listdir('.'))