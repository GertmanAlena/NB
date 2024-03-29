#### Geekbrains

#### Разработчик

#### Тема проекта: Разработка Telegram Bot на Python в сфере нотариальной деятельности для усовершенствования работы нотариальных контор.


#### Гертман Елена Александровна


###### Республика Беларусь, Витебская область, Оршанский район, город Орша

###### 2023


________________________

#### Содержание

### [Введение](#Введение)   
#### [Глава 1 Что такое Бот и для чего он нужен](#Глава-1-Что-такое-Бот-и-для-чего-он-нужен)    
[1.1 Понятие Бота и его основные функции](#1.1-Понятие-Бота-и-его-основные-функции)  
[1.2 Виды Ботов](#1.2-Виды-Ботов)   
[1.3 Выбор программного обеспечения для разработки бота](#1.3-Выбор-программного-обеспечения-для-разработки-бота)   
[1.4 Выводы](#1.4-Выводы) 
#### [Глава 2. Методология разработки Telegram Bot](#Глава-2-Методология-разработки-Telegram-Bot)   
[2.1. Модули, используемые для разработки Telegram Bot Python](#1.4-Модули)      
[2.2. Функции, используемые для разработки Telegram Bot Python](#1.4-Функции)   
[2.3. Операторы и циклы, конструкции и методы для разработки Telegram Bot Python](#1.4-Операторы-и-циклы)
#### [Глава 3. Белорусская нотариальная палата. Цели, задачи Белорусской нотариальной палаты. Основные принципы работы нотариальных контор](#1.4-БНП>)   
#### [Заключение](#Заключение)
#### [Список используемой литературы](#литература)
#### [Приложения](#Приложения)


_______________________

## Введение

    В современном мире люди стараются получить как можно больше информации и ответов на свои запросы с минимальными затратами     
времени и средств. Гаджеты занимают всё большее место в нашей жизни и посредствам их функций человек может производить    
оплату за какой-либо товар(услугу), совершать покупки, можно в любое время связаться с друзьями, родственниками, коллегами для того,     
слушать интересующие подкасты, музыку,смотреть фильмы, изучать, творить, играть, тренироваться, исследовать…..    
    В сфере нотариальной деятельности основной проблемой является организация записи граждан на приём к нотариусу,    
а так же извещение граждан о необходимости записи к нотариусу посредством почтовых писем. Запись на приём всегда велась по телефону     
либо при непосредственном посещении специалиста по записи.    
    Также, граждане, у которых умер кто-либо, после кого необходимо вступить в права наследования, также должны следить на сроком    
в 6 месяцев, и после его истечения явиться к нотариусу, предварительно записавшись на приём. В добавок ко всему, очень часто,   
у граждан нет возможности самостоятельно собрать необходимый пакет документов для совершения какого-либо нотариального действия и    
в таком случае нотариус сам запрашивает эти документы у организаций, после чего также, посредством почтового извещения сообщает   
гражданину о том, что документы собраны и он может записаться на приём и оформить необходимые документы. Эти цепочки действий,   
а особенно ожидания гражданином почтового извещения, его запись на приём, очень длительны по времени и не рациональны в использовании   
времени и средств в виде затрат на почтовые отправления.    
    Также определённой проблемой является то, что большой процент клиентов составляют иностранные граждане, которые не могут по    
телефону решить свои вопросы и посетить нотариальную контору также не предоставляется возможным.    
    Для того, чтобы минимизировать почтовые расходы и улучшить (упростить) процедуру записи на приём к нотариусу и извещения граждан,     
для упрощения иностранным гражданам решить некоторые свои нотариальные вопросы, создавался Telegram Bot.    
    Запись граждан через Telegram Bot к нотариусу ведётся в xslx таблицах, где бот, в случае записи гражданина к нотариусу,    
предложит даты и свободное время для записи, покажет на какой день и к кому записан гражданин.    
    С помощью SQLite будет отслеживаться информация по оформлению наследственных дел, информация о датах явки и записи,   
по появившейся информации в базе данных Telegram Bot будет присылать клиенту уведомление о том, что необходимо записаться или о том,   
что все необходимые для нотариального действия документы собраны.    
    Целью данной работы является изучение особенности создания клиент мессенджера (Telegram Bot) на Python,   
с функциями ведения записи на приём к специалисту и функцией уведомления клиентов.   
    Для выполнения поставленной цели необходимо выполнить следующие задачи:
1.	Изучить документации к библиотекам, касающиеся темы исследования;
2.	Ознакомиться с возможными вариантами работы Telegram Bot, возможными вариантами взаимодействия пользователя и Telegram Bot;
3.	Написать Telegram Bot на Python.
____
[:arrow_up:Содержание](#Содержание)
___
### Глава 1    
### Что такое Бот и для чего он нужен

    1.1. Понятие Бота и его основные функции.     
    Бот — это небольшое приложение, которое самостоятельно выполняет заранее созданные задачи без участия пользователя.   

Telegram-бот умеет делать всё, что мог бы делать человек в чате: отвечать на вопросы, присылать ссылки на сайты или    
создавать мемы. Автоматически или по запросу он может отправлять:    
- текстовые сообщения;   
- картинки;   
- видео;   
- файлы. 

Иными словами чат-боты – это специальные аккаунты, за которыми не закреплен какой-либо человек, а сообщения, отправленные    
с них или на них, обрабатываются внешней системой. Кроме того, для пользователя общение с ботом выглядит как обычная переписка    
с реальным человеком.  

Боты умеют:   
- выполнять действия, которые нельзя настроить на канале. Например продать товар и принять оплату, общаться с пользователем.    
Боты для Телеграма могут собирать потенциальных клиентов, подключая их к CRM, системе продажи билетов или платформе обмена сообщениями.   
  - выполнять несколько разных команд одновременно. Важная функция ботов – возможность запускать цепочку действий, постепенно    
  запрашивая у пользователя новую информацию. Если отправить боту команду /start, на экране появятся кнопки.   

  <image src="/project_diplom_md/images/screen.jpg" alt="Start_Bot" width="500">   
- размещать веб-приложения, написанные на JavaScript. Это позволяет создавать гибкие интерфейсы, которые могут поддерживать    
всё – от интернет-магазинов до приключенческих игр.   
- интеграция с Telegram позволяет подключить собственного бота, отправлять через него сообщения в указанные каналы или указанному    
пользователю и получать все сообщения, которые используются в переписке и отправлять в нужный сервис[1].   
Компьютерные и интернет-боты по сути являются цифровыми инструментами и, как любой инструмент, могут использоваться как во благо,    
так и во вред.   
 «Хорошие» боты выполняют полезные задачи, а «плохие» или вредоносные боты могут использоваться для взлома, рассылки спама, шпионажа,    
прерывания и взлома веб-сайтов любого размера. По оценкам, в настоящее время до половины всего интернет-трафика приходится на компьютерных    
ботов, выполняющих определенные задачи, такие как автоматизация обслуживания клиентов, имитация человеческого общения в социальных сетях,    
помощь компаниям в поиске контента в Интернете и в поисковой оптимизации.     

    1.2. Виды ботов.      
       
    Существует много разных ботов: магазины используют умных помощников, чтобы клиенты могли оплачивать товары и общаться с покупателями,    
киноманы ищут с помощью ботов фильм, за которым будет приятно скоротать вечер, контент-менеджеры настраивают отложенные публикации.   
    Что делают боты, не являющиеся вредоносными? Есть много разных видов ботов:   
    •	Чат-боты.   
    Боты, имитирующие человеческий разговор, отвечают запрограммированными ответами на определенные фразы.   
    На диаграмме ниже можно заметить изменений рынка чат-ботов.   
    
