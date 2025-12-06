"""
Main chatbot class - easy to integrate into existing projects
"""
import random
from .brain import TherapeuticBrain
from .safety import SafetyHandler
from .skills import CopingSkills

class MentalHealthChatbot:
    def __init__(self, enable_safety=True, enable_coping=True):
        self.brain = TherapeuticBrain()
        self.safety = SafetyHandler() if enable_safety else None
        self.skills = CopingSkills() if enable_coping else None
        self.conversation_history = []
        self.user_context = {}
        
        # Response tracking
        self.response_count = 0
        
    def get_response(self, user_message):
        """
        Main method to get chatbot response
        Usage: response = chatbot.get_response("I'm feeling anxious today")
        """
        # Store conversation
        self.conversation_history.append(('user', user_message))
        self.response_count += 1
        
        # Step 1: Safety check (highest priority)
        if self.safety and self.safety.is_crisis_message(user_message):
            crisis_response = self.safety.get_crisis_response()
            self.conversation_history.append(('assistant', crisis_response))
            return crisis_response
        
        # Step 2: Check for coping skills request
        if self.skills and self._is_coping_request(user_message):
            coping_response = self._handle_coping_request(user_message)
            self.conversation_history.append(('assistant', coping_response))
            return self.safety.add_safety_disclaimer(coping_response) if self.safety else coping_response
        
        # Step 3: Analyze and generate therapeutic response
        analysis = self.brain.analyze_message(user_message)
        response = self.brain.generate_response(user_message, analysis)
        
        # Step 4: Occasionally suggest coping skills
        if (self.skills and 
            self.response_count % 4 == 0 and 
            analysis['urgency'] >= 3 and
            random.random() < 0.4):
            suggestion = "\n\nWould you like to try a coping technique to help with these feelings?"
            response += suggestion
        
        # Step 5: Add safety disclaimer occasionally
        if self.safety and self.response_count % 5 == 0:
            response = self.safety.add_safety_disclaimer(response)
        
        # Store and return
        self.conversation_history.append(('assistant', response))
        return response
    
    def _is_coping_request(self, message):
        """Check if user is requesting coping skills"""
        coping_keywords = [
            'coping', 'technique', 'exercise', 'breathing', 'grounding',
            'mindfulness', 'calm down', 'relax', 'help me cope'
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in coping_keywords)
    
    def _handle_coping_request(self, message):
        """Handle requests for coping techniques"""
        message_lower = message.lower()
        
        if 'breathing' in message_lower:
            return self.skills.get_technique('breathing')
        elif 'grounding' in message_lower:
            return self.skills.get_technique('grounding')
        elif 'mindfulness' in message_lower:
            return self.skills.get_technique('mindfulness')
        elif any(word in message_lower for word in ['which', 'what', 'menu', 'list']):
            return self.skills.get_technique_menu()
        else:
            return self.skills.get_random_technique()
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.conversation_history.copy()
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
    
    def get_stats(self):
        """Get conversation statistics"""
        return {
            'total_messages': len(self.conversation_history),
            'user_messages': len([m for m in self.conversation_history if m[0] == 'user']),
            'assistant_messages': len([m for m in self.conversation_history if m[0] == 'assistant']),
            'response_count': self.response_count
        }