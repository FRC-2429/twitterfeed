

from . import database
from . import twitter

from contextlib import closing

import string

import psycopg2


def clasifyTweet(tweet):
	resultArr = tweet.split()
	out = {}
	
	for index,elem in enumerate(resultArr):
		if index==0:
			out['Location'] = elem
		elif all(c in string.uppercase for c in elem):
			if elem == "RA" or elem == "BA":
				out[elem] = [int(num) for num in resultArr[index+1:index+4]]
			elif elem =="TY":
				out[elem] = resultArr[index+1]
			elif elem in "PQE":
				pass
			else:
				out[elem] = int(resultArr[index+1])

	if "RB" in out: #Red bridge points indicates 2012
		out['YEAR'] = 2012
	elif "RC" in out: #Red climb points indicates 2013
		out['YEAR'] = 2013

	return out




def proccessTweets(last_id_recieved):
	newTweets = twitter.getWholeTimeline(screen_name='frcfms',last_id_recieved=last_id_recieved)


def checkForUpdates():
	with closing(database.getConnection()) as conn:
		with closing(conn.cursor()) as curs:
			try:
				conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
				curs.execute("SELECT currently_being_modified FROM statustable;")
				result= curs.fetchone()[0]
				if (result == True):
					print "Currently being used"
					conn.rollback()
					return
				else:

					print "Ready for update"
					curs.execute("UPDATE statustable SET currently_being_modified = TRUE")
					conn.commit()
					print "Transaction sucess"

					conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
					curs.execute("SELECT last_id_recieved FROM statustable;")
					last_id_recieved = curs.fetchone()[0]
					print last_id_recieved





					curs.execute("UPDATE statustable SET currently_being_modified = FALSE")

					conn.commit()








			except psycopg2.extensions.TransactionRollbackError as e:
				print "Transaction failed"
				print e
				conn.rollback()



