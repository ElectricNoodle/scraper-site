import time
import datetime
from flask import Flask
from flaskext.mysql import MySQL

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
	cursor.execute("SELECT * FROM items WHERE status = 'NEW' OR last_updated < %s",(interval.strftime('%Y-%m-%d %H:%M:%S')) );
	items = [dict(id=row[0], user=row[1],name=row[2], url=row[3], price= row[4],shipping= row[5],stock_no= row[6],status=row[7], last_updated = row[8], regex= row[9]) for row in cursor.fetchall()]
	return items;


def process_item(item):
	#Load the URL
	#Parse the HTML Tree
	#Regex it,
	#Update the Stock count
	#Update the Item Status to Updated
	#Store it back in the DB.


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