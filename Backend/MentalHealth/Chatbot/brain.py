"""
IMPROVED AI brain - better emotion detection and context understanding
"""
import random
import re
from .config import THERAPEUTIC_RESPONSES, EMOTION_WORDS

class TherapeuticBrain:
    def __init__(self):
        self.responses = THERAPEUTIC_RESPONSES
        self.emotion_words = EMOTION_WORDS
        self.conversation_context = []
        
        # Add POSITIVE emotion words
        self.positive_emotion_words = {
            'good': ['good', 'great', 'awesome', 'wonderful', 'nice', 'better', 'well', 'happy', 'joy', 'pleased'],
            'calm': ['calm', 'peaceful', 'relaxed', 'chill', 'serene'],
            'hopeful': ['hopeful', 'optimistic', 'positive', 'excited', 'looking forward'],
            'proud': ['proud', 'accomplished', 'achieved', 'success', 'progress']
        }
        
    def analyze_message(self, text):
        """Analyze user message for emotional content and themes"""
        text_lower = text.lower()
        
        analysis = {
            'emotions': self._detect_emotions(text_lower),
            'urgency': self._assess_urgency(text_lower),
            'themes': self._extract_themes(text_lower),
            'length': len(text.split()),
            'has_question': '?' in text,
            'is_positive': self._is_positive_message(text_lower),
            'is_negative': self._is_negative_message(text_lower)
        }
        
        return analysis    
        
    def _detect_emotions(self, text):
        """Detect emotions in text - IMPROVED VERSION"""
        emotions_found = []
        
        # Check for POSITIVE emotions first
        for emotion, words in self.positive_emotion_words.items():
            for word in words:
                if word in text:
                    emotions_found.append(emotion)
                    break
        
        # Check for NEGATIVE emotions
        for emotion, words in self.emotion_words.items():
            for word in words:
                if word in text:
                    # Don't add if we already have positive emotions (unless mixed signals)
                    if not emotions_found or 'not' in text or 'but' in text:
                        emotions_found.append(emotion)
                    break
        
        # Special case: "not good", "not well", "not happy"
        if 'not' in text and any(pos in text for pos in ['good', 'well', 'happy', 'great']):
            if 'good' in emotions_found:
                emotions_found.remove('good')
            emotions_found.append('bad')
            
        return emotions_found if emotions_found else ['neutral']
    
    def _is_positive_message(self, text):
        """Check if message is positive"""
        positive_indicators = [
            'good', 'great', 'awesome', 'happy', 'better', 'well', 
            'excited', 'proud', 'achieved', 'progress', 'improved'
        ]
        
        # Check for positive words WITHOUT negation
        for indicator in positive_indicators:
            if indicator in text:
                # Make sure it's not negated
                if f"not {indicator}" not in text and f"n't {indicator}" not in text:
                    return True
        return False
    
    def _is_negative_message(self, text):
        """Check if message is negative"""
        negative_indicators = [
            'bad', 'sad', 'anxious', 'stressed', 'tired', 'angry', 
            'depressed', 'hopeless', 'overwhelmed', 'exhausted'
        ]
        
        # Explicit negative words
        for indicator in negative_indicators:
            if indicator in text:
                return True
                
        # Negated positive words
        if any(neg in text for neg in ['not good', 'not well', "don't feel good", "not happy"]):
            return True
            
        return False
    
    def _assess_urgency(self, text):
        """Assess urgency level of message - IMPROVED"""
        urgency_score = 0
        
        # Only assess urgency for negative messages
        if self._is_positive_message(text):
            return 0  # No urgency for positive messages
        
        # Intensity words
        intensity_words = ['really', 'very', 'extremely', 'so', 'too', 'cannot', 'can\'t', 'never', 'always']
        for word in intensity_words:
            if word in text:
                urgency_score += 1
        
        # Exclamation marks
        urgency_score += text.count('!') * 2
        
        # Negative absolute statements
        absolute_negative = ["can't take", "can't handle", "can't do this", "hate this", "want to die"]
        for phrase in absolute_negative:
            if phrase in text:
                urgency_score += 3
        
        return min(urgency_score, 10)
    
    def _extract_themes(self, text):
        """Extract key themes from text"""
        themes = []
        
        # Common mental health themes
        common_themes = {
            'sleep': ['sleep', 'tired', 'bed', 'night', 'insomnia', 'awake'],
            'work': ['work', 'job', 'boss', 'colleague', 'deadline', 'office'],
            'family': ['family', 'parent', 'mother', 'father', 'sibling', 'child', 'wife', 'husband'],
            'friends': ['friend', 'friends', 'social', 'lonely', 'alone'],
            'school': ['school', 'exam', 'test', 'homework', 'study', 'college'],
            'health': ['sick', 'pain', 'health', 'doctor', 'hospital'],
            'daily': ['today', 'yesterday', 'morning', 'night', 'day', 'week']
        }
        
        for theme, keywords in common_themes.items():
            for keyword in keywords:
                if keyword in text:
                    themes.append(theme)
                    break
        
        return themes
    
    def generate_response(self, user_message, analysis):
        """Generate appropriate response based on analysis - FIXED VERSION"""
        # Choose response strategy based on message type
        if analysis['is_positive']:
            return self._build_positive_response(analysis)
        elif analysis['is_negative']:
            return self._build_therapeutic_response(analysis, user_message)
        else:
            return self._build_neutral_response(user_message)
    
    def _build_positive_response(self, analysis):
        """Build response for positive messages"""
        positive_responses = [
            "That's wonderful to hear! I'm really glad you're feeling good. 😊",
            "It's great that you're having a positive experience! What's contributing to these good feelings?",
            "I'm happy to hear that! Celebrating the good moments is so important.",
            "That's fantastic! It sounds like things are going well for you.",
            "I'm really pleased to hear you're feeling good! Would you like to share what's been working well for you?",
            "That's excellent! Positive feelings deserve to be acknowledged and celebrated."
        ]
        
        # Add follow-up question occasionally
        response = random.choice(positive_responses)
        if random.random() < 0.6:  # 60% chance to ask follow-up
            follow_ups = [
                " What's been helping you feel this way?",
                " Is there anything specific that's contributing to these good feelings?",
                " How can you build on this positive energy?"
            ]
            response += random.choice(follow_ups)
            
        return response
    
    def _build_therapeutic_response(self, analysis, user_message):
        """Build therapeutic response for negative messages"""
        strategy = self._choose_strategy(analysis)
        
        if strategy == 'validate_explore':
            emotion = analysis['emotions'][0] if analysis['emotions'] else 'challenged'
            # Make sure we don't call positive emotions "challenged"
            if emotion in self.positive_emotion_words:
                emotion = 'mixed'  # Handle mixed emotions
            validate = random.choice(self.responses['validation']).format(emotion=emotion)
            explore = random.choice(self.responses['exploration'])
            return f"{validate} {explore}"
        
        elif strategy == 'reflect_clarify':
            summary = self._create_accurate_summary(user_message)
            reflect = random.choice(self.responses['reflection']).format(summary=summary)
            return reflect
        
        elif strategy == 'support_coping':
            support = random.choice(self.responses['support'])
            return support
        
        else:
            return self._build_default_response()
    
    def _build_neutral_response(self, user_message):
        """Build response for neutral/unclear messages"""
        neutral_responses = [
            "Thanks for sharing. I'm here to listen whenever you need to talk.",
            "I appreciate you checking in. How are things really going for you?",
            "I'm listening. Feel free to share whatever's on your mind.",
            "Tell me more about what's been happening lately.",
            "I'm here to support you. What would you like to talk about today?"
        ]
        return random.choice(neutral_responses)
    
    def _choose_strategy(self, analysis):
        """Choose therapeutic strategy based on analysis"""
        urgency = analysis['urgency']
        message_length = analysis['length']
        
        if urgency >= 7:
            return 'support_coping'
        elif message_length < 6:  # Short message
            return 'validate_explore'
        elif message_length > 12:  # Long message
            return 'reflect_clarify'
        else:
            strategies = ['validate_explore', 'reflect_clarify', 'support_coping']
            weights = [0.5, 0.3, 0.2]
            return random.choices(strategies, weights=weights)[0]
    
    def _create_accurate_summary(self, message):
        """Create accurate summary without misclassifying"""
        message_lower = message.lower()
        
        # Handle positive messages
        if any(word in message_lower for word in ['good', 'great', 'well', 'better', 'happy']):
            if 'not' in message_lower:
                return "you're not feeling as good as you'd like"
            else:
                return "you're feeling pretty good about things"
        
        # Handle sleep themes
        if any(word in message_lower for word in ['sleep', 'night', 'bed', 'tired']):
            return "your sleep patterns have been affecting you"
        
        # Handle general negative feelings
        if any(word in message_lower for word in ['bad', 'sad', 'anxious', 'stressed']):
            return "you've been dealing with some difficult feelings"
        
        # Default summary
        return "you're experiencing some challenges right now"
    
    def _build_default_response(self):
        """Build default therapeutic response"""
        return random.choice([
            "Thank you for sharing that with me. Can you tell me more about what you're experiencing?",
            "I appreciate you opening up about this. What's that been like for you?",
            "I'm listening. What else is coming up for you as we talk about this?"
        ])