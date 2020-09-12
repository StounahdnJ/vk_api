from sql import db
import json
import model
import time
import requests
import config 

class UserClass(object):
	
	def __init__(self, id):
		self.id = id
		self.db = db.DataBase
		self.service_key = config.token['service_key'] # Токен сообщества
		self.token = config.token['token'] # Токен приложения
		self.version = 5.122  # Версия api
		self.keyboard = None
		self.action = None

	def message(self,message):
		requests.get('https://api.vk.com/method/messages.send',params={'access_token': self.token,'user_id': self.id,'message': message,'keyboard': self.keyboard,'random_id': 0,'v': self.version})

	#----------action methods----------#

	def new_action(self,action): # Создает новое пользовательское действие
		self.db.request("""INSERT INTO `request`(`user_id`, `action`, `date`) VALUES ({id},"{action}",{date})""".format(id=self.id,action=action,date=int(time.time())))

	def del_action(self): # Удаляет сохраненое действие пользователя
		self.db.request("""DELETE FROM `request` WHERE `user_id`={id}""".format(id=self.id))

	def check_action(self): # Проверяет наличия действия и присваевает action
		request = self.db.request("""SELECT `action`,`date` FROM `request` WHERE `user_id`={id}""".format(id=self.id))
		if request:
			if request[0][1] < int(time.time())+(60*60*24):
				self.action=request[0][0]
				return True
			else:
				self.del_action()
		return False

	#----------follow----------#
	def new_follow(self,follow_id): # Добавление пользователя в слежку, ответ {"code":True,"mes":"ok"}, при ошибке {"code":False,"mes":err_str}
		friends = model.view_friends(follow_id,self.service_key,self.version)
		if friends[0]:
			self.db.request("""INSERT INTO `user`(`user_id`, `follow_id`, `list`, `date`) VALUES ({id},{follow_id},"{list}",{date})""".format(id=self.id,follow_id=friends[2],list=json.dumps(friends[1]),date=int(time.time())))
			return {"code":True,"mes":"ok"}
		return {"code":False,"mes":friends[1]}

	def del_follow(self):
		pass

	def update_follow(self):
		pass

	def check_follow(self): # Вывод всех за кем следит {'code':True,'items':[[follow_id1,[array]],[follow_id2,[array]],[follow_id3,[array]]]}, при ошибке {'code':False,'items':[]}
		request = self.db.request("""SELECT `follow_id`,`list` FROM `user` WHERE `user_id`={id}""".format(id=self.id))
		if request:
			out=[]
			for friend in request:
				out.append([friend[0],json.loads(friend[1])])
			return {"code":True,"items":out}
		return {"code":False,"items":[]}
