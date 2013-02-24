import oauth2 as oauth
import time

from urllib import urlencode
import simplejson as json




token = oauth.Token(key="521009685-Tshddm088RjBEYgFIF7GQLPgytxukwGmF1HBRtS2", secret="bgudBU4uw5zoFWn5aKYMZlMoURAgU0KjX4UzzuR9AI")
consumer = oauth.Consumer(key="Mcihyoz7UxRZrgBiXvc3A", secret="atTWpRCu8r0RKDqnEdeTq3df06yI3Yjy8OEiOSvOQk")
client = oauth.Client(consumer,token)
url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"

def getTimeline(**kwargs):
	params = {
    'trim_user' : True,
    'exclude_replies' : True,
    'contributer_details' : False,
    'include_rts' : False
	}

	params.update(kwargs)





	resp,content = client.request(url+urlencode(params),'GET')

	if resp.status != 200:
		raise Exception("The status of the twitter request was not 200\n" + content + '\n' + str(resp))

	return json.loads(content)

def getWholeTimeline(screen_name,since_id):

	result = getTimeline(screen_name=screen_name,since_id=since_id)
	output = []


	while len(result) != 0:
		output.extend( (item['text'],item['id']) for item in result)
		for item in result:
			print item['text'], item['id']
		minId = min(item['id'] for item in result)
		result = getTimeline(screen_name=screen_name,since_id=since_id,max_id=minId-1)

	return output

