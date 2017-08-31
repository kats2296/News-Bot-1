#for News bot
from flask import Flask, request
import json 
from pymessenger import Bot
from utilsForAiml import fetch_reply_aiml
from utilsForapiai import apiai_response
from utilsForGenericTemplate import fetch_reply
import requests


app = Flask(__name__) # creates a flask app.. write anything instead of name

#print (__name__)

FB_ACCESS_TOKEN = "EAABz0JLgY20BAKmwwuZAmDPt3xEZC95WgNCiSBd5JKz7CHrvIjZBck4tx9DohEwxMJlzrZB9xBnTUZC4umPKZC8T4ZBoNZBS9eYChIFMyZBItpLZAA91KqG4cLKDEbSvSjbZAXSmGn5vAKJQqxkBfzMgB1roZAVwbIruHs4qPgLcjXuSEbthP1ZCdCKj7"
bot = Bot(FB_ACCESS_TOKEN)
@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	print('request is :\n')
	print(request.data)
	print ('\n\n\n\n')

	data = request.get_json()

	if data['object'] == "page":
		entries = data['entry']

		for entry in entries:
			messaging = entry['messaging']

			for messaging_event in messaging:

				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):

					if messaging_event['message'].get('text'):
						print('msg received is :\n')
						query = messaging_event['message']['text']
						print(query)
						print('\n\n\n\n\n')

						reply = fetch_reply(query, sender_id)


						if reply['type'] == 'news':
							bot.send_generic_message(sender_id, reply['data'])

						else:

						 	bot.send_text_message(sender_id, reply['data'])


						buttons_web_url = [
									  {
									    "type":"web_url",
									    "url":"www.google.com",
									    "title":"checkout this website",
									    "webview_height_ratio": "full",
									    "messenger_extensions": "true",  
									  }
								  ]

						buttons_postback = [{"type":"postback",
									"payload":"SHOW HELP",
									"title":"click to help"}]#this will go as a message to our webhook 

						if query == "url" :
							bot.send_button_message(sender_id, "here is my website", buttons_web_url)
						elif query == "postback":
							bot.send_button_message(sender_id, "here is my website", buttons_postback)
						print('done succesfully \n\n')

				elif messaging_event.get('postback'):
					if messaging_event['postback']['payload'] == 'SHOW HELP':
						bot.send_text_message(sender_id,"okayyyyyyyyyyy")
						


	return "ok", 200


def set_greeting_text():
	headers = {
		'Content-Type':'application/json'
		}
	data = {
		"setting_type":"greeting",
		"greeting":{
			"text":"Hi {{user_first_name}}! Iam news bot"
			}
		}
	ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
	r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
	print(r.content)


def set_persistent_menu():
	headers = {
		'Content-Type':'application/json'
		}
	data = {
		"setting_type":"call_to_actions",
		"thread_state" : "existing_thread",
		"call_to_actions":[
			{
				"type":"web_url",
				"title":"View Website",
				"url":"http://codingblocks.com/" 
			},
			{
				"type":"web_url",
				"title":"Enroll now!",
				"url":"http://students.codingblocks.xyz/purchasable_course"
			},
			{
				"type":"web_url",
				"title":"Register",
				"url":"http://codingblocks.com/signup/"
			}]
		}
	ENDPOINT = "https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s"%(FB_ACCESS_TOKEN)
	r = requests.post(ENDPOINT, headers = headers, data = json.dumps(data))
	print(r.content)

if __name__ == "__main__":
	#set_persistent_menu()
	set_greeting_text()
	app.run(port=8000, use_reloader = True) 
	# flask will detect change on its own . no need to run the app file again and again ..