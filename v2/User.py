#Внешние библиотеки
import json
import time
import requests
#Мои файлы
from sql import db
import config 

class Addition(object):
	"""Класс с доп.методами, позже можно вынести отсюда"""

	def __init__(self):
		self.service_key = config.token['service_key'] # Токен сообщества
		self.token = config.token['token'] # Токен приложения
		self.version = config.token['version']  # Версия api

	def check_id(self,id): # 
		"""Проверка на пользователя и открыт ли профиль, возврат {"code":bool,"mes":str,"id":int}"""

		id = id.replace('https://vk.com/', '').replace('http://vk.com/', '').replace('vk.com/', '') if id is int else 'id'+str(id)
		response = requests.get('https://api.vk.com/method/utils.resolveScreenName',params={'screen_name': id,'access_token': self.service_key,'v': self.version}).json()
		try:
			if response['response']['type']=="user": return {"code":True,"mes":"ok","id":int(response['response']['object_id'])}
			else: return {"code":False,"mes":"not user","id":None}
		except Exception as e:
			return {"code":False,"mes":"id","id":None}

	def view_friends(self,id):
		"""Возвращает всех друзей пользователя, возврат {"code":bool,"mes":str,"id":int,"items":array}"""

		id = self.check_id(id)
		if id['code']:
			response=requests.get('https://api.vk.com/method/friends.get',params={'user_id': id['id'],'access_token': self.service_key,'v': self.version}).json()
			try:
				return {"code":True,"mes":'ok',"id":id['id'],"items":response['response']['items']}
			except Exception as e: 
				return {"code":False,"mes":'close prof',"id":id['id'],"items":None}
		return {"code":False,"mes":id['mes'],"id":id['id'],"items":None}


class UserClass(Addition):
	
	def __init__(self, id):
		self.id = id
		self.db = db.DataBase
		self.service_key = config.token['service_key'] # Токен сообщества
		self.token = config.token['token'] # Токен приложения
		self.version = config.token['version']  # Версия api
		self.keyboard = None
		self.action = None


	def message(self,message):
		"""Отправляет пользователю сообщение"""

		requests.get('https://api.vk.com/method/messages.send',params={'access_token': self.token,'user_id': self.id,'message': message,'keyboard': self.keyboard,'random_id': 0,'v': self.version})

	#----------action methods----------#

	def new_action(self,action):
		"""Создает новое пользовательское действие, возврат None"""

		if not self.check_action()['code']: # Если нет action
			self.db.request("""INSERT INTO `request`(`user_id`, `action`, `date`) VALUES ({id},"{action}",{date})""".format(id=self.id,action=action,date=int(time.time())))


	def del_action(self):
		"""Удаляет сохраненое действие пользователя, возврат None"""

		self.db.request("""DELETE FROM `request` WHERE `user_id`={id}""".format(id=self.id))


	def check_action(self):
		"""Проверяет наличия действия и присваевает action, возврат {'code':bool,'action':action}"""

		request = self.db.request("""SELECT `action`,`date` FROM `request` WHERE `user_id`={id}""".format(id=self.id))
		if request: # Проверка на наличие ответа
			if request[0][1] < int(time.time())+(60*60*24):
				self.action=request[0][0]
				return {"code":True,"action":request[0][0]}
			else:
				self.del_action()
		return {"code":False,"action":None}

	#-------------follow-------------#

	def new_follow(self,follow_id):
		"""Добавление пользователя в список для слежки, возврат {"code":bool,"mes":str}"""

		friends = self.view_friends(follow_id)

		if friends['id'] in [mas['id'] for mas in self.get_follow()['items']]: # Проверка на наличие уже в списке для слежки
			return {"code":False,"mes":'already'}

		if friends['code']:
			self.db.request("""INSERT INTO `user`(`user_id`, `follow_id`, `list`, `date`) VALUES ({id},{follow_id},"{list}",{date})""".format(id=self.id,follow_id=friends['id'],list=json.dumps(friends['items']),date=int(time.time())))
			return {"code":True,"mes":"ok"}

		return {"code":False,"mes":friends['mes']}


	def del_follow(self,follow_id=None,number=None,by_number=False):
		"""Удаляет пользователя из списка для слежки, через номер по списку или ссылке"""
		
		if by_number: # Если удаление по номеру
 
			try: # Проверка на наличие в списке и на число
				id = {'code':True,'mes':'ok','id': self.get_follow()['items'][int(number)-1]['id']}
			except Exception as e:
				id = {'code':False,'mes':'not number', 'id': None}

		else: 

			try: # Получение id через ссылку на пользователя
				id = self.check_id(follow_id)
			except Exception as e:
				id = {'code':False,'mes':'id', 'id': None}

		if id['code']: # Если пользователь есть, удалить из списка

			self.db.request("""DELETE FROM `user` WHERE `user_id`={id} AND `follow_id`={follow_id}""".format(id=self.id,follow_id=id['id']))
			return {"code":True,"mes":"ok"}

		return {"code":False,"mes":id['mes']}


	def update_follow(self,follow_id):
		"""Обновляет друзей тех за кем следят"""

		friends = self.view_friends(follow_id)
		if friends['code']:
			self.db.request("""UPDATE `user` SET `list`="{list}" WHERE `user_id`={id} AND `follow_id`={follow_id}""".format(id=self.id,follow_id=friends['id'],list=json.dumps(friends['items'])))
			return {"code":True,"mes":"ok"}
		return {"code":False,"mes":friends['mes']}


	def get_follow(self,friend=False): 
		"""Вывод всех за кем следит, возврат {'code':bool,'items':[[follow_id,[array]],]}"""

		sql = {True:"""SELECT `follow_id`,`list` FROM `user` WHERE `user_id`={id}""", False:"""SELECT `follow_id` FROM `user` WHERE `user_id`={id}"""}
		request = self.db.request(sql[friend].format(id=self.id))
		if request: 
			out=[]
			#-----------ВОЗМОЖНО НАДО ИСПРАВИТЬ ОБРАБОТКУ ИСКЛЮЧЕНИЙ-----------
			for friend in request:
				try:
					out.append({"id":friend[0],"friends":json.loads(friend[1])})
				except Exception as e:
					out.append({"id":friend[0]})
			#------------------------------------------------------------------
			return {"code":True,"items":out}
		return {"code":False,"items":[]}

	def update(self):
		"""Возвращает все изменения друзей, возврат {'new_friends':{'id':id,'friends':array},'del_friends':{'id':id,'friends':array},'block':array}"""

		all_follow = self.get_follow(friend=True)
		old_follow = [[mas['id'],mas['friends']] for mas in all_follow['items']] # Получение старых списков друзей
		new_follow = [] # Массив для новых полных списков друзей
		dell = [] # Массив для удаленных друзей
		add = [] # Массив для новых друзей
		block = [] # Массив тех, кого нельзя проверить

		for x in old_follow: # Получения обновления по всем спискам друзей
			friend = self.view_friends(x[0])
			if friend['code']: new_follow.append([x[0],friend['items'],True]) 
			else: 
				new_follow.append([x[0],[],False]) 
				block.append([x[0]])

		for g in range(len(old_follow)): # Поиск удаленных id
			if new_follow[g][2]:
				mas = [None if i in new_follow[g][1] else i for i in old_follow[g][1]]
				dell.append({'id':old_follow[g][0],'friends':[value for value in mas if value != None]})

		for g in range(len(old_follow)): # Поиск новых id
			if new_follow[g][2]:
				mas = [None if i in old_follow[g][1] else i for i in new_follow[g][1]]
				add.append({'id':new_follow[g][0],'friends':[value for value in mas if value != None]})

		return {'new_friends':add,'del_friends':dell,'block':block}