import pymysql.cursors

class DataBase(object):
	def __init__(self, arg):
		con = pymysql.connect('localhost', 'root','7157725Rom', 'mpt')
    	cursor = con.cursor()
	
	def request(sql,date):
		pass        