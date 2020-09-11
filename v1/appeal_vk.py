import requests
token = 'dell'
token2 = 'dell'
confirmation_token = 'dell'
version = 5.103

def stroki(adres,name):
    #Проверка количество строк в файле
    un = open(adres+"/"+name+".txt", "r")
    ston=0
    for line in un:
        ston += 1
    un.close()
    return ston
def pars(user_id):
    #Получение друзей ВК
    gg = []
    rrt=prof_close(user_id)
    if rrt == 0:
        response = requests.get('https://api.vk.com/method/friends.get',
            params={
                'access_token' : token2,
                'user_id': user_id,
                'order': 'name',
                'v': version
                    }
                                )
        data2 = response.json()
        gg.extend(data2['response']['items'])
        return gg
    else: return gg
def nick(user):
    #Получение имени и фамили | Ввод id
    response = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': token,
                                'user_ids': user,
                                'fields': 'nickname',
                                'v': version
                            }
                            )
    data45 = response.json()
    all = (data45['response'][0]['first_name']+" "+data45['response'][0]['last_name'])

    return all
def prof_close(user_ids):
    #Проверка закрыт ли профиль
    response = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': token2,
                                'user_ids': user_ids,
                                'order': 'name',
                                'v': version
                            }
                            )
    data_close = response.json()
<<<<<<< HEAD
    if data_close['response'][0].__len__() == 5:
        if data_close['response'][0]['is_closed'] != True:
            return 0
        else: return 1
    else: return 2
=======
    if data_close['response'][0]['is_closed'] == True:
        return 1
    else: return 0
>>>>>>> origin/master
