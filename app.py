from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO
import openai
from dotenv import load_dotenv
import os
from nurse_bot import NurseBot
import secrets

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for testing

# Initialize OpenAI and NurseBot
openai.api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key loaded: {'*' * len(os.getenv('OPENAI_API_KEY', ''))}") # Debug print
nurse_bot = NurseBot()

def get_chatbot_response(user_id, user_message):
    try:
        # First, let the nurse bot process the message
        nurse_response = nurse_bot.process_message(user_id, user_message)
        if nurse_response:
            return nurse_response

        # If no emergency response, proceed with OpenAI
        system_prompt = nurse_bot.create_system_prompt(user_id)
        
        print(f"Sending request to OpenAI with message: {user_message[:50]}...")  # Debug print
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        bot_response = response.choices[0].message.content
        nurse_bot.update_conversation_history(user_id, 'assistant', bot_response)
        return bot_response

    except Exception as e:
        print(f"Error in get_chatbot_response: {str(e)}")  # Debug print
        error_msg = "I apologize, but I'm having trouble processing your request. Please try again later."
        nurse_bot.update_conversation_history(user_id, 'assistant', error_msg)
        return error_msg

@app.route('/')
def home():
    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(16)
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    user_message = data['message']
    user_id = session.get('user_id', 'default_user')
    bot_response = get_chatbot_response(user_id, user_message)
    socketio.emit('receive_message', {'message': bot_response, 'sender': 'bot'})

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5001)
