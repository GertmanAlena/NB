import search_notar_doc as snd

directory = r'D:\studies\BotNotaryMy\Notarius'

def notar_file(file_name):
    f = str(file_name).split('\\')[4]
    try:
        if f == 'Gogol.xlsx':
            return snd.case.notarius_name('Гоголь')
        elif f == 'Soyka.xlsx':
            return snd.case.notarius_name('Сойка')
        elif f == 'Demidova.xlsx':
            return snd.case.notarius_name('Демидова')
        elif f == 'Dumanova.xlsx':
            return snd.case.notarius_name('Думанова')
        elif f == 'Kovalevskaya.xlsx':
            return snd.case.notarius_name('Ковалевская')
        elif f == 'Silchenco.xlsx':
            return snd.case.notarius_name('Сильченко')
        elif f == 'Bondarenco.xlsx':
            return snd.case.notarius_name('Бондаренко')
        elif f == 'Chikan.xlsx':
            return snd.case.notarius_name('Чикан')
        elif f == 'Koticova.xlsx':
            return snd.case.notarius_name('Котикова')
        elif f == 'Shinkevich.xlsx':
            return snd.case.notarius_name('Шинкевич')
        elif f == 'Pozdnyakova.xlsx':
            return snd.case.notarius_name('Позднякова')
    except Exception as e:
        print(e)

def search_file(notarius_name):
    try:
        if notarius_name == 'Гоголь':
            return 'D:/studies/BotNotaryMy/Notarius/Gogol.xlsx'
        elif notarius_name == 'Сойка':
            return 'D:/studies/BotNotaryMy/Notarius/Soyka.xlsx'
        elif notarius_name == 'Демидова':
            return 'D:/studies/BotNotaryMy/Notarius/Demidova.xlsx'
        elif notarius_name == 'Думанова':
            return 'D:/studies/BotNotaryMy/Notarius/Dumanova.xlsx'
        elif notarius_name == 'Ковалевская':
            return 'D:/studies/BotNotaryMy/Notarius/Kovalevskaya.xlsx'
        elif notarius_name == 'Сильченко':
            return 'D:/studies/BotNotaryMy/Notarius/Silchenco.xlsx'
        elif notarius_name == 'Бондаренко':
            return 'D:/studies/BotNotaryMy/Notarius/Bondarenco.xlsx'
        elif notarius_name == 'Чикан':
            return 'D:/studies/BotNotaryMy/Notarius/Chikan.xlsx'
        elif notarius_name == 'Котикова':
            return 'D:/studies/BotNotaryMy/Notarius/Koticova.xlsx'
        elif notarius_name == 'Шинкевич':
            return 'D:/studies/BotNotaryMy/Notarius/Shinkevich.xlsx'
        elif notarius_name == 'Позднякова':
            return 'D:/studies/BotNotaryMy/Notarius/Pozdnyakova.xlsx'
    except Exception as e:
        print("search_file ", e)

def search_month(namber):

    try:
        if namber == "1" or namber == "01":
            return 'Январь'
        elif namber == "2" or namber == "02":
            return 'Февраль'
        elif namber == "3" or namber == "03":
            return 'Март'
        elif namber == "4" or namber == "04":
            return 'Апрель'
        elif namber == "5" or namber == "05":
            return 'Май'
        elif namber == "6" or namber == "06":
            return 'Июнь'
        elif namber == "7" or namber == "07":
            return 'Июль'
        elif namber == "8" or namber == "08":
            return 'Август'
        elif namber == "9" or namber == "09":
            return 'Сентябрь'
        elif namber == "10":
            return 'Октябрь'
        elif namber == "11":
            return 'Ноябрь'
        elif namber == "12":
            return 'Декабрь'
    except Exception as e:
        print("search_month ", e)