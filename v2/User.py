from sql import db
import json
import model
import time
import requests
import config 

class UserClass(model.Addition):
	
	def __init__(self, id):
		self.id = id
		self.db = db.DataBase
		self.service_key = config.token['service_key'] # Токен сообщества
		self.token = config.token['token'] # Токен приложения
		self.version = config.token['version']  # Версия api
		self.keyboard = None
		self.action = None

	def message(self,message): # Отправляет пользователю сообщение
		requests.get('https://api.vk.com/method/messages.send',params={'access_token': self.token,'user_id': self.id,'message': message,'keyboard': self.keyboard,'random_id': 0,'v': self.version})

	#----------action methods----------#

	def new_action(self,action): # Создает новое пользовательское действие, возврат None
		if not self.check_action()['code']: # Если нет action
			self.db.request("""INSERT INTO `request`(`user_id`, `action`, `date`) VALUES ({id},"{action}",{date})""".format(id=self.id,action=action,date=int(time.time())))

	def del_action(self): # Удаляет сохраненое действие пользователя, возврат None
		self.db.request("""DELETE FROM `request` WHERE `user_id`={id}""".format(id=self.id))

	def check_action(self): # Проверяет наличия действия и присваевает action, возврат {'code':bool,'action':action}
		request = self.db.request("""SELECT `action`,`date` FROM `request` WHERE `user_id`={id}""".format(id=self.id))
		if request: # Проверка на наличие ответа
			if request[0][1] < int(time.time())+(60*60*24):
				self.action=request[0][0]
				return {"code":True,"action":request[0][0]}
			else:
				self.del_action()
		return {"code":False,"action":None}

	#----------follow----------#

	def new_follow(self,follow_id): # Добавление пользователя в список для слежки, возврат {"code":bool,"mes":str}
		friends = self.view_friends(follow_id)
		follow_mas = []
		for mas in self.check_follow()['items']: # Проверка на наличие уже в списке для слежки
			follow_mas.append(mas['id'])
		if friends['code'] and (not friends['id'] in follow_mas):
			self.db.request("""INSERT INTO `user`(`user_id`, `follow_id`, `list`, `date`) VALUES ({id},{follow_id},"{list}",{date})""".format(id=self.id,follow_id=friends['id'],list=json.dumps(friends['items']),date=int(time.time())))
			return {"code":True,"mes":"ok"}
		return {"code":False,"mes":friends['mes']}

	def del_follow(self,follow_id): # Удаляет пользователя из списка для слежки
		id = self.check_id(follow_id)
		if id['code']:
			self.db.request("""DELETE FROM `user` WHERE `user_id`={id} AND `follow_id`={follow_id}""".format(id=self.id,follow_id=id['id']))
			return {"code":True,"mes":"ok"}
		return {"code":False,"mes":id['mes']}

	def update_follow(self,follow_id): # Обновляет друзей тех за кем следят
		friends = self.view_friends(follow_id)
		if friends['code']:
			self.db.request("""UPDATE `user` SET `list`="{list}" WHERE `user_id`={id} AND `follow_id`={follow_id}""".format(id=self.id,follow_id=friends['id'],list=json.dumps(friends['items'])))
			return {"code":True,"mes":"ok"}
		return {"code":False,"mes":friends['mes']}

	def check_follow(self,friend=False): # Вывод всех за кем следит, возврат {'code':bool,'items':[[follow_id,[array]],]}
		sql = {True:"""SELECT `follow_id`,`list` FROM `user` WHERE `user_id`={id}""",False:"""SELECT `follow_id` FROM `user` WHERE `user_id`={id}"""}
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
