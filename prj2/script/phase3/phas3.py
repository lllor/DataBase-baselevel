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
	

def main():
	global db_terms, db_ads, db_dates, db_prices
	global cur_terms, cur_ads, cur_dates, cur_prices

	createDB()

	decision = str(input("1. Read from file.\n2. Read from input\n3. Qui\n Enter:\t"))

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
			while query != '':
				search(query,2)#type=2: print answer to termianl
				query = input("Enter your query: ").lower()
			print("Bye~")

		decision = str(input("1. Read from file.\n2. Read from input\n3. Qui\n Enter:\t"))



	cur_prices.close()
	db_prices.close()

	cur_dates.close()
	db_dates.close()

	cur_ads.close()
	db_ads.close()

	cur_terms.close()
	db_terms.close()




if __name__ == "__main__":
    main()