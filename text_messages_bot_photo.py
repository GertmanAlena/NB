
class Help():
    text_help = f'\n <b>В Боте Вы сможете</b>\n' \
                '☑️Заисаться на приём к нотариусу для оформления документов, ' \
                'не требущих предварительной консультации!\n' \
                '☑️Перейти на сайт Белорусский Нотариальной Палаты и ' \
                'там ознакомиться с режимом работы нотариальных контор и нотариусов\n' \
                '☑️Написать электронное письмо в нотариальную контору, выбрав её из списка\n' \
                '☑️Если у Вас имеется наследственное дело, то вы можете получить о нём информацию\n' \
                '☑️Вы можете найти информацию о том, когда Вы записаны к нотариусу\n' \
                ' <b>Если у Вас возникли какие-либо вопросы, обратитесь по телефону</b> 📞 +375 216 56-88-94'

class Info_Notification():
    text_otvet = f'\n\n✅На все запросы по Вашему делу пришли ответы!!!'
    text_zapis = f'\n✅В связи стем, что истекает срок 6 месяцев Вам необходимо записаться к нотариусу'
class Info_Delo():

    text_not_delo = 'наследственное дело в базе <b>НЕ найдено</b>. \nУточните информацияю по телефону 📞 +375 216 56-88-94'
    text_not_zapros = "Ответы на запросы ожидаются от организаций! Как только все запросы будут получены," \
                         " Вам придёт уведомление от меня"
    text_zapis_not = f'\nВам необходимо записаться к нотариусу '
    text_zapis_not2 = 'Так же вы можете найти интересующую Вас информацию о наследственном деле на ' \
                      'ОФИЦИАЛЬНОМ сайте нотариата Республики Беларусь\n'\
                      '*Перейдя по ссылке*\n'
class Info_Zapis():
    def tel(self, ):
        t = '\nУточните информацияю по телефону 📞 +375 216 56-88-94'
        return t
    def data_zapis(self, ):
        t = 'На какую дату Вы хотите записаться, чтобы оформить'
        return t
    def cancel_recording(self, ):
        t = 'Для отмены записи необходимо позвонить по телефону \n📞 +375 216 56-88-94'
        return t
    def sunday(self, ):
        t = '‼ ВОСКРЕСЕНЬЕ ВЫХОДНОЙ ДЕНЬ ‼\nпопробуйте ещё раз??🗓️'
        return t
    def day_off(self, ):
        t = '‼ НЕ РАБОТАЕТ ‼\n попробуйте выбрать другую дату или другого нотариуса'
        return t
    def day_off2(self, ):
        t = '‼ рабочей день окончен ‼\n попробуйте выбрать другую дату или другого нотариуса'
        return t

class Start():

    def text_start(self, ):
        text_s = '\n\nВас приветствует <b>Telegram Bot</b> Нотариальной конторы Оршанского района и г.Орши\n\n' \
               'Для дальнейшей работы с Ботом' \
               '\nподтвердите пожалуйста свои данные, нажав кнопку ниже \n\n'
        return text_s
    def photo(self, ):
        return open('logo.jpg', 'rb')
    def message_reg_ok(self, ):
        """
        текст, если человек сам зарегистрировался и НД нет в базе
        :return:
        """
        text = '\n✅ <b>Вы успешно зарегистрированы!</b>\n'
        return text

    def reg_ok2(self, ):
        """
        текст, если есть НД и человек внесён в базу
        :return:
        """
        t = '\nВы можете найти полезную информацию на официальном сайте БНП' \
            '\nи там ознакомиться с режимами работы нотариальных контор и нотариусов. ' \
            'Также Вы можете записаться к нотариусу и найти полезную информацию'
        return t
    def again(self, ):
        """
        текст, если есть НД и человек внесён в базу
        :return:
        """
        t = 'Попробуйте пожалуйста ещё раз'
        return t
