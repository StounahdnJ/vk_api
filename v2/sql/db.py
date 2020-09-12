import pymysql.cursors

class DataBase(object):
	def __init__(self):
		self.con = pymysql.connect('localhost', 'mysql','mysql', 'bot_vk')
		self.cursor = self.con.cursor()

	def request(self,sql):
		try:
			self.cursor.execute(sql)
		except Exception as e:
			pass
		self.con.commit()
		return self.cursor.fetchall()

DataBase = DataBase()