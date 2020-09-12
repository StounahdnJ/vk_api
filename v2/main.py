import json
import requests
import time
import config
import User
#Получение всех токенов и ключей ---------------------------------
version = config.token['version']  # Версия api
token = config.token['token'] # Токен сообщества
response = requests.get('https://api.vk.com/method/groups.getLongPollServer',params={'access_token': token,'group_id': 191524305,'v': version,}).json()['response']
data = {'ts':response['ts']} # Номер последнего события
key = response['key'] # Ключ запроса
server = response['server'] #Сервер для ожидания ответа
#-----------------------------------------------------------------
#Используемые переменные------------------------------------------
methods={"new":lambda mes:new_followController(mes),None:lambda mes:error(mes),}
command={'Добавить':['new','😈Укажите ссылку на пользователя😈'],} # action и сообщение
command_out={'Список':lambda:all_followController()} # Моментальный действия, без доп ввода
#-----------------------------------------------------------------

def error(mes,detailed=""): # Отправка пользователю ошибки
	user.message(config.error['main']+config.error[detailed])
	print("Пользователь {id}, вводит неверную команду {mes}".format(id=user.id,mes=mes))

def all_followController(): # Вывод всех за кем следит пользователь
	reply = user.check_follow()
	if reply['code']:
		out=''
		for follow in reply['items']:
			out+='{id}\n'.format(id=follow[0])
	else: out=config.mes['list is empty']
	user.message(out)
	print("Пользователь {id}, запрашивает список".format(id=user.id))

def new_followController(mes): # Обработка добавление слежки
	reply = user.new_follow(mes)
	if reply['code']:
		user.message("Добавленно")
		user.del_action()
		print("Пользователь {id}, добавляет {mes} в список".format(id=user.id,mes=mes))
	else: error(mes,reply['mes'])

def Controller(mes):
	if user.check_action()['code']: # Если действие уже выбрано, сделать его
		methods[user.action](mes)
	elif mes in command: # Добавить новое действие
		user.new_action(command[mes][0])
		user.message(command[mes][1])
		print("Пользователь {id}, хочет сделать {command}".format(id=user.id,command=command[mes][0]))
	elif mes in command_out: # Моментальный действия, без доп ввода
		command_out[mes]()
	else: error(mes)
	 	


while True: # Проверка и обработка запросов
	data = requests.get(server,params={'act': 'a_check','key': key,'ts': data['ts'],'wait': 25,}).json()
	if data['updates']:   
		for mas in data['updates']:
			user = User.UserClass(mas['object']['message']['from_id'])
			Controller(mas['object']['message']['text'])