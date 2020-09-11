import json
import requests
import time
import config
#Получение всех токенов и ключей ---------------------------------
confirmation_token = config.token['confirmation_token'] # Токен сообщества
version = 5.122  # Версия api
token = config.token['token'] # Токен приложения
response = requests.get('https://api.vk.com/method/groups.getLongPollServer',params={'access_token': token,'group_id': 191524305,'v': version,}).json()['response']
data = {'ts':response['ts']} # Номер последнего события
key = response['key'] # Ключ запроса
server = response['server'] #Сервер для ожидания ответа
#---------------------------------------------------------------


def message(user_id, message, keyboard=None): # Отпрвка сообщение пользователю
    requests.get('https://api.vk.com/method/messages.send',params={'access_token': token,'confirmation': confirmation_token,'user_id': user_id,'message': message,'keyboard': keyboard,'random_id': 0,'v': version})
    print('Сообщение отправлено')


while True: # Проверка и обработка запросов
	data = requests.get(server,params={'act': 'a_check','key': key,'ts': data['ts'],'wait': 25,}).json()
	if data['updates']:
		print(data['updates'])      
		# for mas in data['updates']:
		# 	message(mas['object']['message']['from_id'],'Ес')