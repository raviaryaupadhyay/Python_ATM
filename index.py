import MySQLdb
from flask import Flask
from flask import render_template
from flask import request 
app=Flask(__name__)
###########################################################################################################################################
###################################################         HOME         ##################################################################
###########################################################################################################################################

@app.route('/')
def handler():
	return render_template("index.html")

###########################################################################################################################################
###################################################      ATM NUMBER      ##################################################################
###########################################################################################################################################

@app.route('/atm_number',methods=['post'])
def atm_number():
	global atm_number,account_number,pin_number,first_name,last_name,amount,blocking
	atm_number=request.form['atm_number']
	db=MySQLdb.Connect("localhost","root","","atm_database")
	con=db.cursor()
	con.execute("SELECT * FROM `atm_users` WHERE `atm_number`=%s AND `blocking`=0",atm_number)
	data=con.fetchone()
	if (con.rowcount==1):
		if(atm_number==data[0]):
			account_number=data[1]
			pin_number=data[2]
			first_name=data[3]
			last_name=data[4]
			amount=data[5]
			return render_template("pin_auth.html",atm_number=atm_number)
		else:
			return render_template("error.html")
	else:
			return render_template("error.html")
	db.close()
###########################################################################################################################################
###################################################       PIN AUTH       ##################################################################
###########################################################################################################################################


@app.route('/pin_auth',methods=['post'])
def pin_auth():
	atm_pin=request.form['atm_pin']
	if(atm_pin==pin_number):
		return render_template("login.html",atm_number=atm_number)
	else:
		return render_template("error.html")

###########################################################################################################################################
###################################################        ERROR         ##################################################################
###########################################################################################################################################


@app.route('/error',methods=['post'])
def error():
		return render_template("index.html",atm_number=atm_number)

###########################################################################################################################################
####################################################       DEPOSITE      ##################################################################
###########################################################################################################################################

@app.route('/deposite_auth')
def deposite_auth():
		return render_template("deposite_auth.html",atm_number=atm_number)

                                   ###############################################################
                                   #############     DEPOSITE AUTENTICATION    ###################
                                   ###############################################################

@app.route('/deposite',methods=['post'])
def deposite():
		global auth_number,amount
		auth_number=request.form['auth_number']
		auth_password=request.form['auth_password']
		acount_number=request.form['account_number']
		amount_add=request.form['amount']
		try :
			amount_add=int(amount_add)
		except ValueError:
			amount_add=0
		amount=int(amount)+int(amount_add)
		db=MySQLdb.Connect("localhost","root","","atm_database")
		con=db.cursor()
		con.execute("SELECT * FROM `authentication_member` WHERE `auth_id`=%s",auth_number)
		data=con.fetchone()
		if (con.rowcount==1):
			if(auth_number==data[0]):
				if(auth_password==data[1]):
					global auth_name
					auth_name=data[2]###### use  pendding
					con.execute("UPDATE `atm_users` SET `amount`=%s WHERE atm_number=%s" ,(amount,atm_number))
					db.commit()
					db.rollback()
					return render_template("enquiry.html",first_name=first_name,last_name=last_name,atm_number=atm_number,account_number=account_number,amount=amount,auth_number=auth_number)
				else:
					return render_template("auth_error.html")
			else:
				return render_template("auth_error.html")
		else:
			return render_template("error.html")
		db.close()
###########################################################################################################################################
###################################################       WITHDRAWAL     ##################################################################
###########################################################################################################################################

@app.route('/withdrawal_page')
def withdrawal_page():
		return render_template("withdrawal.html",atm_number=atm_number)

                                   ###############################################################
                                   #############        WITHDRAWAL DETAILS     ###################
                                   ###############################################################

@app.route('/withdrawal',methods=['post'])
def withdrawal():
	global amount
	amount_withdrawal=request.form['amount_withdrawal']
	try :
		amount_withdrawal=int(amount_withdrawal)
	except ValueError:
		amount_withdrawal=0
	amount=int(amount)-int(amount_withdrawal)
	if (amount > 0):
		db=MySQLdb.Connect("localhost","root","","atm_database")
		con=db.cursor()
		con.execute("UPDATE `atm_users` SET `amount`=%s WHERE atm_number=%s" ,(amount,atm_number))
		db.commit()
		db.rollback()
		db.close()
		return render_template("enquiry.html",first_name=first_name,last_name=last_name,atm_number=atm_number,account_number=account_number,amount=amount)

	else:
		amount=int(amount)+int(amount_withdrawal)
		return render_template("error.html")

###########################################################################################################################################
###################################################       TRANSFER       ##################################################################
###########################################################################################################################################

@app.route('/transfer_page')
def transfer_page():
		return render_template("transfer.html",atm_number=atm_number)


                                   ###############################################################
                                   #############        TRANSFER DETAILS       ###################
                                   ###############################################################


@app.route('/transfer',methods=['post'])
def transfer():
		global transfer_account_number,transfer_amount,amount
		transfer_account_number=request.form['transfer_account_number']
		transfer_amount=request.form['transfer_amount']
		
		db=MySQLdb.Connect("localhost","root","","atm_database")
		con=db.cursor()
		con.execute("SELECT * FROM `atm_users` WHERE `atm_number`=%s AND `blocking`=0",atm_number)
		data=con.fetchone()
		transfered_amount=data[5]
	
		try :
			transfer_amount=int(transfer_amount)
		except ValueError:
			transfer_amount=0
		
		amount=int(amount)-int(transfer_amount)
		transfered_amount=int(transfered_amount)+int(transfer_amount)
		if (amount > 0):
			db=MySQLdb.Connect("localhost","root","","atm_database")
			con=db.cursor()
			con.execute("UPDATE `atm_users` SET `amount`=%s WHERE atm_number=%s" ,(amount,atm_number))
			con.execute("UPDATE `atm_users` SET `amount`=%s WHERE account_number=%s" ,(transfered_amount,transfer_account_number))
			db.commit()
			db.rollback()
			db.close()
			return render_template("enquiry.html",first_name=first_name,last_name=last_name,atm_number=atm_number,account_number=account_number,amount=amount)
		else:
			amount=int(amount)+int(transfer_amount)
			transfered_amount=int(transfered_amount)-int(transfer_amount)
			return render_template("error.html")

###########################################################################################################################################
###################################################       ENQUIRY        ##################################################################
###########################################################################################################################################

@app.route('/enquiry')
def enquiry():
		return render_template("enquiry.html",first_name=first_name,last_name=last_name,atm_number=atm_number,account_number=account_number,amount=amount)

###########################################################################################################################################
###################################################      PIN CHNAGE      ##################################################################
###########################################################################################################################################

@app.route('/pin_change_page')
def pin_change_page():
		return render_template("pin_change.html",atm_number=atm_number)

@app.route('/pin_change',methods=['post'])
def pin_change():
		old_pin=request.form['old_pin']
		new_pin=request.form['new_pin']
		re_new_pin=request.form['re_new_pin']
		if(old_pin==pin_number):
			if(new_pin==re_new_pin):
				if(new_pin==''):
					new_pin=old_pin
				db=MySQLdb.Connect("localhost","root","","atm_database")
				con=db.cursor()
				con.execute("UPDATE `atm_users` SET `pin_number`=%s WHERE atm_number=%s" ,(new_pin,atm_number))
				db.commit()
				db.rollback()
				db.close()
				return render_template("index.html")
			else:
				return render_template("index.html")

		else:
			db=MySQLdb.Connect("localhost","root","","atm_database")
			con=db.cursor()
			con.execute("UPDATE `atm_users` SET `blocking`=1 WHERE atm_number=%s" ,(atm_number))
			db.commit()
			db.rollback()
			db.close()
			return render_template("index.html")

###########################################################################################################################################
###################################################         MINI         ##################################################################
###########################################################################################################################################

@app.route('/mini')
def mini():
		return render_template("mini.html",atm_number=atm_number)

###########################################################################################################################################
###################################################       FAST CASH      ##################################################################
###########################################################################################################################################

@app.route('/fast_cash')
def fast_cash():
		return render_template("fast_cash.html",atm_number=atm_number)

###########################################################################################################################################
###################################################         OTHER        ##################################################################
###########################################################################################################################################

@app.route('/other')
def other():
		return render_template("other.html",atm_number=atm_number)
		
###########################################################################################################################################
###################################################        END        ###################################################################
###########################################################################################################################################

if __name__=='__main__':
	app.run(debug=True)