#for News bot
from flask import Flask, request
import json 
from pymessenger import Bot
#from utilsForAiml import fetch_reply
from utilsForapiai import apiai_response
from utilsForGenericTemplate import fetch_reply


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

if __name__ == "__main__":
	app.run(port=8000, use_reloader = True) 
	# flask will detect change on its own . no need to run the app file again and again ..