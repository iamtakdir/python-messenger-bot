import os,sys
from flask import Flask , request
from pymessenger import Bot
import requests
from verify import*


app = Flask(__name__)
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Don't Write Hello World", 200

@app.route('/',methods=['POST'])

def webhook():
    data=request.get_json()
    log(data)

    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                sender_id= messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text=messaging_event['message']['text']

                # Sending Response 
                    sendmessage=messaging_text
                    bot.send_text_message(sender_id,sendmessage)
                
    return "Is fine Dude",200
def log(message):
    print(message)
    sys.stdout.flush()


if __name__=="__main__":
    app.run(debug=True,port =80)