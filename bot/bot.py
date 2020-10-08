import requests
import json
from random import randint as r_int
from random import shuffle
import urllib3
import people 

#sites that have a products.json file listed
file = open("shopify_std_db.txt", "r")
shopify_sites = [line[0:-1] for line in file]

def get_products (link, session):
	link = link + "/products.json"
	json_page = session.get(link, verify=False)
	products_json = json.loads(json_page.text)
	products = products_json["products"]
	return products

def keyword_search (products, keywords, partial_match=False, partial_verify=False):
	for product in products:
		keys = len(keywords)
		for key in keywords:
			if key in product["title"]: keys -= 1
		if keys == 0: return product
	return None #TODO partial keyword verification support

def find_id(product, sizes): #this way you can get a random size from a range of ones
	shuffle(sizes)
	for size in sizes:
		for variant in product["variants"]:
			if str(size) in variant["title"] and variant['available']:
				return [str(variant["id"]), size, str(variant['price'])]

def get_cart_link(link, id): return link + "/cart/" + id + ":1"


session = requests.session()
url = "https://" + input("enter site: ")

product = keyword_search(get_products(url, session), "Nike WMNS Max III".split(" "))

id = find_id (product, list(range(7,15)))
cart_link = get_cart_link(url, id[0])

print ("product: ",  product['title'])
print ("\tprice", id[2])
print ("\tsize:",id[1])
print ("\tid:",id[0])
print ("\tcart link: ", cart_link)


"""
other sites:
https://www.yeezysupply.com, has a products.json file, but restricts access.
https://shop.ronniefieg.com, idk what is up with this one.
https://eflash-us.doverstreetmarket.com, idk either...
"""



