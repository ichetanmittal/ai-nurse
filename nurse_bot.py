import re
from datetime import datetime
from typing import List, Dict

class NurseBot:
    def __init__(self):
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.emergency_keywords = [
            "emergency", "heart attack", "stroke", "bleeding", "unconscious",
            "severe pain", "difficulty breathing", "chest pain"
        ]
        
    def create_system_prompt(self, user_id: str) -> str:
        """Creates a dynamic system prompt based on conversation history and time of day."""
        current_time = datetime.now()
        greeting = self._get_time_based_greeting(current_time)
        
        base_prompt = f"""You are an AI nurse assistant. {greeting}

Role and Approach:
- Speak in a warm, professional, and empathetic tone
- Use clear, simple language avoiding medical jargon
- Show genuine concern for the user's well-being
- Be patient and thorough in your responses

Medical Guidelines:
- Cannot diagnose conditions or prescribe medications
- Must recommend professional medical consultation for serious concerns
- Can provide general health information and wellness advice
- Should focus on preventive care and healthy lifestyle choices

Conversation History Context:
{self._get_conversation_summary(user_id)}

Important:
- Always maintain professional boundaries
- Prioritize patient safety above all
- Include relevant medical disclaimers
- Direct to emergency services if situation requires immediate medical attention"""
        
        return base_prompt

    def _get_time_based_greeting(self, current_time: datetime) -> str:
        """Returns an appropriate greeting based on time of day."""
        hour = current_time.hour
        if 5 <= hour < 12:
            return "Good morning! I'm here to assist you with any health-related questions."
        elif 12 <= hour < 17:
            return "Good afternoon! I'm here to help you with your health concerns."
        else:
            return "Good evening! I'm here to assist you with any health-related questions."

    def _get_conversation_summary(self, user_id: str) -> str:
        """Creates a summary of recent conversation history."""
        if user_id not in self.conversation_history:
            return "This is a new conversation."
            
        recent_messages = self.conversation_history[user_id][-5:]
        summary = "Recent conversation context:\n"
        for msg in recent_messages:
            summary += f"- {msg['role']}: {msg['content'][:50]}...\n"
        return summary

    def check_for_emergency(self, message: str) -> bool:
        """Checks if the message contains emergency keywords."""
        return any(keyword in message.lower() for keyword in self.emergency_keywords)

    def get_emergency_response(self) -> str:
        """Returns an emergency response message."""
        return """IMPORTANT: Based on what you've described, you should seek immediate medical attention. 

If this is an emergency:
1. Call emergency services (911 in the US) immediately
2. Do not wait or delay seeking professional medical care
3. If possible, have someone stay with you

I cannot provide medical advice for emergency situations. Please prioritize your safety and contact medical professionals right away."""

    def update_conversation_history(self, user_id: str, role: str, content: str):
        """Updates the conversation history for a user."""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 messages to manage memory
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]

    def process_message(self, user_id: str, message: str) -> str:
        """Main method to process incoming messages."""
        # Update conversation history
        self.update_conversation_history(user_id, 'user', message)
        
        # Check for emergency keywords
        if self.check_for_emergency(message):
            response = self.get_emergency_response()
            self.update_conversation_history(user_id, 'assistant', response)
            return response
            
        return None  # Allow main app to handle normal responses
