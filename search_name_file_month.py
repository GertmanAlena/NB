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