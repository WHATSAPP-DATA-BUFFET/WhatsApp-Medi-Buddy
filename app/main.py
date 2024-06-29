from langchain.prompts.chat import HumanMessagePromptTemplate 
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from flask import Flask, request
import json
import re


from flask import Flask, request, json
from vonage import send_message  # Ensure this function is synchronous
from function_calling import common_func
import threading
import time


from app.function_calling import filter_user_query

app = Flask(__name__)
lock = threading.Lock()
processed_messages = set()
processing_messages = {}

@app.route('/')
def home():
    return 'Everything is going good. Go ahead!!'

@app.route('/chat', methods=['POST'])
def handle_message():
    try:
        data = request.get_json()
        print('data-->',data)
        message_id = data.get('message_uuid')  # Assuming message_id is included in the request
        user_text = data['text']
        sender_id = data['from']

        print(f"Received message from {sender_id}: {user_text} with message ID: {message_id}")

        # Check if the message is already processed
        if message_id in processed_messages:
            print("Message already processed.")
            return json.dumps({"response": "Message already processed."}), 200

        # Acquire the lock before checking and updating processing_messages
        with lock:
            # Check if the message is already being processed
            if message_id in processing_messages:
                print("Message is being processed.")
                return json.dumps({"response": "Message is being processed."}), 200

            # Mark the message as being processed
            processing_messages[message_id] = True

        print("Processing message...")

      
        result1 = common_func(question=user_text)

        print("Sending message to user...")
        send_message(sender_id, result1)

        print("Message sent to user.")

        # Acquire the lock before updating processed_messages and removing from processing_messages
        with lock:
            # Mark the message as processed
            processed_messages.add(message_id)
            # Remove the message from processing_messages
            del processing_messages[message_id]

        print("Message processing completed.")

        # Return the response after sending the message
        return json.dumps({"response": result1}), 200

    except Exception as e:
        print(f"Error: {e}")
        return json.dumps({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
