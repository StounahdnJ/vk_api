import mms_api
import vk_api
import json
import os
import requests
import appeal_vk
import time
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

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
                "label": "Удалить"
            },
            "color": "negative"
            }
            ]],
"inline": False
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
keyboard_com = {
"one_time": True,
"buttons":[[{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Отмена"
            },
            "color": "negative"
            }
            ]],
"inline": False
}
keyboard_com = json.dumps(keyboard_com, ensure_ascii=False).encode('utf-8')
keyboard_com = str(keyboard_com.decode('utf-8'))
add_t=["Добавить","добавить","add","Add"]
del_t=["Удалить","удалить","del","Del"]
help_t=["Помощь","помощь","help","Help"]
list_t=["Список","список","list","List"]
rep_t=["Репорт","репорт","rep","Rep"]
com=["add","del"]

def writeri(data, user_id, m_id):
    # Запись друзей в документ
    ston = 0
    #добавление в un был тут, возврат сюда
    good = 0
    ston = appeal_vk.stroki('user', str(m_id))
    u_file = open('user/' + str(m_id) + ".txt", "r")
    for line in u_file.readlines():
        # Проверка наличия проверяемого в личной папке usera и добавление его в папку 1/2
        line = line.replace('\n', '')
        g = 0
        while g < ston:
            if line == str(user_id):
                good = good + 1
                g = ston
            g += 1
    u_file.close()
    if good == 0:  # Проверка наличия проверяемого в личной папке usera и добавление его в папку 2/2
        u_file = open("user/" + str(m_id) + ".txt", "a")
        u_file.write(str(user_id) + '\n')
        u_file.close()
    good = 0
    ston = 0
    u_file.close()
    file = open('sql/' + str(user_id) + ".txt", "w")
    for i in data:
        file.write(str(i) + '\n')
        # file.write("vk.com/id") Доп команда для Вывод ссылки с именем и фамилией
        # f_l_name = nick(i) Доп команда для Вывод ссылки с именем и фамилией
        # file.write(str(i)+' '+f_l_name+'\n') Вывод ссылки с именем и фамилией D№№#
    file.close()

def pars_m():
    # Проверка наличия сообщений
    response = requests.get('https://api.vk.com/method/messages.getConversations',
                            params={
                                'access_token': token,
                                'confirmation': confirmation_token,
                                'filter': 'unread',
                                'v': version
                            }
                            )
    data = response.json()
    return data

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

def mes_com(user_id, message):
    random_id = 0  # Отправка сообщений
    time.sleep(0.5)
    response = requests.get('https://api.vk.com/method/messages.send',
                            params={
                                'access_token': token,
                                'confirmation': confirmation_token,
                                'user_id': user_id,
                                'message': message,
                                'keyboard': keyboard_com,
                                'random_id': random_id,
                                'v': version
                            }
                            )
    print('Сообщение отправлено')

def prog2(id, m_id):
    if os.path.isfile('user/'+str(m_id)+'.txt'):
        file = open('user/'+str(m_id)+'.txt', "r")
        og=0
        for line in file.readlines():
            line=line.replace('\n', '')
            if str(id)==line:
                og+=1
        file.close()
        if og==1:
            mes(m_id,"Пользователь уже добавлен в ваш список")
        else:
            if appeal_vk.prof_close(id)==0:
                gg = appeal_vk.pars(id)
                writeri(gg, id, m_id)
                mes(m_id, 'Пользователь добавлен')
            elif appeal_vk.prof_close(id)==1:
                mes(m_id, 'Профиль пользователя закрыт')
            else: mes(m_id, 'Пользователь удален или заблокирован')
    else:
        file = open('user/un.txt', "a")
        file.write(str(m_id)+'\n')
        file.close()
        file = open('user/'+str(m_id)+'.txt', "w")
        file.close()
        prog2(id,m_id)

def prog4(m_id):
    # Ввывод списка тех за кем следит человек
    file_ce = ("user/" + m_id + ".txt")
    if os.path.exists(file_ce):
        file = open("user/" + m_id + ".txt", "r")
        out = ''
        hhgg = 0
        for line in file.readlines():
            line = line.replace('\n', '')
            hhgg += 1
            if appeal_vk.prof_close(line)==2:
                line = (str(hhgg) + '. [id'+str(line)+'|'+appeal_vk.nick(line)+']' + ' (Пользователь заблокирован)' + '\n')
            elif appeal_vk.prof_close(line)==0:
                line = (str(hhgg) + '. [id'+str(line)+'|'+appeal_vk.nick(line)+']' + '\n')
            else: line = (str(hhgg) + '. [id'+str(line)+'|'+appeal_vk.nick(line)+']' + ' (Проверка недоступна)' + '\n')
            out = out + line
        file.close()
        if hhgg != 0:
            return out
        else:
            return ''
    else:
        return ''

def prog5(id, m_id):
    # Удаление пользователя из списка за кем следить
    file = open('user/' + str(m_id) + ".txt", "r")
    file_c = open('user/cache.txt', 'w')
    che = 0
    strok = appeal_vk.stroki("user", str(m_id))
    if id == 0:
        file.close()
        file_c.close()
        return "Вы указали недействительное число"
    else:
        if strok < id:
            file.close()
            file_c.close()
            return "Ошибка, вы указали склишком большое число"
        else:
            for line in file.readlines():
                line = line.replace('\n', '')
                che += 1
                if che != id:
                    file_c.write(line + '\n')
                else:
                    out_5 = line
            file.close()
            file_c.close()
            file_c = open('user/cache.txt', 'r')
            file = open('user/' + str(m_id) + ".txt", "w")
            for line in file_c.readlines():
                file.write(line)
            file_c.close()
            file.close()
            file_c = open('user/cache.txt', 'w')
            file_c.close()
            return ("Пользователь " +'[id'+str(int(out_5))+'|'+appeal_vk.nick(int(out_5))+']' + " был удален из вашего списка.")

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

def check2():
    #print('Проверка сообщений')
    data = pars_m()
    count_mes = data['response']['items']
    otv = 0
    text_id="Close1"
    text_id_dou='Close'
    for i in count_mes:
        #print('Сообщение есть')
        text = i['last_message']['text']
        id = i['last_message']['from_id']
        mes(id,"Бот был перезагружен повторите свою команду.")

def check():
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, 191524305)
    vk = vk_session.get_api()
    evn=mms_api.mms()
    check2()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print("Идет проверка сообщений")
            otv = 0
            text_id = "Close1"
            text_id_dou = 'Close'
            text = event.message.text.split(' ')
            id = event.message.peer_id
            if text == "":
                mes(id, "Я не могу ответить")
            text_с = text
            text_с[0] = text_с[0].replace('https://vk.com/', '')
            text_с[0] = text_с[0].replace('http://vk.com/', '')
            text_с[0] = text_с[0].replace('vk.com/', '')
            text_id_dou = rentable(text_с[0])
            if text_с.__len__() != 0:
                if text_с.__len__() > 1:
                    text_с[1] = text_с[1].replace('https://vk.com/', '')
                    text_с[1] = text_с[1].replace('http://vk.com/', '')
                    text_с[1] = text_с[1].replace('vk.com/', '')
                    text_id = rentable(text_с[1])
                else:
                    text_с[0] = text_с[0].replace('https://vk.com/', '')
                    text_с[0] = text_с[0].replace('http://vk.com/', '')
                    text_с[0] = text_с[0].replace('vk.com/', '')
                    text_id = rentable(text_с[0])
                if text_с[0] == 'Начать':
                    mes(id, 'Команды для бота:\n'
                            '●Добавить vk.com/id207681600 - Добавляет пользователся в список отслеживаемых\n'
                            '●Удалить номер по списку - Прекращение слежки за человеком\n'
                            '●Список - Показывает всех за кем вы следите\n'
                            '●Report текст - Задать вопрос')
                    evn.mms_add(id, "non")
                    otv = 1
                if text_с[0] in add_t:
                    if text_id != 'Close' and text_id != "Close1":
                        prog2(int(text_id), id)
                        out_l = prog4(str(id))
                        if out_l == '':
                            mes(id, "Список за кем вы следите пуст")
                        else:
                            out_l = ('Спискок за кем вы следите:\n' + out_l)
                        mes(id, out_l)
                        otv = 1
                    else:
                        mes(id, "Укажите ссылку на пользователя")
                        evn.mms_add(id, "add")
                        otv = 1
                if text_с[0] in help_t:
                    mes(id, 'Команды для бота:\n'
                            '●Добавить vk.com/id207681600 - Добавляет пользователся в список отслеживаемых\n'
                            '●Удалить номер по списку - Прекращение слежки за человеком\n'
                            '●Список - Показывает всех за кем вы следите\n'
                            '●Report текст - Задать вопрос')
                    evn.mms_add(id, "non")
                    otv = 1
                if text_с[0] in list_t:
                    out_l = prog4(str(id))
                    if out_l == '':
                        mes(id, "Список за кем вы следите пуст")
                    else:
                        out_l = ('Список за кем вы следите:\n' + out_l)
                    mes(id, out_l)
                    evn.mms_add(id, "non")
                    otv = 1
                if text_с[0] in del_t:
                    out_l = prog4(str(id))
                    if text_id != 'Close' and text_id != "Close1":
                        if text_с[1].isdigit():
                            out_d = prog5(int(text_с[1]), id)
                            mes(id, out_d)
                            if out_l == '':
                                mes(id, "Список за кем вы следите пуст")
                            else:
                                out_l = ('Список за кем вы следите:\n' + out_l)
                            mes(id, out_l)
                            otv = 1
                    else:
                        mes(id, "↓Укажите номер пользователя в списке↓")
                        out_l = ('Спискок за кем вы следите:\n' + out_l)
                        mes(id, out_l)
                        evn.mms_add(id, "del")
                        otv = 1
                if text_с[0] in rep_t:
                    i2 = text_с.__len__() - 1
                    report = ''
                    for i in range(i2):
                        i += 1
                        report = report + text_с[i] + ' '
                    report = (report + 'vk.com/id' + str(id))
                    che = open("user/report.txt", "a")
                    che.write(report + '\n')
                    che.close()
                    mes(id, ('Заявка ' + str(appeal_vk.stroki('user', 'report')) + ' принята.'))
                    mes(207681600, report)
                    evn.mms_add(id, "non")
                    otv = 1
                if otv == 0:
                    former_text=evn.mms_search(id)
                    if former_text == "add":
                        prog2(int(text_с[0]), id)
                        out_l = prog4(str(id))
                        if out_l == '':
                            mes(id, "Список за кем вы следите пуст")
                        else:
                            out_l = ('Спискок за кем вы следите:\n' + out_l)
                        mes(id, out_l)
                        otv = 1
                    if former_text == "del":
                        out_l = prog4(str(id))
                        out_d = prog5(int(text_с[0]), id)
                        mes(id, out_d)
                        if out_l == '':
                            mes(id, "Список за кем вы следите пуст")
                        else:
                            out_l = ('Список за кем вы следите:\n' + out_l)
                        mes(id, out_l)
                        otv = 1
                    if otv == 1:
                        mes(id, 'Неверная команда, напишите "help" чтобы узнать команды')

def test():
    vk_session = vk_api.VkApi(token=token)
    longpoll = VkBotLongPoll(vk_session, 191524305)
    vk = vk_session.get_api()
    evn=mms_api.mms()#Добавление класса для сообщений
    check2()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            otv=0
            text_с = event.message.text.split(' ')#Разбитие сообщения на слова
            id = event.message.peer_id #Получение id пользователя написавшего сообщение
            comand_pred = evn.mms_search(id)#Получение прежней команды
            if comand_pred in com: #Проверка на прежнию команду по типу add или del, если есть выполняется
                print(comand_pred)
                if comand_pred == "add": #Выполнение команды добавить пользователя
                    text_с[0] = text_с[0].replace('https://vk.com/', '')
                    text_с[0] = text_с[0].replace('http://vk.com/', '')
                    text_с[0] = text_с[0].replace('vk.com/', '')
                    text_id_dou = rentable(text_с[0])#Получение оригинального id
                    if text_id_dou!="Close":
                        prog2(int(text_id_dou), id)#Добавление пользователя
                        out_l = prog4(str(id))#Получение списка за кем следит пользователь
                        if out_l == '':
                            mes(id, "Список за кем вы следите пуст")
                        else:
                            out_l = ('…:::★☆★ ★☆★:::… \nСпискок за кем вы следите:\n' + out_l+'…:::★☆★ ★☆★:::… ')
                        mes(id, out_l)
                        evn.mms_add(id, "non")  # Отменяет значение последней команды
                    elif text_с[0]=="Отмена":
                        mes(id, '🔴Команда была отменена')
                        evn.mms_add(id, "non")
                    else: #Если ввели не цифру пишет ошибку и сбрасывает команду
                        mes(id, "🤗Неизвестное значение, повторите команду")
                        evn.mms_add(id, "non")
                if comand_pred == "del":#Удаления пользователя из списка по номеру
                    if text_с[0].isdigit():
                        out_d = prog5(int(text_с[0]), id)#Удаление пользователя
                        out_l = prog4(str(id))#Показ списка за кем следит пользователь
                        if out_l == '':
                            mes(id, out_d+"\nСписок за кем вы следите пуст")
                        else:
                            out_l = (out_d+"\n…:::★☆★ ★☆★:::… \nСписок за кем вы следите:\n" + out_l+'…:::★☆★ ★☆★:::… ')
                        mes(id, out_l)
                        evn.mms_add(id, "non")#Отменяет значение последней команды
                    elif text_с[0]=="Отмена":
                        mes(id, '🔴Команда была отменена')
                        evn.mms_add(id, "non")
                    else: #Если ввели не цифру пишет ошибку и сбрасывает команду
                        mes(id,"🤗Неизвестное значение, повторите команду")
                        evn.mms_add(id,"non")
            else: #Проверка новой команды
                if text_с[0] == 'Начать':
                    mes(id, 'Команды для бота:\n'
                            '●Добавить - Добавляет пользователся в список отслеживаемых\n'
                            '●Удалить - Прекращение слежки за человеком\n'
                            '●Список - Показывает всех за кем вы следите\n'
                            '●Report текст - Задать вопрос')
                    otv = 1
                if text_с[0] in add_t:
                    mes_com(id, "😈Укажите ссылку на пользователя😈")
                    evn.mms_add(id, "add")
                    otv = 1
                if text_с[0] in help_t:
                    mes(id, 'Команды для бота:\n'
                            '●Добавить - Добавляет пользователся в список отслеживаемых\n'
                            '●Удалить - Прекращение слежки за человеком\n'
                            '●Список - Показывает всех за кем вы следите\n'
                            '●Report текст - Задать вопрос')
                    otv = 1
                if text_с[0] in list_t:
                    out_l = prog4(str(id))
                    if out_l == '':
                        mes(id, "Список за кем вы следите пуст")
                    else:
                        out_l = ('…:::★☆★ ★☆★:::… \n'
                                 'Список за кем вы следите:\n' + out_l+'…:::★☆★ ★☆★:::… ')
                    mes(id, out_l)
                    otv = 1
                if text_с[0] in del_t:
                    out_l = prog4(str(id))
                    if out_l=='':
                        mes(id,"Вы не следите ни за кем🙀")
                    else:
                        out_l = ('↓Укажите номер пользователя в списке↓\n'
                                 'Спискок за кем вы следите:\n' + out_l)
                        evn.mms_add(id, "del")
                        mes_com(id, out_l)
                    otv = 1
                if text_с[0] in rep_t:
                    i2 = text_с.__len__() - 1
                    report = ''
                    for i in range(i2):
                        i += 1
                        report = report + text_с[i] + ' '
                    report = (report + 'vk.com/id' + str(id))
                    che = open("user/report.txt", "a")
                    che.write(report + '\n')
                    che.close()
                    mes(id, ('Заявка ' + str(appeal_vk.stroki('user', 'report')) + ' принята.'))
                    mes(207681600, report)
                    otv = 1
                if otv==0: #Если неверная команда
                    mes(id,"👾Неверная команда👾\n"
                           "→А кнопки для кого🤔←\n")

test()