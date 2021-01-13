#Внешние библиотеки
import requests
import time
#Мои файлы
import config
import User
import datetime

class Controller(object):
	"""Класс для взаимодействия с User"""
	
	def __init__(self):
		self.methods={"new":lambda mes,bool=False:self.__new_followController(mes,bool),"list":lambda mes:self.__all_followController(),"del":lambda mes,bool=False:self.__del_followController(mes,bool)}
		self.command={'Добавить':{'action':"new",'mes':"😈Укажите ссылку на пользователя😈"},'Начать':{'action':"new",'mes':"😈Укажите ссылку на пользователя😈"},'Список':{'action':"list",'mes':""},'Удалить':{'action':"del",'mes':"Напишите номер кого хотите удалить"}}
		self.user = None


	def error(self,detailed="",action=False):
		"""Вывод какой либо ошибки"""

		self.user.message(config.error['main']+config.error[detailed],action)
		self.__log("Пользователь {id}, делает ошибку ({detailed})".format(id=self.user.id,detailed=detailed))


	def __log(self,mes): #
		"""Метод для ведения логов"""

		print(mes)

	def __list_follow(self):
		"""Создает список(перечесление) всех за кем следить пользователь"""

		follows = self.user.get_follow()
		if follows['code']:
			out = ""
			num = 1
			for i in follows['items']:
				out+="{num}. {id}\n".format(num=num,id=self.user.get_name(i['id'])['name'])
				num+=1
		else: out = config.mes['list is empty']
		return out

	def update(self):
		"""Метод для обновления новых и удаленных друзей"""

		user_loc = User.UserClass(1)
		mounths = ["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
		while True:
			for x in user_loc.all_user(): # Получение всех пользователей и проход по ним
				user = User.UserClass(x)
				follow = user.update_user()
				col = 0
				date = datetime.datetime.now()
				mes = config.mes['time'].format(year=date.year,day=date.day,month=mounths[date.month-1],min=date.strftime("%H:%M"))
				for i in follow['new_friends']: # Проверка и проход по новым друзьям тех за кем следит
					for friend in i['friends']: # Проход именно по тем кто появился
						mes += config.mes['new friend'].format(id=user.get_name(i['id'])['name'],friend=user.get_name(friend)['name'])+"\n"
						col+=1
					user.update_follow(i['id'])

				for i in follow['del_friends']: # Проверка и проход по удаленным друзьям тех за кем следит
					for friend in i['friends']: # Проход именно по тем кто появился
						mes += config.mes['del friend'].format(id=user.get_name(i['id'])['name'],friend=user.get_name(friend)['name'])+"\n"
						col+=1
					user.update_follow(i['id'])

				for i in follow['block']: # Проверка и проход по заблокированным людям из слежки
					mes += config.mes['close prof'].format(id=user.get_name(i)['name'])+"\n"
					user.del_follow(follow_id=i)
					col+=1
					user.update_follow(0)
				mes+="\n"+config.mes['dop']
				if col>0:
					user.message(mes)

			print('Сделал обновление')
			time.sleep(config.setting['update_time'])

	def __new_followController(self,mes,action=False):
		"""Добавляет нового пользователя в список"""

		if action: # Было ли выбрано это действие
			follow = self.user.new_follow(mes) # добавление в спиок
			if follow['code']:
				self.user.del_action()
				self.user.message(config.mes['ok new'].format(id=self.user.get_name(follow['id'])['name']))
				self.__log("Пользователь {id}, добавляет {mes} в свой список".format(id=self.user.id,mes=mes))
			else: 
				self.error(follow['mes'],action=True)
		else: 
			self.user.new_action("new")
			self.user.message(self.command[mes]['mes'],action=True)
			self.__log("Пользователь {id}, хочет сделать new".format(id=self.user.id))


	def __del_followController(self,mes,action=False):
		"""Удаляет пользователя из списка, по номеру из списка"""

		if action: # Было ли выбрано это действие
			follow = self.user.del_follow(number=mes,by_number=True)
			if follow['code']:
				self.user.del_action()
				self.user.message(config.mes['ok del'].format(id=self.user.get_name(follow['id'])['name']))
				self.__log("Пользователь {id}, удаляет из списка человека".format(id=self.user.id,mes=mes))
			else: 
				self.error(follow['mes'],action=True)
		else: 
			self.user.new_action("del")
			self.user.message((self.command[mes]['mes']+'\n'+self.__list_follow()),action=True)
			self.__log("Пользователь {id}, хочет сделать del".format(id=self.user.id))
	

	def __all_followController(self):
		"""Возвращает список за кем следит пользователь"""
		
		self.user.message(self.__list_follow())
		self.__log("Пользователь {id}, запросил список".format(id=self.user.id))


	def actionController(self,id,mes):
		"""Главный контроллер"""

		self.user = User.UserClass(id)
		action = self.user.check_action()

		if mes==config.command['Cancel']: # Отмена команд при ключевом слове
			self.user.del_action()
			self.user.message('Команда отменена')
			self.__log("Пользователь {id}, отменил команду".format(id=self.user.id))

		elif mes in self.command and not action['code']: # Выполнение команды если она есть в списке
			self.methods[self.command[mes]['action']](mes)

		elif action['code']: # Выполняет команду, ели она уже выбрана
			self.methods[action['action']](mes,True)

		else: # Неверный ввод
			self.error('not command')