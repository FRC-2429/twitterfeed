

from . import database
from . import twitter
from . import blueallaince

from contextlib import closing

import string

import psycopg2


import simplejson as json


def classifyTweet(tweet):
	resultArr = tweet.split()
	out = {}
	
	for index,elem in enumerate(resultArr):
		if index==0:
			out['EVENT'] = elem
		elif all(c in string.uppercase for c in elem):
			if elem == "TST":
				continue
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


def chunks(l,n):
	return (l[i:i+n] for i in range(0,len(l),n))

class FMS(object):

	def __init__(self):
		self.conn = database.getConnection()
		self.curs = self.conn.cursor()

	def addBlueAllainceData(self):
		regionalList = blueallaince.getRegionalsForYear(2012)
		matchList = (match for regional in regionalList for match in blueallaince.getMatchesForRegional(regional))
		
		matches =  (match for chunk in chunks(list(matchList),100) for match in blueallaince.getDetailsForMatches(chunk))

		for m in matches:
			self.curs.execute("INSERT INTO raw_blueallaince_match (key,data) VALUES (%s,%s);", (m["key"],json.dumps(m)))

		self.conn.commit()




	def addEvent(self,year,name):
		self.curs.execute("SELECT id FROM events WHERE year = %s AND name = %s;", (year,name) )
		eventResult = self.curs.fetchone()
		if eventResult:
			return eventResult[0]

		print "Inserted event"
		self.curs.execute("INSERT INTO events (year,name) VALUES (%s,%s) RETURNING id;", (year,name))
		return self.curs.fetchone()[0]


	def addTeam(self,eventId,teamNumber):
		self.curs.execute("SELECT id from teams WHERE team_number = %s;", (teamNumber,))
		teamResult = self.curs.fetchone()
		if teamResult:
			return teamResult[0]

		print "Inserted team"
		self.curs.execute("INSERT INTO teams (team_number) VALUES (%s) RETURNING id;",(teamNumber,))
		return self.curs.fetchone()[0]

	def addRelationship(self,eventId,teamId):
		self.curs.execute("SELECT id FROM event_team_relationships WHERE event_id = %s AND team_id = %s;", (eventId,teamId))
		if not self.curs.fetchone():
			print "Inserting relation"
			self.curs.execute("INSERT INTO event_team_relationships (event_id,team_id) VALUES (%s,%s);", (eventId,teamId))

	def processTweets(self,last_id_recieved):
		newTweets = twitter.getWholeTimeline(screen_name='frcfms',since_id=last_id_recieved)

		print newTweets

		for newTweet,tweetId in newTweets:
			newData = classifyTweet(newTweet)
			print(newData)		

			eventId = self.addEvent(newData['YEAR'],newData['EVENT'])

			for teamNumber in (newData["RA"] + newData["BA"]):
				teamId = self.addTeam(eventId,teamNumber)
				self.addRelationship(eventId,teamId)
							
		self.conn.commit()

		newTweets.append( (None,last_id_recieved )) #if newTweets is empty, fixes max
		return max(tweetId for _,tweetId in newTweets)

			
	def claimModificationRights(self):

		try:

			self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
			self.curs.execute("SELECT currently_being_modified FROM statustable;")
			result= self.curs.fetchone()[0]
			if (result == True):
				print "Currently being used"
				self.conn.rollback()
				self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
				return False

			print "Ready for update"
			self.curs.execute("UPDATE statustable SET currently_being_modified = TRUE;")
			self.conn.commit()
			print "Cliam modify rights sucess"
			self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
			return True

		except psycopg2.extensions.TransactionRollbackError as e:
			print "Transaction failed in trying to claim rights"
			print e
			self.conn.rollback()
			self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
			return False

	def releaseModificationRights(self):
		self.curs.execute("UPDATE statustable SET currently_being_modified = FALSE")
		self.conn.commit()
		print "Modify rights released"


	def getNewestTweetsSinceLastUpdate(self):
		self.curs.execute("SELECT last_id_recieved FROM statustable;")
		last_id_recieved = self.curs.fetchone()[0]
		print last_id_recieved
		newLastId = self.processTweets(last_id_recieved)

		self.curs.execute("UPDATE statustable SET last_id_recieved = %s", (newLastId,))

		self.conn.commit()



	def __enter__(self):
		return self

	def __exit__(self,*ignored):
		self.curs.close()
		self.conn.close()


	def getEventsForTeam(self,teamNumber):
		self.curs.execute("""SELECT year,name FROM event_team_relationships
			INNER JOIN teams ON teams.id = event_team_relationships.team_id
			INNER JOIN events ON events.id = event_team_relationships.event_id
			WHERE teams.team_number= %s
			""", (teamNumber,))
		results = self.curs.fetchall()
		self.conn.commit()

		print results


		return [ {'year':result[0], 'event': result[1]} for result in results]

	def checkForUpdates(self):

		if self.claimModificationRights():	
			self.getNewestTweetsSinceLastUpdate()
			self.releaseModificationRights()