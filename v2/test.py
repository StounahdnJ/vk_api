import User

user = User.UserClass(207681600)

#-----------Test Action-----------#

def test_new_action():
	user.new_action("new")
	user.new_action("res")
	user.new_action(234234)

def test_del_action():
	user.del_action()
	user.del_action()

def test_check_action():
	user.check_action()

def test_action():
	#Попытка создать два действия
	user.new_action("new")
	user.new_action("res")
	user.check_action()
	user.del_action()
	user.del_action()
	#Вывод действий, если их нет
	user.check_action()

#--------------------------------#

#----------Test Follow-----------#

def test_new_follow():
	#Попытка двух одинаковых
	user.new_follow("https://vk.com/romanm4")
	user.new_follow("https://vk.com/romanm4")
	user.new_follow("https://vk.com/id467073495")
	user.new_follow("https://vk.com/id467073495")
	#Ссылка на группу
	user.new_follow("https://vk.com/pikabu")
	#Сломанная ссылка
	user.new_follow("hcom/romanm4")
	user.new_follow("vk.com/romanфывфывфывm4")


def test_del_follow():
	pass

def test_update_follow():
	pass

def test_check_follow():
	pass

def test_follow():
	pass

#--------------------------------#