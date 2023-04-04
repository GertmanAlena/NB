
def documents(value):
    text = "\n\n💳 Оплату можно произвести после посещения нотариуса банковской картой в нотариальной конторе, а" \
                   "при отсутсвии банковской карты, Вам необходимо будет оплатить в отделении банка самостоятельно!"
    match value:
        case "Доверенность":
            return "Для оформления доверенности, \nк нотариусу необходимо явиться лицу, от чьего имени будет оформляться доверенность " \
                   "\n(кто будет оформлять доверенность)" \
                   "\nс паспортом \n\n(при наличии также предъявляется: " \
                   "пенсионное удостоверние, документы, подтверждающие родственные отношения, " \
                   "либо документы, подтверждающие факт регистрации брака. " + text

        case "Завещание":
            return "Для оформления завещания\n, к нотариусу необходимо явиться лицу, кто будет оформлять завещание " \
                   "\nс паспортом \n\n(при наличии также предъявляется пенсионное удостоверние. " \
                   "\nЕсли лицо, которое оформляет завещание, собственноручно напишет два экземпляра завещания," \
                   " ему необходимо явиться с паспортом и документом, предоставляющим льготу (если такое имеется)," \
                   "\n если, лицо, которое оформляет завещание, собственноручно НЕ напишет завещание, то " \
                   "ему необходимо явиться с паспортом и документом, предоставляющим льготу (если такое имеется), а " \
                   "также необходимо присутствие свидетеля - постороннего лица, не родственника, лица не заинтересованного" \
                   "в завещании" + text
        case "Согласие":
            return "Для оформления согласия,\n к нотариусу необходимо явиться лицу(лицам), " \
                   "кто будет оформлять согласие с паспортом" + text
        case "Заявление":
            return "Для оформления заявления,\n к нотариусу необходимо явиться лицу(лицам), " \
                   "кто будет оформлять заявление с паспортом" + text
        case "Консультация":
            return text

            default()

def notarius_name(value):
    match value:
        case "Сойка":
            return "Сойка Елена Яковлевна \nкабинет № 8"
        case "Гоголь":
            return "Гоголь Наталья Андреевна \nкабинет № 9"
        case "Думанова":
            return "Думанова Ирина Николаевна \nкабинет № 3"
        case "Ковалевская":
            return "Ковалевская Анастасия Геннадьевна \nкабинет № 3"
        case "Сильченко":
            return "Сильченко Анна Васильевна \nкабинет № 4"
        case "Бондаренко":
            return "Бондаренко Юлия Павловна \nкабинет № 5"
        case "Чикан":
            return "Чикан Наталья Михайловна \nкабинет № 6"
        case "Котикова":
            return "Котикова Ольга Владимировна  \nкабинет № 7"
        case "Шинкевич":
            return "Шинкевич Екатерина Александровна \nкабинет № 8"
        case "Позднякова":
            return "Позднякова Светлана Евгеньевна \nкабинет № 10"
        case "Демидова":
            return "Демидова Ванда Геннадьевна \nкабинет № 11"
            default()