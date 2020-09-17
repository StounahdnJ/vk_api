#Внешние библиотеки
import requests
#Мои файлы
import config
import User

class Controller(object):
	"""Класс для взаимодействия с User"""
	
	def __init__(self):
		self.methods={"new":lambda mes,bool=False:self.__new_followController(mes,bool),"list":lambda mes:self.__all_followController(),"del":lambda mes,bool=False:self.__del_followController(mes,bool)}
		self.command={'Добавить':{'action':"new",'mes':"😈Укажите ссылку на пользователя😈"},'Список':{'action':"list",'mes':""},'Удалить':{'action':"del",'mes':"Напишите номер кого хотите удалить"}}
		self.user = None


	def error(self,detailed=""):
		"""Вывод какой либо ошибки"""

		self.user.message(config.error['main']+config.error[detailed])
		self.__log("Пользователь {id}, делает ошибку ({detailed})".format(id=self.user.id,detailed=detailed))


	def __log(self,mes): #
		"""Метод для ведения логов"""

		print(mes)


	def __new_followController(self,mes,action=False):
		"""Добавляет нового пользователя в список"""

		if action: # Было ли выбрано это действие
			follow = self.user.new_follow(mes) # добавление в спиок
			if follow['code']:
				self.user.del_action()
				self.user.message(config.mes['ok new'])
				self.__log("Пользователь {id}, добавляет {mes} в свой список".format(id=self.user.id,mes=mes))
			else: 
				self.error(follow['mes'])
		else: 
			self.user.new_action("new")
			self.user.message(self.command[mes]['mes'])
			self.__log("Пользователь {id}, хочет сделать new".format(id=self.user.id))


	def __del_followController(self,mes,action=False):
		"""Удаляет пользователя из списка, по номеру из списка"""

		if action: # Было ли выбрано это действие
			follow = self.user.del_follow(number=mes,by_number=True)
			if follow['code']:
				self.user.del_action()
				self.user.message(config.mes['ok del'])
				self.__log("Пользователь {id}, удаляет из списка человека".format(id=self.user.id,mes=mes))
			else: 
				self.error(follow['mes'])
		else: 
			self.user.new_action("del")
			self.user.message(self.command[mes]['mes'])
			self.__all_followController()
			self.__log("Пользователь {id}, хочет сделать del".format(id=self.user.id))
	

	def __all_followController(self):
		"""Возвращает список за кем следит пользователь"""

		follows = self.user.get_follow()
		if follows['code']:
			out = ""
			num = 1
			for i in follows['items']:
				out+="{num}. {id}\n".format(num=num,id=user.get_name(i['id']))
				num+=1
			self.user.message(out)
		else: self.user.message(config.mes['list is empty'])
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