from bsddb3 import db
import sys
import re

db_terms = None
db_ads = None
db_dates = None
db_prices = None

cur_terms = None
cur_ads = None
cur_dates = None
cur_prices = None
def createDB():
	global db_terms, db_ads, db_dates, db_prices
	global cur_terms, cur_ads, cur_dates, cur_prices

	db_terms = db.DB()
	db_terms.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
	db_terms.open("te.idx", None, db.DB_BTREE, db.DB_CREATE)

	db_ads = db.DB()
	db_ads.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
	db_ads.open("ad.idx", None, db.DB_HASH, db.DB_CREATE)

	db_dates = db.DB()
	db_dates.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
	db_dates.open("da.idx", None, db.DB_BTREE, db.DB_CREATE)

	db_prices = db.DB()
	db_prices.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
	db_prices.open("pr.idx", None, db.DB_BTREE, db.DB_CREATE)

def search(query,type):
	query = re.sub(r'\s+',' ',query)
	#print(query)
	keywords = ['date','cat','price','location']
	whitespce = [' ','\r','\t','\f','\v']
	query_temp = query
	date = re.findall(r"[.\s]*(date[>=<\s]+\d\d\d\d[\/]\d\d[\/]\d\d)[\s]*",query)
	if date:
		print("Date: ")
		print(date)
		for i in date:
			query_temp = query_temp.replace(i,' ')



	price = re.findall(r"[.\s]*(price[>=<\s]+\d*)[\s]*",query)
	if price:
		
		print("Price: ")
		print(price)
		for i in price:
			query_temp = query_temp.replace(i,' ')
	
	location = re.findall(r"[.\s]*(location[=\s]+[0-9a-zA-Z_-]*)[\s]*",query)
	if location:
		
		print("location: ")
		print(location)
		for i in location:
			query_temp = query_temp.replace(i,' ')
	
	cat = re.findall(r"[.\s]*(cat[=\s]+[0-9a-zA-Z_-]*)[\s]*",query)
	if cat:
		
		print("cat: ")
		print(cat)
		for i in cat:
			query_temp = query_temp.replace(i,' ')

	terms = query_temp.split()
	for term in terms:
		if term!='' and term != 'output=brief' and term != 'output=full':
			print(term)
		elif term == 'output=brief':
			output_type = 1
		elif term == 'output=full':
			output_type = 2
	#z = re.match("[.\s]*date[\s]*[<>=]?[\s]*\d{4}+[\/]\d{2}+[\/]{2}",query)
	#z = re.match("[.\s]*date[>=<]+\d{4}\d{2}\d{2}",query)
	
'''
	q = ''
	flag = 0 #use to determine whether this is a longterm condtion(ie. date <= 2018/11/05)
	count = 0
	whitespce = [' ','\r','\t','\f','\v']
	keywords = ['date','cat','price','location']
	keychar = ['=','<','>','<=','>=']

	for i in range(len(query)):
		if query[i] in whitespce and query[i-1] not in whitespce:
			q += '産'
		if query[i] in whitespce:
			continue
		else:
			q += query[i]
	
	conditions = q.split('産')
	result = {}
	#print(conditions)
	
	querys=[]
	for i in range(len(conditions)):
		if conditions[i] in keychar:
			querys.append(conditions[i-1]+conditions[i]+conditions[i+1])
			flag = 1
		elif flag == 1:
			flag = 0
			continue
		elif conditions[i] not in keywords:
			querys.append(conditions[i])

	#print(querys)

	for each in conditions:
		if each == "output=full":
			count -= 1
			continue
		elif each == "output=key":
			count -= 1
			continue

		elif re.match('\Adate',each):
			date(each[4:])
		elif re.match('\Aprice',each):
			price(each[4:])
		elif re.match('\Alocation',each):
			location(each[9:])
		else:

		elif re.match('[\s]+date[>=<\s]+\d{4}+[\/]+\d{2}+[\/]+\d{2}+[\s]+'):
			print()
'''


	












	

        


def main():
	global db_terms, db_ads, db_dates, db_prices
	global cur_terms, cur_ads, cur_dates, cur_prices

	#createDB()

	decision = str(input("1. Read from file.\n2. Read from input\n3. Quite\n Enter:\t"))

	while decision != '3':
		if decision == '1':
			from_file()
			input_filename = str(input("Please enter the inout file name: "))
			#output_filename = str(input("Please enter the output file name: "))
			input_file = open(input_filename,"r")
			output_file = open("output.txt","w")

			for eachline in input_file:
				search(eachline[:-1],1)#type=1:print answer to outputfile

			input_file.close()
			output_file.close()

		
		elif decision == '2':
			query = input("Enter your query: ").lower()
			type_out = input("Enter the output formate: ").lower()
			#while query != '':
			search(query,2)#type=2: print answer to termianl
				#query = input("Enter your query: ").lower()
			print("Bye~")

		decision = str(input("1. Read from file.\n2. Read from input\n3. Qui\n Enter:\t"))



	#cur_prices.close()
	#db_prices.close()

	#cur_dates.close()
	#db_dates.close()

	#cur_ads.close()
	#db_ads.close()

	#cur_terms.close()
	#db_terms.close()




if __name__ == "__main__":
    main()