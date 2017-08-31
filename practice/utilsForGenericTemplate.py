import apiai
import json
import requests
from utilsForAiml import fetch_reply_aiml


APIAI_ACCESS_TOKEN = "afdd1251c5df488c9bef992ea7a854ab"

ai = apiai.ApiAI(APIAI_ACCESS_TOKEN)

GNEWS_API_ENDPOINT = "https://gnewsapi.herokuapp.com"

def get_news(params):

	params['news'] = params['news_type']
	resp = requests.get(GNEWS_API_ENDPOINT, params = params)

	return resp.json()


def apiai_response(query, session_id):
	"""
	function to fetch api.ai response
	"""
	request = ai.text_request()
	request.lang='en'
	request.session_id=session_id
	request.query = query
	response = request.getresponse()
	return json.loads(response.read().decode('utf8'))


def parse_response(response):
	"""
	function to parse response and 
	return intent and its parameters
	"""
	result = response['result']
	params = result.get('parameters')
	intent = result['metadata'].get('intentName')
	return intent, params

	
def fetch_reply(query, session_id):
	"""
	main function to fetch reply for chatbot and 
	return a reply dict with reply 'type' and 'data'
	"""
	response = apiai_response(query, session_id)
	intent, params = parse_response(response)

	reply = {}

	if intent == None:
		reply['type'] = 'none'
		reply = fetch_reply_aiml(query, session_id)
		reply['data'] = reply['data']

	elif intent == "news":
		reply['type'] = 'news'
		print(params)
		articles = get_news(params)
		news_elements = []

		for article in articles:
			element = {}
			element['title'] = article['title']
			element['item_url'] = article['link']
			element['image_url'] = article['img']
			element['buttons'] = [{
				"type":"web_url",
				"title":"Read more",
				"url":article['link']}]
			news_elements.append(element)

		reply['data'] = news_elements

	elif intent.startswith('smalltalk'):
		reply['type'] = 'smalltalk'
		reply['data'] = response['result']['fulfillment']['speech']

	return reply

#print get_news({'news':'politics'})