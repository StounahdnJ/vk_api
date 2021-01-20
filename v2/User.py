# Внешние библиотеки
import json
import time
import requests
# Мои файлы
from sql import db
import config


class Addition(object):
    """Класс с доп.методами, позже можно вынести отсюда"""

    def __init__(self):
        self.service_key = config.token['service_key']  # Токен сообщества
        self.token = config.token['token']  # Токен приложения
        self.version = config.token['version']  # Версия api

    def get_name(self, id):
        """Возврат имени пользователя, принимает (ссылку), возврат {"code":bool,"mes":str,"id":int}"""

        id = id.replace('https://vk.com/', '').replace('http://vk.com/', '').replace('vk.com/', '') if isinstance(id, (
            str)) else 'id' + str(id)
        response = requests.get('https://api.vk.com/method/users.get',
                                params={'user_ids': id, 'access_token': self.service_key, 'lang': 'ru',
                                        'v': self.version}).json()
        try:
            return {'code': True, 'id': response['response'][0]['id'],
                    'name': '[id{id}|{name}]'.format(id=response['response'][0]['id'],
                                                     name=response['response'][0]['first_name'] + ' ' +
                                                          response['response'][0]['last_name'])}
        except Exception:
            return {'code': False, 'id': id, 'name': None}

    def check_id(self, id):  #
        """Проверка на пользователя и открыт ли профиль, принимает (ссылку), возврат {"code":bool,"mes":str,"id":int}"""

        id = id.replace('https://vk.com/', '').replace('http://vk.com/', '').replace('vk.com/', '') if isinstance(id, (
            str)) else 'id' + str(id)
        response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                                params={'screen_name': id, 'access_token': self.service_key, 'v': self.version}).json()
        try:
            if response['response']['type'] == "user":
                return {"code": True, "mes": "ok", "id": int(response['response']['object_id'])}
            else:
                return {"code": False, "mes": "not user", "id": None}
        except Exception:
            return {"code": False, "mes": "id", "id": None}

    def view_friends(self, id):
        """Возвращает всех друзей пользователя, принимает (ссылку), возврат {"code":bool,"mes":str,"id":int,"items":array}"""

        id = self.check_id(id)
        if id['code']:
            response = requests.get('https://api.vk.com/method/friends.get',
                                    params={'user_id': id['id'], 'access_token': self.service_key,
                                            'v': self.version}).json()
            try:
                return {"code": True, "mes": 'ok', "id": id['id'], "items": response['response']['items']}
            except Exception as e:
                return {"code": False, "mes": 'close prof', "id": id['id'], "items": None}
        return {"code": False, "mes": id['mes'], "id": id['id'], "items": None}


class UserClass(Addition):

    def __init__(self, id):

        # -----------Параметры для VK_api-----------#
        self.service_key = config.token['service_key']  # Токен сообщества
        self.token = config.token['token']  # Токен приложения
        self.version = config.token['version']  # Версия api
        # ---------------------------------#

        # -----------Настройки-----------#
        self.id = id  # id Пользователя
        self.db = db.DataBase  # Подключение к базе данных
        self.update_time = config.setting['update_time']  # Время для обновления друзей
        request = self.db.request(
            """SELECT `update_date`, `registration_date`,`active` FROM `detailed_user` WHERE `user_id`={id}""".format(
                id=id))
        self.detailed = {'update_date': request[0][0], 'registration_date': request[0][1],
                         'active': request[0][2]} if request else None  # Получение активности пользователя
        self.db.request(
            """INSERT INTO `detailed_user`(`user_id`, `update_date`, `registration_date`, `active`) VALUES ({id},{date},{date},0)""".format(
                id=id,
                date=int(time.time()))) if not self.detailed else 1  # Создание нового профиля пользователя, ели его нет
        # ---------------------------------#

        # -----------Клавиатуры-----------#
        self.keyboard = json.dumps({"one_time": True, "buttons": [[
            {"action": {"type": "text", "payload": "{\"button\": \"1\"}", "label": "Список"}, "color": "primary"},
            {"action": {"type": "text", "payload": "{\"button\": \"2\"}", "label": "Добавить"}, "color": "positive"},
            {"action": {"type": "text", "payload": "{\"button\": \"3\"}", "label": "Удалить"}, "color": "negative"}
        ]], "inline": False}, ensure_ascii=False).encode('utf-8')  # Стандартная клавиатура
        self.keyboard_action = json.dumps({"buttons": [[
            {"action": {"type": "text", "payload": "{\"button\": \"1\"}", "label": "Отмена"}, "color": "negative"}
        ]], "inline": True}, ensure_ascii=False).encode('utf-8')  # Клавиатура для действий

    # ---------------------------------#

    def message(self, message, action=False):
        """Отправляет пользователю сообщение"""

        if action:
            response = requests.get('https://api.vk.com/method/messages.send',
                                    params={'access_token': self.token, 'user_id': self.id, 'message': message,
                                            'keyboard': self.keyboard_action, 'random_id': 0, 'v': self.version}).json()
        else:
            response = requests.get('https://api.vk.com/method/messages.send',
                                    params={'access_token': self.token, 'user_id': self.id, 'message': message,
                                            'keyboard': self.keyboard, 'random_id': 0, 'v': self.version}).json()
        if "error" in response and response["error"]["error_code"] == 901: return False
        return True

    def all_user(self):
        """Возвращает всех активных пользователей"""

        request = self.db.request("""SELECT DISTINCT `user_id` FROM `detailed_user`""")
        if request:
            return [i[0] for i in request]

    # ----------action methods----------#

    def new_action(self, action):
        """Создает новое пользовательское действие, принимает (строку), возврат None"""

        if not self.check_action()['code']:  # Если нет action
            self.db.request(
                """INSERT INTO `request`(`user_id`, `action`, `date`) VALUES ({id},"{action}",{date})""".format(
                    id=self.id, action=action, date=int(time.time())))

    def del_action(self):
        """Удаляет сохраненое действие пользователя, возврат None"""

        self.db.request("""DELETE FROM `request` WHERE `user_id`={id}""".format(id=self.id))

    def check_action(self):
        """Проверяет наличия действия и присваевает action, возврат {'code':bool,'action':action}"""

        request = self.db.request("""SELECT `action`,`date` FROM `request` WHERE `user_id`={id}""".format(id=self.id))
        if request:  # Проверка на наличие ответа
            if request[0][1] < int(time.time()) + (60 * 60 * 24):
                return {"code": True, "action": request[0][0]}
            else:
                self.del_action()
        return {"code": False, "action": None}

    # -------------follow-------------#

    def new_follow(self, follow_id):
        """Добавление пользователя в список для слежки, принимает (ссылку), возврат {"code":bool,"mes":str,"id":id}"""

        friends = self.view_friends(follow_id)

        if friends['id'] in [mas['id'] for mas in
                             self.get_follow()['items']]:  # Проверка на наличие уже в списке для слежки
            return {"code": False, "mes": 'already'}

        if friends['code']:
            self.db.request(
                """INSERT INTO `user`(`user_id`, `follow_id`, `list`,`date`) VALUES ({id},{follow_id},"{list}",{date})""".format(
                    id=self.id, follow_id=friends['id'], list=json.dumps(friends['items']), date=int(time.time())))
            self.db.request("""UPDATE `detailed_user` SET `active`=1 WHERE `user_id`={id}""".format(id=self.id))
            return {"code": True, "mes": "ok", "id": friends['id']}

        return {"code": False, "mes": friends['mes'], "id": None}

    def del_follow(self, follow_id=None, number=None, by_number=False):
        """Удаляет пользователя из списка для слежки, принимает (ссылку,число,bool) через номер по списку или ссылке, возврат {"code":bool,"mes":str,"id":id}"""

        if by_number:  # Если удаление по номеру

            try:  # Проверка на наличие в списке и на число
                id = {'code': True, 'mes': 'ok', 'id': self.get_follow()['items'][int(number) - 1]['id']}
            except Exception as e:
                id = {'code': False, 'mes': 'not number', 'id': None}

        else:

            try:  # Получение id через ссылку на пользователя
                id = self.check_id(follow_id)
            except Exception as e:
                id = {'code': False, 'mes': 'id', 'id': None}

        if id['code']:  # Если пользователь есть, удалить из списка
            self.db.request("""DELETE FROM `user` WHERE `user_id`={id} AND `follow_id`={follow_id}""".format(id=self.id,
                                                                                                             follow_id=
                                                                                                             id['id']))
            self.db.request("""UPDATE `detailed_user` SET `active`=0 WHERE `user_id`={id}""".format(id=self.id)) if not \
                self.get_follow()['code'] else 1
            return {"code": True, "mes": "ok", "id": id['id']}

        return {"code": False, "mes": id['mes'], "id": id['id']}

    def update_follow(self, follow_id):
        """Обновляет друзей тех за кем следят, принимает (ссылку), возврат {'code':bool,'mes':str}"""

        friends = self.view_friends(follow_id)
        if friends['code']:
            self.db.request(
                """UPDATE `user` SET `list`="{list}" WHERE `user_id`={id} AND `follow_id`={follow_id}""".format(
                    id=self.id, follow_id=friends['id'], list=json.dumps(friends['items'])))
            self.db.request(
                """UPDATE `detailed_user` SET `update_date`={date} WHERE `user_id`={id}""".format(id=self.id, date=int(
                    time.time())))

            return {"code": True, "mes": "ok"}
        self.db.request("""UPDATE `detailed_user` SET `update_date`={date} WHERE `user_id`={id}""".format(id=self.id,
                                                                                                          date=int(
                                                                                                              time.time())))
        return {"code": False, "mes": friends['mes']}

    def get_follow(self, friend=False):
        """Вывод всех за кем следит, возврат {'code':bool,'items':[[follow_id,[array]],]}"""

        sql = {True: """SELECT `follow_id`,`list` FROM `user` WHERE `user_id`={id}""",
               False: """SELECT `follow_id` FROM `user` WHERE `user_id`={id}"""}
        request = self.db.request(sql[friend].format(id=self.id))
        if request:
            out = []
            if friend:
                for friends in request:
                    out.append({"id": friends[0], "friends": json.loads(friends[1])})
            else:
                for friends in request:
                    out.append({"id": friends[0]})
            return {"code": True, "items": out}
        return {"code": False, "items": []}

    def update_user(self):
        """Возвращает все изменения друзей, возврат {'new_friends':{'id':id,'friends':array},'del_friends':{'id':id,'friends':array},'block':array}"""

        # if not self.detailed['active'] or self.detailed['update_date']+self.update_time > int(time.time()):
        # 	return {'code':False,'new_friends':[],'del_friends':[],'block':[]}
        old_follow = [[mas['id'], mas['friends']] for mas in
                      self.get_follow(friend=True)['items']]  # Получение старых списков друзей
        new_follow = []  # Массив для новых полных списков друзей
        dell = []  # Массив для удаленных друзей
        add = []  # Массив для новых друзей
        block = []  # Массив тех, кого нельзя проверить

        for x in old_follow:  # Получения обновления по всем спискам друзей
            friend = self.view_friends(x[0])
            if friend['code']:
                new_follow.append([x[0], friend['items'], True])
            else:
                new_follow.append([x[0], [], False])
                block.append(x[0])

        for g in range(len(old_follow)):  # Поиск удаленных id
            if new_follow[g][2]:
                mas = [None if i in new_follow[g][1] else i for i in old_follow[g][1]]
                vrem = {'id': old_follow[g][0], 'friends': [value for value in mas if value is not None]}
                dell.append(vrem) if vrem['friends'] else 1

        for g in range(len(old_follow)):  # Поиск новых id
            if new_follow[g][2]:
                mas = [None if i in old_follow[g][1] else i for i in new_follow[g][1]]
                vrem = {'id': new_follow[g][0], 'friends': [value for value in mas if value is not None]}
                add.append(vrem) if vrem['friends'] else 1

        return {'code': True, 'new_friends': add, 'del_friends': dell, 'block': block}
