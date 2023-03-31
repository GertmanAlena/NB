import os

import openpyxl


# Retrieve current working directory (`cwd`) Получить текущий рабочий каталог
# cwd = os.getcwd()
# cwd
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
    # val = "записали"

    if notarius == "Гоголь":
        wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')
        worksheet = wb.active
        print("worksheet ", worksheet)
        save_file(wb, worksheet, notarius, time, day)
        wb.save('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')
    elif notarius == "Сойка":
        wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Soyka.xlsx')
        worksheet = wb.active
        print("worksheet ", worksheet)
        save_file(wb, worksheet, notarius, time, day)
        wb.save('D:/studies/BotNotaryMy/Notarius/Soyka.xlsx')
    # max_rows = worksheet.max_row
    # max_cols = worksheet.max_column
    # print("max_rows ", max_rows, "max_cols ", max_cols)
    # for i in range(1, max_cols + 1):
    #     if worksheet.cell(row=1, column=i).value != None and day == worksheet.cell(row=1, column=i).value.strftime("%d.%m.%Y"):
    #         print("day", day)
    #         for j in range(2, max_rows + 1):
    #             if worksheet.cell(row=j, column=1).value != None and time == worksheet.cell(row=j, column=1).value.strftime("%H:%M"):
    #                 print(">>>><<<<<", worksheet.cell(row=j, column=i).value)
    #                 # worksheet.cell(row=j, column=i).value = val
    #                 worksheet.cell(row=j, column=i).value = val
    #
    #                 print(">>>>cell.value<<<<<", worksheet.cell(row=j, column=i).value)

    # wb.save('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')


def activ_list(notarius, day):
    month = day.split('.')[1]

    if notarius == 'Гоголь':
        wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')
        # wb = load_workbook('D:/studies/BotNotaryMy/Notarius/Gogol.xlsx')
        if month == "01":
            worksheet = wb.get_sheet_by_name('Январь')
            print(worksheet)
        elif month == "02":
            sheet = wb.get_sheet_by_name('Февраль')
            print(sheet)
        elif month == "03":
            # worksheet = wb.get_sheet_by_name('Март')  # worksheet это лист Марта
            worksheet = wb['Март']
            print("worksheet ", worksheet)
        return worksheet
    elif notarius == 'Сойка':
        wb = openpyxl.load_workbook('D:/studies/BotNotaryMy/Notarius/Soyka.xlsx')
        if month == "01":
            worksheet = wb.get_sheet_by_name('Январь')
            print(worksheet)
        elif month == "02":
            sheet = wb.get_sheet_by_name('Февраль')
            print(sheet)
        elif month == "03":
            # worksheet = wb.get_sheet_by_name('Март')  # worksheet это лист Марта
            worksheet = wb['Март']
            print("worksheet ", worksheet)
        return worksheet
def save_file(wb, worksheet, notarius, time, day):
    val = "записали"
    max_rows = worksheet.max_row
    max_cols = worksheet.max_column
    print("max_rows ", max_rows, "max_cols ", max_cols)
    for i in range(1, max_cols + 1):
        if worksheet.cell(row=1, column=i).value != None and day == worksheet.cell(row=1, column=i).value.strftime(
                "%d.%m.%Y"):
            print("day", day)
            for j in range(2, max_rows + 1):
                if worksheet.cell(row=j, column=1).value != None and time == worksheet.cell(row=j,
                                                                                            column=1).value.strftime(
                        "%H:%M"):
                    print(">>>><<<<<", worksheet.cell(row=j, column=i).value)
                    # worksheet.cell(row=j, column=i).value = val
                    worksheet.cell(row=j, column=i).value = val

                    print(">>>>cell.value<<<<<", worksheet.cell(row=j, column=i).value)
                    return