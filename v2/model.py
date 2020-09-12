import requests
def id_close(id,service_key,version): # Проверка на пользователя и открыт ли профиль
	id = id.replace('https://vk.com/', '').replace('http://vk.com/', '').replace('vk.com/', '')
	response = requests.get('https://api.vk.com/method/utils.resolveScreenName',params={'screen_name': id,'access_token': service_key,'v': version}).json()
	try:
		if response['response']['type']=="user": return [int(response['response']['object_id']),"ok"]
		else: return [False,"Был получен не пользователь"]
	except Exception as e:
		return [False,"id"]


def view_friends(id,service_key,version): # Возвращает всех друзей пользователя, формат [True,array], при ошибке [False,error_str]
	id = id_close(id,service_key,version)
	return [True,requests.get('https://api.vk.com/method/friends.get',params={'user_id': id[0],'access_token': service_key,'v': version}).json()['response']['items'],id[0]] if id[0] else id