import json
import requests
import config
import controller
import threading

control = controller.Controller()
#Получение всех токенов и ключей ---------------------------------
version = config.token['version']  # Версия api
token = config.token['token'] # Токен сообщества
response = requests.get('https://api.vk.com/method/groups.getLongPollServer',params={'access_token': token,'group_id': 191524305,'v': version,}).json()['response']
data = {'ts':response['ts']} # Номер последнего события
key = response['key'] # Ключ запроса
server = response['server'] #Сервер для ожидания ответа
#-----------------------------------------------------------------

t1 = threading.Thread(target = control.update)
t1.start()
while True: # Проверка и обработка запросов
	data = requests.get(server,params={'act': 'a_check','key': key,'ts': data['ts'],'wait': 25,}).json()
	if data['updates']:   
		for mas in data['updates']:
			control.actionController(mas['object']['message']['from_id'],mas['object']['message']['text'])