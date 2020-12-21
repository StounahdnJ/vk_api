import pymysql.cursors

class DataBase(object):
	# def __init__(self):

	def request(self,sql):
		try:
			self.con = pymysql.connect('localhost', 'ci17950_vk','7157725', 'ci17950_vk')
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