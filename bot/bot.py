import requests
import json
from random import randint as r_int
from random import shuffle
import urllib3
import people 
import time

"""
TODO:
finish the checkout procedure.
add proxy support.
"""

#sites that have a products.json file listed
file = open("shopify_std_db.txt", "r")
shopify_sites = [line[0:-1] for line in file]

def get_products (link, session):
	link = link + "/products.json"
	json_page = session.get(link, verify=False)
	products_json = json.loads(json_page.text)
	products = products_json["products"]
	return products

def keyword_search (products, keywords, partial_match=True, partial_verify=True, verify_threshold=0.6):
	for product in products:
		keys = 0
		for key in keywords:
			if key in product["title"]: keys += 1
		if keys == len(keywords): return product
		if keys/len(keywords) >= verify_threshold and partial_match:
			if partial_verify:
				if input ("item with name " + product['title'] + " is a " + str((keys/len(keywords)) * 100) + "% match, proceed [Y/n]") != "n":
					return product
			else:
				return product
	return None 

def find_id(product, sizes): #this way you can get a random size from a range of ones
	shuffle(sizes)
	for size in sizes:
		for variant in product["variants"]:
			if str(size) in variant["title"] and variant['available']:
				return [str(variant["id"]), size, str(variant['price'])]

def get_cart_link(link, id): return link + "/cart/" + id + ":1"

def add_to_cart (link, id):
	url = link + "/cart/add.js?quantity=1&id=" + id
	return session.get(url)

def get_shipping_info(link, postal_code, country, province, cookies):
	response = session.get(link, cookies=cookies, verify=False)
	options = json.loads(response.text)
	shipping_options = options["shipping_rates"][0]["name"].replace(' ', "%20")
	shipping_price = options["shipping_rates"][0]["price"]
	return "shopify-" + shipping_options+ "-" + shipping_price


#just proof-of-concept code
session = requests.session()
url = "https://" + input("enter site: ")

def shopify_order (info, link, kwords, sizes, proxy_info = None, delay = 1):
	if proxy_info: 
		pass #TODO
	else: 
		session = requests.session()
	product = None
	
	while not product:
		time.sleep(delay)
		products = get_products("https://" + link, session)
		product = keyword_search(products, kwords)

	(variant_id, product_size, product_price) = find_id(product, sizes)
	print("[*] ordering size", product_size, product['title'], "for", product_price, "usd")
	response = add_to_cart(link, variant_id)
	cookies = response.cookies
	get_shipping_info(link, info.postal_code, info.country, info.state, cookies)
