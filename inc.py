import MySQLdb


db=MySQLdb.Connect("127.0.0.1","root","","atm_database")
con=db.cursor()
def data():
	sql="SELECT * FROM `atm_users` "
	con.execute("UPDATE `atm_users` SET `amount`=13000")
	db.commit()
a=data()
db.close()