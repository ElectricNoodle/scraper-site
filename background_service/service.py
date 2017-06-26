import time
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'squirrels like to play in the park.'

mysql = MySQL()
#SAUSAGE
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'scraper'
app.config['MYSQL_DATABASE_PASSWORD'] = '42Ir&fdds'
app.config['MYSQL_DATABASE_DB'] = 'scraper'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

SECONDS = 10
CHUNK_SIZE = 20;

#Get time so we run an update every x seconds.
starttime=time.time()




def get_items(num_items):
	print "Getting up to " + str(num_items) + ".."

def process(items):
	print "Processing.."

def store(items):
	print "Storing.."


def main():
	items_to_check = get_items(CHUNK_SIZE)
	processed_items = process(items_to_check)
	store(processed_items)


while True:
  main();
  time.sleep(SECONDS - ((time.time() - starttime) % SECONDS))