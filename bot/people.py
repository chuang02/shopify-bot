import json
import requests
import urllib3
from random import randint as r_int
from selenium import webdriver #gonna be used for most everyything but the actual bot.
"""
TODO:
somehow automate the creation of voip clients.
jig addresses
"""


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#email generator data
email_extensions = ["@gmail.com","@yahoo.com","@icloud.com","@gmail.com","@aol.com"]
transitions = [".","-","_",""]

file = open("babynames.txt", "r")
f_names = [line[0:-1].lower() for line in file]

file = open("surnames.txt", "r")
l_names = [line[0:-1] for line in file]

class person:
	def __init__ (self,card_number, cardholder, expiry_month, expiry_year, cvv):
		self.first_name = f_names[r_int(0,len(f_names) - 1)]
		self.last_name = l_names[r_int(0,len(l_names) - 1)]
		self.email = self.generate_email(self.first_name, self.last_name)
		(self.token, self.card) = self.get_shopify_payment_token(card_number, cardholder, expiry_month, expiry_year, cvv)
		"""
		self.phone_number = phone
		self.city = "charlotte"
		self.address = address
		self.postal_code = mail_code
		self.state = "North Carlolina"
		Self.Country = "United States"
		"""
	#generate payment token in advanced to save time.
	def get_shopify_payment_token(self, card_number, cardholder, expiry_month, expiry_year, cvv):
		link = "https://elb.deposit.shopifycs.com/sessions"
		payload = {
	    "credit_card": {
	        "number": card_number,
	        "name": cardholder,
	        "month": expiry_month,
	       "year": expiry_year,
	        "verification_value": cvv
			}
    	}
		r = requests.post(link, json=payload, verify=False)
		payment_token = json.loads(r.text)["id"]
		return (payment_token, payload['credit_card'])


	def generate_email(self, fname, lname):
		case = r_int(0,3)
		if (case == 0):
			username = fname + transitions [r_int (0, len (transitions) - 1)] + lname
		elif (case == 1):
			username = fname[0] + lname + transitions [r_int (0, len (transitions) - 1)] + str(r_int(0,99))		
		elif (case == 2):
			username = fname + lname + str(r_int(0,99))
		else:
			date = r_int(19,20)
			if (date == 20):
				date = str(date) + "0" + str(r_int(0,6))
			else:
				date = str(date) + str(r_int(84,99))
			username = fname + transitions [r_int (0, len (transitions) - 1)] + date
 
		if (" " in username): username.replace(" ", transitions [r_int (0, len (transitions) - 1)])
		return username + email_extensions [r_int (0, len (email_extensions) - 1)] 


