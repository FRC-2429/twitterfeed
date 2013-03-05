import requests


def getRegionalsForYear(year):
	r= requests.get("http://www.thebluealliance.com/api/v1/events/list",params={"year": year})

	regionalList = [key["key"] for key in r.json() if key["official"]]
	return regionalList

def getMatchesForRegional(regionalKey):
	r = requests.get("http://www.thebluealliance.com/api/v1/event/details",params={"event":regionalKey})

	return r.json()["matches"]

def getDetailsForMatch(matchKey):
	r = requests.get("http://www.thebluealliance.com/api/v1/match/details",params={"match":matchKey})
	return r.json()

def getDetailsForMatches(matchList):
	r = requests.get("http://www.thebluealliance.com/api/v1/match/details",params={"matches":",".join(matchList)})
	print r.url
	return r.json()

