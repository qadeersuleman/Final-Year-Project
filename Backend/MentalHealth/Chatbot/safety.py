"""
Safety and crisis detection module
"""
import re
from .config import CRISIS_KEYWORDS, CRISIS_RESPONSE

class SafetyHandler:
    def __init__(self):
        self.crisis_keywords = CRISIS_KEYWORDS
        self.crisis_patterns = [
            r"i (want|wanna) (to )?die",
            r"i (should|might) kill myself",
            r"no point (in|to) living",
            r"better off (dead|without me)",
            r"can'?t go on",
            r"end it all"
        ]
    
    def is_crisis_message(self, text):
        """Check if message indicates crisis situation"""
        text_lower = text.lower()
        
        # Check for exact crisis keywords
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                return True
        
        # Check for crisis patterns
        for pattern in self.crisis_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def get_crisis_response(self):
        """Get crisis resources"""
        return CRISIS_RESPONSE
    
    def add_safety_disclaimer(self, response):
        """Add safety disclaimer to responses when appropriate"""
        disclaimer = "\n\n💙 Remember: I'm an AI assistant. For professional help, consider speaking with a therapist or counselor."
        return response + disclaimer