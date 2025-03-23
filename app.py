import requests
import time

PAGE_ACCESS_TOKEN = "EAARUYfBH2isBO8WCvo7fIVN1Hv7b2jBufYoVFDVxugDpuqksBsH3WZBVthmzAazQKjqFMFHJG9SYgwoPA5tkGdPdDQbTyXZBJcvzuIxVFrrYphWkboHZC2jlqrWsOMAPEEBKwo3jPZBekHq6eh2TEQIAvtWhKpJAzZCzOfL9rVGkbG7su12lk8bqUWgY18NPmBgZDZD"
LAST_MESSAGE_ID = None  # সর্বশেষ বার্তার ID সংরক্ষণ করবে

def get_latest_message():
    global LAST_MESSAGE_ID
    
    url = f"https://graph.facebook.com/v18.0/me/conversations?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.get(url).json()
    
    if "data" in response and len(response["data"]) > 0:
        latest_conversation = response["data"][0]
        conversation_id = latest_conversation["id"]
        
        # মেসেজ লিস্ট চেক করা
        messages_url = f"https://graph.facebook.com/v18.0/{conversation_id}/messages?access_token={PAGE_ACCESS_TOKEN}"
        messages = requests.get(messages_url).json()
        
        if "data" in messages and len(messages["data"]) > 0:
            latest_message = messages["data"][0]
            message_id = latest_message["id"]
            sender_id = None

            # Check if 'from' exists, otherwise handle it gracefully
            if 'from' in latest_message:
                sender_id = latest_message["from"]["id"]
            else:
                print("Error: 'from' field not found in message!")
                # Optional: Check message type, or just skip non-user messages
                if 'message' in latest_message:
                    print("Message Type:", latest_message['message'])
                    # Ignore system messages or other types
                    return None, None
                else:
                    return None, None
            
            # 🔹 নতুন মেসেজ চেক করে
            if LAST_MESSAGE_ID != message_id:  
                LAST_MESSAGE_ID = message_id
                return sender_id, latest_message["message"]
    
    return None, None

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    
    response = requests.post(url, json=data)
    return response.json()

# Polling loop
while True:
    sender, message = get_latest_message()
    if sender and message:
        print(f"📩 নতুন মেসেজ: {message} (from {sender})")
        send_message(sender, "আসসালামুয়ালাইকুম!")
    
    time.sleep(5)  # প্রতি ৫ সেকেন্ড পরপর নতুন মেসেজ চেক করা
