from flask import Flask, request
import json 
from pymessenger import Bot
from utils import apiai_response


app = Flask(__name__) # creates a flask app.. write anything instead of name

#print (__name__)

FB_ACCESS_TOKEN = "EAABz0JLgY20BAJ9QXkM8V9ShebHx1GpF0AGV7N3dSiYospKNkVra6DtpTQ1ZBR0SPwerk6LFoneUhB7TsbtODZC2xjhaP9i5HLxgqZBfo81pInJ5PRHDVxbebyKtaT99TmosZAlxIW1s5JhfZCOZB2NBMdPfVXpHH2xQ0OSrizzgZDZD"
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
						intent , params , action , reply = apiai_response(query, sender_id)
						if intent is not None:
							if intent == 'news':
								bot.send_text_message(sender_id, str(params))

							elif intent.startswith('smalltalk'):
								bot.send_text_message(sender_id, default)

							else :
								bot.send_text_message(sender_id, "i didn't get you")

						elif action.startswith('smalltalk'):
							bot.send_text_message(sender_id, reply)


	return "ok", 200

if __name__ == "__main__":
	app.run(port=8000, use_reloader = True) 
	# flask will detect change on its own . no need to run the app file again and again ..