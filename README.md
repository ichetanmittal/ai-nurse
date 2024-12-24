# AI Nurse Chatbot

An intelligent chatbot that simulates conversations with a nurse, providing general health information and guidance.

## Disclaimer
This chatbot is for educational and informational purposes only. It does not replace professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Features
- Real-time chat interface
- Nurse-like conversational AI
- General health information
- Emergency situation handlers
- Medical disclaimers
