import psycopg2

from . import app
from contextlib import closing

def getConnection():
	return psycopg2.connect("dbname=twitterfeed user=twitterfeed password=none port=2429")

def init_db():
	with closing(getConnection()) as db:
		with app.open_resource('schema.sql') as f:
			with closing(db.cursor()) as cursor:
				cursor.execute(f.read())
		db.commit()