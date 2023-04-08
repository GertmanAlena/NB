from telebot import types

class Button():


    button_power_of_attorney = types.KeyboardButton('✔️Доверенность')
    button_will = types.KeyboardButton('✔️Завещание')
    button_agreement = types.KeyboardButton('✔️Согласие')
    button_statement = types.KeyboardButton('✔️Заявление')
    button_consultation = types.KeyboardButton('✔️Консультация')
    button_other_action = types.KeyboardButton('✔️иное действие')
    back = types.KeyboardButton('Назад')

    button_info_delo = types.KeyboardButton('Информация о моём деле')
    button_website = types.KeyboardButton('Перейти на сайт и ознакомиться')
    button_mail = types.KeyboardButton('Написать e-mail')
    button_entry = types.KeyboardButton('Записаться на приём к нотариусу')
    button_info_zapisi = types.KeyboardButton('Найти сведения о моей записи')

    button_office_Vitebsk = types.KeyboardButton('Витебский нотариальный округ')
    button_office_Minsk_gor = types.KeyboardButton('Минский городской нотариальный округ')
    button_office_Minsk_obl = types.KeyboardButton('Минский областной нотариальный округ')
    button_office_Brest = types.KeyboardButton('Брестский нотариальный округ')
    button_office_Gomel = types.KeyboardButton('Гомельский нотариальный округ')
    button_office_Grodno = types.KeyboardButton('Гродненский нотариальный округ')
    button_office_Mogilev = types.KeyboardButton('Могилёвский нотариальный округ')
    button_office_Orsha = types.KeyboardButton('Нотариальная контора Оршанского района и г.Орши')
    button_office_Baran = types.KeyboardButton('Нотариальная контора г.Барани Оршанского района')
