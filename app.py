from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Facebook ভেরিফিকেশন টোকেন (আপনার ইচ্ছামতো নাম দিন)
VERIFY_TOKEN = "mahfuz123"

# Facebook পেজ অ্যাকসেস টোকেন (আপনার প্রদত্ত টোকেন)
PAGE_ACCESS_TOKEN = "EAARUYfBH2isBO8WCvo7fIVN1Hv7b2jBufYoVFDVxugDpuqksBsH3WZBVthmzAazQKjqFMFHJG9SYgwoPA5tkGdPdDQbTyXZBJcvzuIxVFrrYphWkboHZC2jlqrWsOMAPEEBKwo3jPZBekHq6eh2TEQIAvtWhKpJAzZCzOfL9rVGkbG7su12lk8bqUWgY18NPmBgZDZD"

# Webhook ভেরিফিকেশন
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    hub_mode = request.args.get('hub.mode')
    hub_token = request.args.get('hub.verify_token')
    hub_challenge = request.args.get('hub.challenge')

    if hub_mode and hub_token:
        if hub_mode == 'subscribe' and hub_token == VERIFY_TOKEN:
            print("Webhook verified!")
            return hub_challenge, 200
        else:
            return "Verification failed", 403
    return "Hello, this is your webhook!", 200

# মেসেজ হ্যান্ডলিং
@app.route('/webhook', methods=['POST'])
def handle_messages():
    data = request.json
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id = messaging_event['sender']['id']
                if 'message' in messaging_event:
                    message_text = messaging_event['message']['text']
                    if message_text.lower() == 'সালাম':
                        send_message(sender_id, "ওয়ালাইকুম আসসালাম! আপনার সাথে কিভাবে সাহায্য করতে পারি?")
    return "ok", 200

# মেসেজ পাঠানোর ফাংশন
def send_message(sender_id, message):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": message}
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")

# সার্ভার চালু করুন
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
