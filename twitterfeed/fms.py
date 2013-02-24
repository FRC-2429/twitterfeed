

from . import database
from . import twitter

from contextlib import closing

import string

import psycopg2


def classifyTweet(tweet):
	resultArr = tweet.split()
	out = {}
	
	for index,elem in enumerate(resultArr):
		if index==0:
			out['EVENT'] = elem
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



def addTeam(conn,curs,year,name):
	curs.execute("SELECT id FROM events WHERE year = %s AND name = %s;", (year,name) )
	eventResult = curs.fetchone()
	if eventResult:
		return eventResult[0]

	print "Inserted event"
	curs.execute("INSERT INTO events (year,name) VALUES (%s,%s) RETURNING id;", (year,name))
	return curs.fetchone()[0]


def processTweets(last_id_recieved=294893974513123328):
	newTweets = twitter.getWholeTimeline(screen_name='frcfms',since_id=last_id_recieved)

	print newTweets

	with closing(database.getConnection()) as conn:
			with closing(conn.cursor()) as curs:

				for newTweet,tweetId in newTweets:
					newData = classifyTweet(newTweet)
					print(newData)
					

					eventId = addTeam(conn,curs,newData['YEAR'],newData['EVENT'])

					for team in (newData["RA"] + newData["BA"]):
						curs.execute("SELECT id from teams WHERE team_number = %s;", (team,))
						teamResult = curs.fetchone()
						if not teamResult:
							print "Inserted team"
							curs.execute("INSERT INTO teams (team_number) VALUES (%s) RETURNING id;",(team,))
							teamResult = curs.fetchone()

						teamId = teamResult[0]

						curs.execute("SELECT id FROM event_team_relationships WHERE event_id = %s AND team_id = %s;", (eventId,teamId))
						if not curs.fetchone():
							print "Inserting relation"
							curs.execute("INSERT INTO event_team_relationships (event_id,team_id) VALUES (%s,%s);", (eventId,teamId))

				conn.commit()

		



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
					curs.execute("UPDATE statustable SET currently_being_modified = TRUE;")
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



