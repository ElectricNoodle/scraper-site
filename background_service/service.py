import time
import datetime
import microdata
from flask import Flask
from flaskext.mysql import MySQL
import nltk   
import requests
import urllib2 
from random import randint
from fake_useragent import UserAgent
import re
from pprint import pprint
from extruct.jsonld import JsonLdExtractor
app = Flask(__name__)
app.secret_key = 'squirrels like to play in the park.'


#SAUSAGE
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'scraper'
app.config['MYSQL_DATABASE_PASSWORD'] = '42Ir&fdds'
app.config['MYSQL_DATABASE_DB'] = 'scraper'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

ua = UserAgent()

conn = mysql.connect()
cursor = conn.cursor()

SECONDS = 10

#In minutes:
UPDATE_PERIOD = 10
CHUNK_SIZE = 20;

#Get time so we run an update every x seconds.
starttime=time.time()


def get_items(num_items):

	print "Getting up to " + str(num_items) + ".."
	interval = datetime.datetime.now() - datetime.timedelta(minutes=UPDATE_PERIOD)
	print (interval.strftime('%Y-%m-%d %H:%M:%S'))
	cursor.execute("SELECT * FROM items WHERE status = 'NEW' OR last_updated < %s ",(interval.strftime('%Y-%m-%d %H:%M:%S')) );
	items = [dict(id=row[0], name=row[1],url=row[2], asin=row[3], old_price= row[4], price=row[5], shipping=row[6], variation=row[7], old_stock = row[8],stock= row[9], status = row[10]) for row in cursor.fetchall()]
	return items;


def process_item(item):
	#print item;
	agent = ua.random
	#https://stackoverflow.com/questions/5620263/using-an-http-proxy-python
	#print item['url'] 
	secs = randint(10,30) 
	print "Sleeping for.." + str(secs) + "\n" 
        time.sleep(secs)
	req = urllib2.Request(item['url'], headers={ 'User-Agent': agent })
	html = urllib2.urlopen(req).read()
	jslde = JsonLdExtractor()
	data = jslde.extract(html)
	pprint(data[0])	
		
	try:
		print cursor.execute("UPDATE scraper.items SET stock_no=%s, name=%s, status=%s WHERE id=%s ",(stock,(info.group(1) + " " + info.group(2)),"PROCESSED", item['id']))
		conn.commit()
		print cursor._last_executed
	except:     
		print "ERRROR :( "
		conn.rollback()
	#Load the URL
	#Parse the HTML Tree
	#Regex it,
	#Update the Stock count
	#Update the Item Status to Updated
	#Store it back in the


def process(items):
	print "Processing.."
	for item in items:
		process_item(item)



def main():
	items_to_check = get_items(CHUNK_SIZE)
	processed_items = process(items_to_check)



while True:
  main();
  time.sleep(SECONDS - ((time.time() - starttime) % SECONDS))
