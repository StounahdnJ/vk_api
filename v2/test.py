import User
import controller

user = User.UserClass(207681600)

#-----------Test Action-----------#

def test_new_action():
	print(user.new_action("new"))
	print(user.new_action("res"))
	print(user.new_action(234234))

def test_del_action():
	print(user.del_action())
	print(user.del_action())

def test_check_action():
	print(user.check_action())

def test_action():
	#Попытка создать два действия
	print(user.new_action("new"))
	print(user.new_action("res"))
	print(user.check_action())
	print(user.del_action())
	print(user.del_action())
	#Вывод действий, если их нет
	print(user.check_action())

#--------------------------------#

#----------Test Follow-----------#

def test_new_follow():
	#Попытка двух одинаковых
	print(user.new_follow("https://vk.com/romanm4"))
	print(user.new_follow("https://vk.com/romanm4"))
	print(user.new_follow("https://vk.com/id467073495"))
	print(user.new_follow("https://vk.com/id467073495"))
	#Ссылка на группу
	print(user.new_follow("https://vk.com/pikabu"))
	#Сломанная ссылка
	print(user.new_follow("hcom/romanm4"))
	print(user.new_follow("vk.com/romanфывфывфывm4"))


def test_del_follow():
	#Попытка двух одинаковых
	print(user.del_follow("https://vk.com/romanm4"))
	print(user.del_follow("https://vk.com/romanm4"))
	print(user.del_follow("https://vk.com/id467073495"))
	print(user.del_follow("https://vk.com/id467073495"))
	#Ссылка на группу
	print(user.del_follow("https://vk.com/pikabu"))
	#Сломанная ссылка
	print(user.del_follow("hcom/romanm4"))
	print(user.del_follow("vk.com/romanфывфывфывm4"))


def test_update_follow():
	print(user.update_follow("https://vk.com/romanm4"))
	print(user.update_follow("https://vk.com/id467073495"))
	#Ссылка на группу
	print(user.update_follow("https://vk.com/pikabu"))
	#Сломанная ссылка
	print(user.update_follow("hcom/romanm4"))
	print(user.update_follow("vk.com/romanфывфывфывm4"))


def test_get_follow():
	print(user.get_follow("https://vk.com/romanm4"))
	print(user.get_follow("https://vk.com/id467073495"))
	#Ссылка на группу
	print(user.get_follow("https://vk.com/pikabu"))
	#Сломанная ссылка
	print(user.get_follow("hcom/romanm4"))
	print(user.get_follow("vk.com/romanфывфывфывm4"))


#--------------------------------#

cont = controller.Controller()

cont.actionController(207681600,"Добавить")
cont.actionController(207681600,"https://vk.com/romanm4")