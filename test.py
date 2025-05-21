import json
# req=['{"method":"pagination","LS":\"100093000\","idmeter":\"18995\"}']
# print('start\n ')
# print(req[0])
# print('\n next \n ')
# print(req[0][0])
# json_string = json.loads(req[0])
# print(json_string)
LS=1111
id_meter_next=99
count=1
page=2
callback_data="{\"method\":\"pagination\",\"LS\":" + str(LS) + ",\"idmeter\":" + str(id_meter_next) + "}"
callback_data="{\"method\":\"pagination\",\"NumberPage\":" +'"'+str(page-1) + ",\"CountPage\":" + str(count) + "}"
print(callback_data)


# Выбор ЛС
def SetLS(markup):
    # sqlTransaction = database.listColledjeForPage(tables='Meter_Measure', wheres=" where LS='100093000' ")
    markup.add(InlineKeyboardButton(text='1', callback_data='k1'),
               InlineKeyboardButton(text='2', callback_data='k2'),
               InlineKeyboardButton(text='3', callback_data='k3'))
    markup.add(InlineKeyboardButton(text='4', callback_data='k4'),
               InlineKeyboardButton(text='5', callback_data='k5'),
               InlineKeyboardButton(text='6', callback_data='k6'))
    markup.add(InlineKeyboardButton(text='7', callback_data='k7'),
               InlineKeyboardButton(text='8', callback_data='k8'),
               InlineKeyboardButton(text='9', callback_data='k9'))     