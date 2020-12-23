import pymysql.cursors
import config

class DataBase(object):
	# def __init__(self):

	def request(self,sql):
		try:
			self.con = pymysql.connect(config.setting['host_dp'],config.setting['login_db'],config.setting['password_db'], config.setting['name_db'])
			self.cursor = self.con.cursor()
		except Exception as e:
			print('Error connect DataBase')
		try:
			self.cursor.execute(sql)
		except Exception as e:
			pass
		self.con.commit()
		otv = self.cursor.fetchall()
		self.cursor.close()
		return otv
		# return self.cursor.fetchall()
		

DataBase = DataBase()