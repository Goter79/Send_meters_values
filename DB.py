# подключаем модуль для Телеграма
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
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
@bot.message_handler(commands=['Key'])
def Keybord(message):
	markup_inline = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text='📱Купить номер', callback_data='buynumber'),
        types.InlineKeyboardButton(text='💰Пополнить баланс', callback_data='balance')).add(
        types.InlineKeyboardButton(text='🌎Cтрана/Оператор', callback_data='country'),
        types.InlineKeyboardButton(text='🎉Мультисервис', callback_data='myltis')).add(
        types.InlineKeyboardButton(text='📚История покупок', callback_data='history')).add(
        types.InlineKeyboardButton(text='🎃Профиль', callback_data='prof'))	
	bot.send_message(
        message.chat.id,
        'Выбери что тебе интересно',
        reply_markup=markup_inline)
    

# обрабатываем команду /ListIPU, получение списка счетчиков
@bot.message_handler(commands=['List_IPU'])
def List_IPU(message):
    bot.send_message(message.from_user.id, 'Список ИПУ')
    # подключаемся к базе
    con = sl.connect('reports.db')   
    
    # пустая строка для данных
    s = ''
    sql="SELECT id_meter, LS, Number, value, value_old  FROM Meter_Measure"
    print(sql)
     # работаем с базой
     
    with con:
        # выполняем запрос к базе
        data = con.execute(sql).fetchall()
        # перебираем все результаты
        
        for row in data:
            # формируем строку в общем отчёте
             s += "id_meter:           {0}\nЛицевой счет: {1}\nНомер ИПУ:      {2}\nТек.показ-я:    {3}\nПред.показ-я: {4}\n\n".format(row[0], row[1], row[2], row[3], row[4])
             
            
    # если нет данных
    if s == '':
        # формируем новое сообщение
        s = 'Нет данных'
    # отправляем общий отчёт обратно в телеграм
    #bot.send_message(message.from_user.id, s, parse_mode='Markdown')
    bot.send_message(message.from_user.id, s)
    con.close()
    
# список ИПУ по ЛС
def Find_LS(message):
	if message.text.isdigit():
		#bot.send_message(message.from_user.id, "Список ИПУ по ЛС:"+message.text)
		# подключаемся к базе
		con = sl.connect('reports.db')   

		keyboard = types.InlineKeyboardMarkup() #Инлайн клавиатура
		# keyboard.row_width = 2	
		# пустая строка для данных
		s = ''
		LS=str(message.text) 
		sql="SELECT id_meter, LS, Number, value, value_old  FROM Meter_Measure Where LS='"+LS+"'"
		print(sql)
		# работаем с базой
		with con:
			# выполняем запрос к базе
			data = con.execute(sql).fetchall()
			for row in data:
				# формируем строку в общем отчёте
				s += "id_meter:           {0}\nЛицевой счет: {1}\nНомер ИПУ:      {2}\nТек.показ-я:    {3}\nПред.показ-я: {4}\n\n".format(row[0], row[1], row[2], row[3], row[4])
				#keyboard.add(InlineKeyboardButton(text=row[2], callback_data=row[2]))
				button=InlineKeyboardButton(text=row[2], callback_data=row[2])
				keyboard.add(button)
						
		# если нет данных
		if s == '':
			# формируем новое сообщение
			s = 'Нет данных'
		# отправляем общий отчёт обратно в телеграм
		
		bot.send_message(message.from_user.id, text="Список ИПУ по ЛС: "+message.text, reply_markup = keyboard)
		con.close()
	else:
		bot.send_message(message.from_user.id, 'Введите 9 цифр')
		bot.send_message(message.from_user.id, "Введите номер лицевого счета")
		bot.register_next_step_handler(message,Find_LS)
    

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
        con.commit()
    # отправляем пользователю сообщение о том, что отчёт принят
    bot.send_message(message.from_user.id, 'Принято, спасибо!', parse_mode='Markdown')

# обрабатываем что пишет чел
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Подать показания':
        bot.send_message(message.from_user.id, "Введите номер лицевого счета");
        bot.register_next_step_handler(message,Find_LS)
    else:
        bot.send_message(message.from_user.id, "Выбирите команду");

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
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌'+e)
