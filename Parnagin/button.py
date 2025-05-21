from telebot.types import  InlineKeyboardMarkup, InlineKeyboardButton


def button_whith_IPU(message,sqlTransaction):
        data = sqlTransaction
        countmass=data[1]       # Количество счетчиков в массиве
        count = data[2]   # Общее количество счетчиков в запросе
        
        # print(data)

        markup = InlineKeyboardMarkup()

        if countmass==3:
            id_meter_next=data[0][2][2] # id_meter следующего счетчика
            id_meter_curr=data[0][1][2] # id_meter текущего счетчика
            id_meter_prev=data[0][0][2] # id_meter предыду счетчика
            Meter=data[0][1]            # счетчик
            page=Meter[1]          # номер счетчика в массиве data
            LS=Meter[3] 

            markup.add(InlineKeyboardButton(text='Передать показания', callback_data="{\"method\":\"addVol\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(Meter[2]) +'"'+ "}"))
            markup.add (InlineKeyboardButton(text=f'⬅️ Назад', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_prev) +'"'+ "}"),
                        InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                        InlineKeyboardButton(text=f'Вперёд ➡️', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_next) +'"'+ "}"))

        elif countmass==2:  
            if data[0][0][0] == 0: #первый счетчик   
                Meter=data[0][0]            # счетчик
                page=Meter[1]          # номер счетчика в массиве data
                LS=Meter[3] 
                id_meter_next=data[0][1][2] # id_meter следующего счетчика
                markup.add(InlineKeyboardButton(text='Передать показания', callback_data="{\"method\":\"addVol\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(Meter[2]) +'"'+ "}"))
                markup.add (InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                            InlineKeyboardButton(text=f'Вперёд ➡️', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_next) +'"'+ "}"))
            else:                 #последний счетчик
                id_meter_prev=data[0][0][2] # id_meter предыдущего счетчика
                Meter=data[0][1]            # счетчик
                page=Meter[1]          # номер счетчика в массиве data
                LS=Meter[3] 
                markup.add(InlineKeyboardButton(text='Передать показания', callback_data="{\"method\":\"addVol\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(Meter[2]) +'"'+ "}"))
                markup.add (InlineKeyboardButton(text=f'⬅️ Назад', callback_data="{\"method\":\"pagination\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(id_meter_prev) +'"'+ "}"),
                            InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))

        else: # один счетчик
            Meter=data[0][0]            # счетчик
            markup.add(InlineKeyboardButton(text='Передать показания', callback_data="{\"method\":\"addVol\",\"LS\":"+'"'+  LS + '"'+",\"idmeter\":"+'"' + str(Meter[2]) +'"'+ "}"))
            markup.add (InlineKeyboardButton(text=f'1/1', callback_data=f' '))

        markup.add(InlineKeyboardButton(text='Выбрать другой лицевой', callback_data='SetLS'))            
        return markup, Meter
