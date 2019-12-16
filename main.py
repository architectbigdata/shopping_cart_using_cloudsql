import pymysql
import json
import random as r
from datetime import datetime
db_user = "root"
db_pass = "qwER12#$"
db_name = "shoppingcart"


def generate_uuid():
  '''Function generating random unique id of 5 digit'''
  random_string = ''
  random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  uuid_format = 5
  for n in range(uuid_format):
    random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
  return random_string


def add_user():
  user_id = generate_uuid()
  fname = input("Please enter your First name:  ")
  lname = input("Please enter your Last name:  ")
  fulladdress = input("Please enter your Address:  ")
  postalcode = input("Please enter your Postal Code:  ")
  phone = input("Please enter your Phone:  ")
  email = input("Please enter your email:  ")
  age = input("Please enter your age:  ")
  gender = input("Please enter your gender:  ")
  password = input("Please enter your password:  ")
  deliveryaddreesid = generate_uuid()
  city = input("Please enter your city:  ")
  state = input("Please enter your state:  ")
  country = input("Please enter your country:  ")

  cursor.execute("""INSERT into users VALUES ("%s", "%s", "%s", "%s", "%s","%s","%s","%s","%s","%s","%s")""" % (
    user_id, fname, lname, fulladdress, postalcode, phone, email, age, gender, password,datetime.now()))
  cursor.execute("""INSERT into deliveryaddress VALUES ("%s", "%s", "%s", "%s", "%s","%s","%s","%s")""" % (
    deliveryaddreesid, user_id, fulladdress, 'NULL', postalcode, city, state, country))

  db_conn.commit()
  print("Thanks for registration")
  return 1


def fetch_user_detail(pnumber):
  cursor.execute("""SELECT fname FROM users WHERE phone='%s'""" % (pnumber))
  rows = cursor.fetchone()
  if rows:
    print("Welcome" + " " + rows[0])
  return 1

def checkuser(pnumber):
#check whether user exists
	cursor.execute("""SELECT fname FROM users WHERE phone='%s'""" % (pnumber))
	rows = cursor.fetchone()
	if rows:
		return rows[0]
	else:
		return "NA"

def validation_check():
	option = input("Welcome to ShoppingCart, Please enter your Mobile Number:  ")
	if len(option) < 10 or len(option) > 10:
		print("Invalid Phone number")
		return 0,0
	else:
		c_val = checkuser(option)
		if c_val == "NA":
			t_val = add_user()
			return t_val,option
		else:
			print("Welcome " + c_val + ", please continue with your order")	
			return 1,option


def most_rated_product():
    cursor.execute("""SELECT PD.name,AVG(UR.rating) "AVG RATING" FROM userrating UR,products PD WHERE UR.product_id=PD.product_id GROUP BY PD.name ORDER BY 2 DESC LIMIT 2""")
    rows = cursor.fetchall()
    for k in rows:
        print(k[0])


def age_based():
    min_age=input("Please enter age range(min): ")
    max_age=input("Please enter age range(max): ")
    cursor.execute("""select C.Cat_Name, COUNT(*) Qty from users U, orders O, orderitem I, products P, categories C where (U.Age >= '%s' and U.Age <='%s') AND U.User_Id=O.LoginId AND O.Order_id=I.Order_id AND I.Product_id=P.Product_id AND P.Cat_Id=C.Cat_Id GROUP BY C.Cat_Name ORDER BY 2 DESC LIMIT 2""" %(min_age,max_age))
    rows=cursor.fetchall()
    for k in rows:
        print(k)

def gender_based():
    g_name=input("Please enter gender Female or Male: ")
    min_age=input("Please enter age range(min): ")
    max_age=input("Please enter age range(max): ")
    cursor.execute("""select C.Cat_Name, COUNT(*) Qty from users U, orders O, orderitem I, products P, categories C where (U.Age >= '%s' and U.Age <='%s') AND (U.gender='%s') AND U.User_Id=O.LoginId AND O.Order_id=I.Order_id AND I.Product_id=P.Product_id AND P.Cat_Id=C.Cat_Id GROUP BY C.Cat_Name ORDER BY 2 DESC LIMIT 2""" %(min_age,max_age,g_name))
    rows=cursor.fetchall()
    for k in rows:
        print(k)

def get_order(pnumber):
    cursor.execute("""select cat_name from categories""")
    rows = cursor.fetchall()
    cat_data=set()
    for i in rows:
        cat_data.update(i)
    print(cat_data)
    c_name = input("Please enter category name: ")
    cursor.execute("""SELECT cat_id FROM categories WHERE cat_name='%s'""" % (c_name))
    rows = cursor.fetchall()
    for i in rows:
        cursor.execute("""SELECT name FROM products WHERE cat_id='%s'""" % (i))
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    p_name = input("Please enter product name: ")
    cursor.execute("""SELECT product_id,name,description,price FROM products WHERE name='%s'""" % (p_name))
    rows= cursor.fetchone()
    productid = rows[0]
    itemid = generate_uuid()
    print("The price of the product is:  ",rows[3])
    resp = input("Please confirm for buying 'yes' : ")
    if resp.lower() == 'yes' or resp.lower() == 'y':
      orderid = generate_uuid()
      paymenttype = input("Please enter payment type(cash/card): ")
      orderdate = datetime.now()
      issameaspermanentaddress = input("Is delivery address same as permanent address(Yes/No) : ")
      if issameaspermanentaddress.lower() == 'yes' or issameaspermanentaddress.lower() == 'y':
        cursor.execute("""SELECT user_id FROM users WHERE phone='%s'""" % (pnumber))
        rows = cursor.fetchone()
        loginid = rows[0]
        cursor.execute("""SELECT deliveryaddreesid FROM deliveryaddress WHERE loginid='%s'""" % (loginid))
        rows = cursor.fetchone()
        deliveryaddressid = rows[0]
      if issameaspermanentaddress.lower() == 'no':
        deliveryaddressid = input("Enter the delivery address")
        cursor.execute("""SELECT user_id FROM users WHERE phone='%s'""" % (pnumber))
        rows = cursor.fetchone()
        loginid = rows[0]
      cursor.execute("""INSERT INTO orders values('%s','%s','%s','%s','%s','%s')""" %
                     (orderid,orderdate,loginid,issameaspermanentaddress,deliveryaddressid,paymenttype))
      cursor.execute("""INSERT INTO orderitem values('%s','%s','%s','%s')""" %
                     (itemid,orderid,productid,'1'))
      db_conn.commit()
      print("Thanks for Purchase")
      return 1
    else:
      return 0


def userrating():
  try:
    f_name = input("Enter the file name from which the userrating has to be entered: ")
    with open(f_name, 'r') as json_file:
      line = json_file.readline()
      while line:
        ratingid = generate_uuid()
        input_user = json.loads(line)
        user_id = str(input_user["user_id"])
        product_id = str(input_user["product_id"])
        rating = str(input_user["rating"])
        feedbackdate = str(input_user["feedbackdate"])
        cursor.execute("""insert into userrating values('%s','%s','%s','%s','%s')""" % (
          ratingid, user_id, product_id, rating, feedbackdate))
        db_conn.commit()
        line = json_file.readline()
  except Exception as e:
    print(e)


if __name__ == "__main__":
	try:
		db_conn = pymysql.connect(host='35.184.73.12', user=db_user, password=db_pass, db=db_name)
		cursor = db_conn.cursor()
		while True:
			print("Select the operations to perform:")
			print("1. Register User")
			print("2. Place Order")
			print("3. Most Rated Product")
			print("4, Top 2 Most Order Categories by Age Range")
			print("5, Top 2 Most Order Categories based on Gender")
			print("0. Exit")
			operation = input()
			if (operation == '1' or operation == 1):
				print("Selected: Register User")
				v_val, pnumber = validation_check()
			if (operation == '2' or operation == 2):
				print("Selected: Place Order")
				o_value = get_order(pnumber)
				if o_value == 1:
					print("Order Placed")
				elif o_value == 0:
					print("Order failed please retry")
			if (operation=='3' or operation==3):
				most_rated_product()
			if (operation=='4' or operation==4):
				age_based()
			if (operation=='5' or operation==3):
				gender_based()
			if (operation == '0' or operation == 0):
				print("Thank You")
#				cursor.close()
#        			db_conn.close()
				break
	except Exception as e:
		print(e)

	finally:
		cursor.close()
		db_conn.close()

