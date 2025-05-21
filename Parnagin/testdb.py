import json
import sqlite3 as sl
from telebot.types import  ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from button import button_whith_IPU
from bot import bot # Импортируем объект бота

database = Database()
start_txt = 'Приветствуем Вас! Это официальный бот компании ООО ГУК-Краснодар. \n\n Тут Вы можете передать показания по своим индивидуальным приборам учета'

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    req = call.data.split('_')

    if 'addVol' in req[0]:
        bot.delete_message(call.message.chat.id, call.message.message_id)

        json_string = json.loads(req[0])
        id_meter = json_string['idmeter']
        LS = json_string['LS']
        sqlTransaction = database.listColledjeForPage(tables='Meter_Measure', wheres=" where LS='"+LS+"' ", id_meter=id_meter)
        tt=button_whith_IPU(call.message, sqlTransaction)
        markup=tt[0]
        Meter=tt[1]
        
        bot.send_message(call.message.chat.id,
                                        f'<code><b>Введите показания по выбранному ИПУ:</b>\n\n'
                                        f'<p>Лицевой счет:</p><p><b>{Meter[3]}</b></p>\n\n'
                                        f'Улуга                 :<b>{Meter[4]}</b>\n'
                                        f'Номер ИПУ             :<b>{Meter[5]}</b>\n'
                                        f'Предыдущие показания  :<b>{str(Meter[6])}</b>\n'
                                        f'Текущие показания     :<b>{str(Meter[7])}</b></code>',
                              parse_mode="HTML")
        # bot.send_message(call.message.chat.id, f'<b>Введите показания по ИПУ:</b>', parse_mode="HTML")
        # далее запускаем обработчик введенных показаний
         
    elif req[0] == 'SetLS':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        # markup = InlineKeyboardMarkup()
        # SetLS(markup)  
        bot.send_message(call.message.chat.id, f'<b>Введите Лицевой счет:</b>', parse_mode="HTML")
        bot.register_next_step_handler(call.message,Find_LS)
        # bot.send_message(call.message.from_user.id, "Введите номер лицевого счета");
        # bot.register_next_step_handler(call.message,Find_LS)
        


    elif 'pagination' in req[0]:
        json_string = json.loads(req[0])
        id_meter = json_string['idmeter']
        LS = json_string['LS']
        sqlTransaction = database.listColledjeForPage(tables='Meter_Measure', wheres=" where LS='"+LS+"' ", id_meter=id_meter)
        tt=button_whith_IPU(call.message, sqlTransaction)
        markup=tt[0]
        Meter=tt[1]
        
        bot.edit_message_text(
                                        f'Лицевой счет        :<b>{Meter[3]}</b>\n\n'
                                        f'Улуга               :<b>{Meter[4]}</b>\n'
                                        f'Номер ИПУ           :<b>{Meter[5]}</b>\n'
                                        f'Предыдущие показания:<b>{str(Meter[6])}</b>\n'
                                        f'Текущие показания   :<b>{str(Meter[7])}</b>',
                              parse_mode="HTML",reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)

# список ИПУ по ЛС  
def Find_LS(message):
    if message.text.isdigit():
        sqlTransaction = database.listColledjeForPage(tables='Meter_Measure', wheres=" where LS='"+message.text+"' ", id_meter='')

        if sqlTransaction[1] !=0:
            tt=button_whith_IPU(message, sqlTransaction)
            markup=tt[0]
            Meter=tt[1]

            bot.send_message(message.from_user.id,
                                        f'<code>Лицевой счет			:<b>{Meter[3]}</b>\n\n'
                                        f'Улуга					:<b>{Meter[4]}</b>\n'
                                        f'Номер ИПУ				:<b>{Meter[5]}</b>\n'
                                        f'Предыдущие показания	:<b>{str(Meter[6])}</b>\n'
                                        f'Текущие показания   	:<b>{str(Meter[7])}</b></code>',
                                        parse_mode="HTML", reply_markup = markup)
        else:
            bot.send_message(message.from_user.id, f'Не найден лицевой счет!!!\n\nВведите 9 цифр\n Введите номер лицевого счета')
            bot.register_next_step_handler(message,Find_LS)
    else:
        bot.send_message(message.from_user.id, f'Введите 9 цифр\n Введите номер лицевого счета')
        bot.register_next_step_handler(message,Find_LS)

# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    markup_reply = ReplyKeyboardMarkup(resize_keyboard=True).add(
        "Подать показания", "Помощь", "👀 Наш канал")
    bot.send_message(message.chat.id, start_txt, reply_markup=markup_reply)

@bot.message_handler(content_types=['text'])
def go_vvod(message):
    if message.text == "Подать показания": 
        bot.send_message(message.from_user.id, f'Введите номер лицевого счета\n Введите 9 цифр',)
        bot.register_next_step_handler(message,Find_LS)


# запускаем бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e: 
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌'+e)
