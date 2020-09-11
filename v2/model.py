import db
import time

db = db.DataBase

def new_action(id,action):
	db.request("""INSERT INTO `request`(`user_id`, `action`, `date`) VALUES ({id},"{action}",{date})""".format(id=id,action=action,date=int(time.time())))