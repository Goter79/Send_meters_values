import json
import telebot;
from telebot.types import  ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from config import TOKEN;

database = Database()

bot = telebot.TeleBot(TOKEN)


@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    req = call.data.split('_')
    print('req')
    print(req)
    print('call.data')
    print(call.data) 

    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif 'pagination' in req[0]:
        json_string = json.loads(req[0])
        id_meter = json_string['idmeter']
        LS = json_string['LS']
        sqlTransaction = database.listColledjeForPage(tables='Meter_Measure', wheres=" where LS='"+LS+"' ", id_meter=id_meter)
        
        data = sqlTransaction
        countmass=data[1]       # Количество счетчиков в массиве
        count = data[2]   # Общее количество счетчиков в запросе
        


        print(data)

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Передать показания', callback_data='unseen'))
        
        if countmass==3:
            id_meter_next=data[0][2][2] # id_meter следующего счетчика
            id_meter_prev=data[0][0][2] # id_meter следующего счетчика
            Meter=data[0][1]            # счетчик
            page=Meter[1]          # номер счетчика в массиве data
            LS=Meter[3] 

            
            markup.add (InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_prev) +'"'+ "}"),
                        InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                        InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_next) +'"'+ "}"))

        elif countmass==2:  
            if data[0][0][0] == 0: #первый счетчик   
                Meter=data[0][0]            # счетчик
                page=Meter[1]          # номер счетчика в массиве data
                LS=Meter[3] 
                id_meter_next=data[0][1][2] # id_meter следующего счетчика
                markup.add (InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                            InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_next) +'"'+ "}"))
            else:                 #последний счетчик
                id_meter_prev=data[0][0][2] # id_meter предыдущего счетчика
                Meter=data[0][1]            # счетчик
                page=Meter[1]          # номер счетчика в массиве data
                LS=Meter[3] 
                markup.add (InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_prev) +'"'+ "}"),
                            InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))

        else: # один счетчик
            markup.add (InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))

        # if page == 1:
        #     markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
        #             InlineKeyboardButton(text=f'Вперёд --->',
        #                                     callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
        #                                         page + 1) + ",\"CountPage\":" + str(count) + "}"))
        # elif page == count:
        #     markup.add(InlineKeyboardButton(text=f'<--- Назад',
        #                                     callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
        #                                         page - 1) + ",\"CountPage\":" + str(count) + "}"),
        #             InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
        # else:
        #     markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page-1) + ",\"CountPage\":" + str(count) + "}"),
        #                 InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
        #                 InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))
            
        bot.edit_message_text(f'<b>Лицевой счет:{LS}</b>\n\n'
                                f'<b>Улуга:</b><i>{Meter[4]}</i>\n'
                                f'<b>Номер: ИПУ</b><i> {Meter[5]}</i>',
                                parse_mode="HTML",reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)



# обрабатываем старт бота
# @bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'])
def start(message):
    sqlTransaction = database.listColledjeForPage(tables='Meter_Measure', wheres=" where LS='100093000' ")
        
    #0 r,
    #1 rn, номер по порядку
    #d_meter,
    #LS,
    #Service,
    #Number,
    #value,
    #value_old,
    #LastUpdate,
    #id_user

    data = sqlTransaction
    print(data)
    id_meter_next=data[0][1][2] # id_meter следующего счетчика
    Meter=data[0][0]            # счетчик
    LS=Meter[3]
    
    page=Meter[1]          # номер счетчика в массиве data
    count = sqlTransaction[2]   # Общее количество счетчиков в запросе
    
    print(Meter)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Передать показания', callback_data='unseen'))
    markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
               InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_next) +'"'+ "}"))

    bot.send_message(message.from_user.id, f'<b>Лицевой счет:{LS}</b>\n\n'
                                    f'<b>Улуга:</b><i>{Meter[4]}</i>\n'
                                    f'<b>Номер: ИПУ</b><i> {Meter[5]}</i>',
                     parse_mode="HTML", reply_markup = markup)



# запускаем бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e: 
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌'+e)
