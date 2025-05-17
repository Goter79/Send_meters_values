# подключаем модуль для Телеграма
import telebot
from telebot import types
# модуль работы со временем
from datetime import datetime, timezone, timedelta
# модуль для работы с базой данных
import sqlite3 as sl
from config import TOKEN;
import os #импортируем модуль "os"

bot = telebot.TeleBot(TOKEN);


# указываем токен для доступа к боту
bot = telebot.TeleBot(TOKEN)

# приветственный текст
start_txt = 'Приветствуем Вас! Это официальный бот компании ООО ГУК-Краснодар. \n\n Тут Вы можете передать показания по своим индивидуальным приборам учета'

# подключаемся к файлу с базой данных
con = sl.connect('reports.db')

# открываем файл
with con:
    # получаем количество таблиц с нужным нам именем
    data = con.execute("select count(*) from sqlite_master where type='table' and name='Meter_Measure'")
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу для отчётов
            with con:
                con.execute("""
                    CREATE TABLE Meter_Measure (
                        id_meter BIGINT PRIMARY KEY,
                        LS VARCHAR(9),
                        Service VARCHAR(20),
                        Number VARCHAR(20),
                        value float,
                        value_old float,
                        LastUpdate VARCHAR(40),
                        id_user VARCHAR(200)
                    );
                """)

# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    #создание клавитуры
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        "Подать показания", "Помощь", "👀 Наш канал")
    bot.send_message(message.chat.id, start_txt, reply_markup=markup_reply)

    # выводим приветственное сообщение
    #bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')
    

# обрабатываем команду /ListIPU, получение списка счетчиков
@bot.message_handler(commands=['List_IPU'])
def List_IPU(message):
    bot.send_message(message.from_user.id, message.text)
    # подключаемся к базе
    con = sl.connect('reports.db')   
    
    # пустая строка для будущих отчётов
    s = ''
     # работаем с базой
    with con:
        # выполняем запрос к базе
        data = con.execute('SELECT id_meter, LS, Number, value, value_old  FROM Meter_Measure').fetchall()
        # перебираем все результаты
        for row in data:
            # формируем строку в общем отчёте
            #s = s +  ' id_meter ->' + str(row[0])+\
            #         '\n LS ->' + row[1]+  '\n Number ->' + row[2] +  '\n value ->' + str(row[3]) +  '\n value_old ->' + str(row[4])  + '\n\n'
             s += "id_meter:           {0}\nЛицевой счет: {1}\nНомер ИПУ:      {2}\nТек.показ-я:    {3}\nПред.показ-я: {4}\n\n".format(row[0], row[1], row[2], row[3], row[4])

            
            
    # если нет данных
    if s == '':
        # формируем новое сообщение
        s = 'Нет данных'
    # отправляем общий отчёт обратно в телеграм
    #bot.send_message(message.from_user.id, s, parse_mode='Markdown')
    bot.send_message(message.from_user.id, s)
    
    

# обрабатываем команду /Add_IPU, добавление счетчика в БД
@bot.message_handler(commands=['Add_IPU'])
def Add_IPU(message):
    # подключаемся к базе
    con = sl.connect('reports.db')
    # подготавливаем запрос
    sql = 'INSERT INTO Meter_Measure (id_meter, LS, Service, Number, value, LastUpdate, id_user) values(?, ?, ?, ?, ?, ?, ?)'
    # получаем дату и время
    now = datetime.now(timezone.utc)
    
    # формируем данные для запроса
    data = [
        (307130, '060076180', 'ХВС', '200148346', 115, str(now), str(message.from_user.username))
    ]
    # добавляем с помощью запроса данные
    with con:
        con.executemany(sql, data)
    # отправляем пользователю сообщение о том, что отчёт принят
    bot.send_message(message.from_user.id, 'Принято, спасибо!', parse_mode='Markdown')
                           

# обрабатываем команду /now
@bot.message_handler(commands=['now'])
def start(message):
    # подключаемся к базе
    con = sl.connect('reports.db')   
    # получаем сегодняшнюю дату
    now = datetime.now(timezone.utc)
    date = now.date()
    # пустая строка для будущих отчётов
    s = ''
     # работаем с базой
    with con:
        # выполняем запрос к базе
        data = con.execute('SELECT * FROM reports WHERE date = :Date;',{'Date': str(date)})
        # перебираем все результаты
        for row in data:
            # формируем строку в общем отчёте
            s = s + '*' + row[3] + '*' + ' → ' + row[4] + '\n\n'
    # если отчётов не было за сегодня
    if s == '':
        # формируем новое сообщение
        s = 'За сегодня ещё нет записей'
    # отправляем общий отчёт обратно в телеграм
    bot.send_message(message.from_user.id, s, parse_mode='Markdown')

# обрабатываем команду /yesterday
@bot.message_handler(commands=['yesterday'])
def start(message):
    # подключаемся к базе
    con = sl.connect('reports.db')
    # получаем вчерашнюю дату
    yesterday = datetime.today() - timedelta(days=1)
    y_date = yesterday.date()
    # пустая строка для будущих отчётов
    s = ''
    # работаем с базой
    with con:
        # выполняем запрос
        data = con.execute('SELECT * FROM reports WHERE date = :Date;',{'Date': str(y_date)})
        # смотрим на результат
        for row in data:
            # если результат пустой — ничего не делаем
            if row[0] == 0:
                pass
            # если вчера были какие-то отчёты
            else:
                # добавляем их в общий список отчётов 
                s = s + '*' + row[3] + '*' + ' → ' + row[4] + '\n\n'
    # если отчётов не было за вчера
    if s == '':
        # формируем новое сообщение
        s = 'За вчерашний день нет записей'
    # отправляем пользователю это новое сообщение 
    bot.send_message(message.from_user.id, s, parse_mode='Markdown')

# обрабатываем что пишет чел
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Подать показания':
        bot.send_message(message.from_user.id, "Введите номер лицевого счета");
        bot.register_next_step_handler(message,List_IPU)
        bot.register_next_step_handler(message, get_LS);
    else:
        bot.send_message(message.from_user.id, "dd");
'''
    if message.text.isdigit():
       bot.register_next_step_handler(message,List_IPU)
    else:
        bot.send_message(message.from_user.id, 'Неверный ввод.')
        bot.register_next_step_handler(message, get_age);
'''
def get_LS(message): #ищем ЛС
    
    LS = message.text;
    #тут ищем лс и выводим все ИПУ
    
    
    bot.send_message(message.from_user.id, "Выбирите Ваш счетчик");
    bot.register_next_step_handler(message, get_IPU);

def get_IPU(message): #Выводим счетчик
    
    IPU = message.text;
    bot.send_message(message.from_user.id, "Дальше");
    #bot.register_next_step_handler(message, get_sname);
    
        
        
'''    
    # подключаемся к базе
    con = sl.connect('reports.db')
    # подготавливаем запрос
    sql = 'INSERT INTO reports (datetime, date, id, name, text) values(?, ?, ?, ?, ?)'
    # получаем дату и время
    now = datetime.now(timezone.utc)
    # и просто дату
    date = now.date()
    # формируем данные для запроса
    data = [
        (str(now), str(date), str(message.from_user.id), str(message.from_user.username), str(message.text[:500]))
    ]
    # добавляем с помощью запроса данные
    with con:
        con.executemany(sql, data)
    # отправляем пользователю сообщение о том, что отчёт принят
    bot.send_message(message.from_user.id, 'Принято, спасибо!', parse_mode='Markdown')
'''
# создание клавиатуры
@bot.message_handler(commands=['keyboard'])
def handle_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("/start" )
    markup.add(item)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)
''' 
# перезапуск бота
@bot.message_handler(commands=["restart"]) #вызов по команде /restart; можно сделать и на кнопку
def restart(message):
	pid = str(os.getpid()) #получаем ProcessID запущенного бота
	restarter = open('restarter.bat', 'w') #открываем/создаем батник
	restarter.write('Taskkill /PID ' + pid + ' /F\nTIMEOUT /T 5 /NOBREAK\n cd D:\\WORK\\Telegramm \n D: \n python DB.py') #записываем скрипт в батник		
	restarter.close() #закрываем отредактированный батник
	os.system('D:\\WORK\\Telegramm\\restarter.bat') #запускаем наш батник
'''
# запускаем бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e: 
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')
