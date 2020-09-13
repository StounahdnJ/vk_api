import requests
import config

class Addition(object):
	
	def __init__(self):
		self.service_key = config.token['service_key'] # Токен сообщества
		self.token = config.token['token'] # Токен приложения
		self.version = config.token['version']  # Версия api

	def check_id(self,id): # Проверка на пользователя и открыт ли профиль, возврат {"code":bool,"mes":str,"id":int}
		id = id.replace('https://vk.com/', '').replace('http://vk.com/', '').replace('vk.com/', '')
		response = requests.get('https://api.vk.com/method/utils.resolveScreenName',params={'screen_name': id,'access_token': self.service_key,'v': self.version}).json()
		try:
			if response['response']['type']=="user": return {"code":True,"mes":"ok","id":int(response['response']['object_id'])}
			else: return {"code":False,"mes":"not user","id":None}
		except Exception as e:
			return {"code":False,"mes":"id","id":None}

	def view_friends(self,id): # Возвращает всех друзей пользователя, возврат {"code":bool,"mes":str,"id":int,"items":array}
		id = self.check_id(id)
		if id['code']:
			try:
				response=requests.get('https://api.vk.com/method/friends.get',params={'user_id': id['id'],'access_token': self.service_key,'v': self.version}).json()['response']['items']
				return {"code":True,"mes":'ok',"id":id['id'],"items":response}
			except Exception as e: pass
		return {"code":False,"mes":id['mes'],"id":id['id'],"items":None}

		