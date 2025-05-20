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