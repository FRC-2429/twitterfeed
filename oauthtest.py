import oauth2 as oauth
import time

from urllib import urlencode
import simplejson as json

import pprint

# Set the API endpoint 
url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"

# Set the base oauth_* parameters along with any other parameters required
# for the API call.
params = {
    'screen_name': 'frcfms',
    'count': 2
}

# Set up instances of our Token and Consumer. The Consumer.key and 
# Consumer.secret are given to you by the API provider. The Token.key and
# Token.secret is given to you after a three-legged authentication.
token = oauth.Token(key="521009685-Tshddm088RjBEYgFIF7GQLPgytxukwGmF1HBRtS2", secret="bgudBU4uw5zoFWn5aKYMZlMoURAgU0KjX4UzzuR9AI")
consumer = oauth.Consumer(key="Mcihyoz7UxRZrgBiXvc3A", secret="atTWpRCu8r0RKDqnEdeTq3df06yI3Yjy8OEiOSvOQk")

# Set our token/key parameters


client = oauth.Client(consumer,token)
resp,content = client.request(url+urlencode(params),'GET')



pprint.pprint(json.loads(content))

f = open('outdata','w')
f.write(json.dumps(json.loads(content),indent=4))
f.close()
