import appeal_vk
import json
import os
import vk_api
import requests
import time

confirmation_token = 'edeac87b'
version = 5.103
key = open("key.txt", "r")
token=key.read()
key.close()
key = open("key2.txt", "r")
token2=key.read()
key.close()
keyboard = {
"one_time": False,
"buttons":[[{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Список"
            },
            "color": "primary"
            },
            {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Добавить"
            },
            "color": "positive"
            },
            {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Помощь"
            },
            "color": "negative"
            }
            ]],
"inline": False
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

che = open("user/cache_add.txt", "w")
che.close()
che = open("user/cache_del.txt", "w")
che.close()
che = open("user/cache.txt", "w")
che.close()
che = open("sql/cache.txt", "w")
che.close()


def check_del(user_id):
    # Проверка друзей из файла
    if os.path.exists('sql/' + str(user_id) + ".txt") != True:
        return '1'
    data_pars = appeal_vk.pars(user_id)
    ston = 0
    f = 0
    ostal = ''
    ston = appeal_vk.stroki('sql', str(user_id))
    file = open('sql/' + str(user_id) + ".txt", "r")
    for line in file.readlines():
        line = line.replace('\n', '')
        good = 0
        g = 0
        while g < ston:
            for i in data_pars:
                if line == str(i):
                    good = good + 1
                    g = ston
            g += 1
        if good == 0:
            ostal = ostal + (line + ' ')
    file.close()
    return ostal

def check_add(user_id):
    if os.path.exists('sql/' + str(user_id) + ".txt") != True:
        return '1'
    data_pars = appeal_vk.pars(user_id)
    ston = 0
    ostal = ''
    ston = appeal_vk.stroki('sql', str(user_id))
    for i in data_pars:
        bad = 0
        line = 0
        g = 0
        file = open('sql/' + str(user_id) + ".txt", "r")
        for line in file.readlines():
            lineg = line.replace('\n', '')
            if lineg == str(i):
                bad += 1
                g = ston
        file.close()
        if bad == 0:
            ostal = (ostal + str(i) + ' ')
    file.close()
    return ostal

def mes(user_id, message):
    random_id = 0  # Отправка сообщений
    time.sleep(0.5)
    response = requests.get('https://api.vk.com/method/messages.send',
                            params={
                                'access_token': token,
                                'confirmation': confirmation_token,
                                'user_id': user_id,
                                'message': message,
                                'keyboard': keyboard,
                                'random_id': random_id,
                                'v': version
                            }
                            )
    print('Сообщение отправлено')

def prog1():
    # Проверка всех людей в базе и отправка сообщения тем кто его внес о удаление пользователя
    print('Идёт проверка людей')
    ston = appeal_vk.stroki('user', 'un')
    un = open("user/un.txt", "r")
    for line in un.readlines():
        time.sleep(4)
        # Проверка наличия пользователся в папке user и добавление его в папку 1/2
        line = line.replace('\n', '')
        if appeal_vk.prof_close(line)==0:
            un2 = open("user/" + line + ".txt", "r")
            for line2 in un2.readlines():
                line2 = line2.replace('\n', '')
                if appeal_vk.prof_close(line2)==0:
                    time.sleep(1)
                    out2 = check_add(line2)
                    out = check_del(line2)
                    frame = open("user/cache.txt", "w")
                    frame.write(out2.replace(' ', '\n'))
                    frame.close()
                    frame = open("user/cache.txt", "r")
                    for line_frame in frame.readlines():
                        line_frame = line_frame.replace('\n', '')
                        if line_frame != '':
                            vrem = open("user/cache_add.txt", "a")
                            vrem.write(str(line2) + '/' + str(line_frame) + '/' + str(line) + '\n')
                            vrem.close()
                    frame.close()
                    frame = open("user/cache.txt", "w")
                    frame.write(out.replace(' ', '\n'))
                    frame.close()
                    frame = open("user/cache.txt", "r")
                    for line_frame in frame.readlines():
                        line_frame = line_frame.replace('\n', '')
                        if line_frame != '':
                            vrem = open("user/cache_del.txt", "a")
                            vrem.write(str(line2) + '/' + str(line_frame) + '/' + str(line) + '\n')
                            vrem.close()
                    frame.close()
                #Добавить ввывод того что пользователь заблокирован в список (list)
            un2.close()
    un.close()
    che = open("user/cache_add.txt", "r")
    for line_c in che.readlines():
        line_c = line_c.replace('\n', '')
        indexs = [i for i, symb in enumerate(line_c) if symb == "/"]
        dlin = len(line_c)
        line_c1 = line_c[0:indexs[0]]
        line_c2 = line_c[indexs[0] + 1:indexs[1]]
        line_c3 = line_c[indexs[1] + 1:dlin]
        out = ''
        out = ("У " + '[id'+str(line_c1)+'|'+appeal_vk.nick(line_c1)+']' + " появился новый друг " + '[id'+str(line_c2)+'|'+appeal_vk.nick(line_c2)+']')
        mes(line_c3, out)
        gg = appeal_vk.pars(line_c1)
        file = open('sql/' + str(line_c1) + ".txt", "w")
        for i in gg:
            file.write(str(i) + '\n')
        file.close()
    che.close()
    che = open("user/cache_del.txt", "r")
    for line_c in che.readlines():
        line_c = line_c.replace('\n', '')
        indexs = [i for i, symb in enumerate(line_c) if symb == "/"]
        dlin = len(line_c)
        line_c1 = line_c[0:indexs[0]]
        line_c2 = line_c[indexs[0] + 1:indexs[1]]
        line_c3 = line_c[indexs[1] + 1:dlin]
        out = ''
        out = ("У " + '[id'+str(line_c1)+'|'+appeal_vk.nick(line_c1)+']' + " из друзей был удален " + '[id'+str(line_c2)+'|'+appeal_vk.nick(line_c2)+']')
        mes(line_c3, out)
        gg = appeal_vk.pars(line_c1)
        file = open('sql/' + str(line_c1) + ".txt", "w")
        for i in gg:
            file.write(str(i) + '\n')
        file.close()
    che.close()
    che = open("user/cache_add.txt", "w")
    che.close()
    che = open("user/cache_del.txt", "w")
    che.close()
    che = open("user/cache.txt", "w")
    che.close()
    print('Конец проверки людей в цикле')

def prog3(text):
    # Возвращает всех удаленых друзей
    out = check(text)
    name = ''
    if out == '':
        return 'Все остались'
    elif out == '1':
        name = 'Данный пользователь отсутствует в базе данных'
    else:
        list = out.split()
        for i in list:
            name = name + appeal_vk.nick(int(i)) + ' ' + 'https://vk.сom/id' + str(i)
    return name

def rentable(screen_name):
    if screen_name.isdigit():
        return 'Close'
    else:
        response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                    params={
                            'access_token': token,
                            'confirmation': confirmation_token,
                            'screen_name': screen_name,
                            'v': version
                            }
                                )
        data2 = response.json()
        if data2['response'].__len__() > 0:
            if data2['response']['type']=='user':
                if screen_name!=1:
                    return data2['response']['object_id']
                else: return 'Close'
            else: return 'Close'
        else:  return 'Close'

def prov():
    prov2 = 0
    oper = 0
    prog1()
    while True:
        time.sleep(2)
        prov = oper / 1000
        if int(prov) > prov2:
            print('Начало проверки')
            prov2 += 1
            prog1()
            print('Проверка пройдена ' + str(prov2))
        if oper > 240000:
            prov2=0
            oper = 0
        #print(oper)
        oper += 1