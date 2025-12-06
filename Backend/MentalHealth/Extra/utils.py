import re
import json
import random
from datetime import datetime

class MentalHealthChatbot:
    def __init__(self):
        self.greeting_patterns = [
            r'hi|hello|hey|hola|hay|ehy',
            r'good morning|good afternoon|good evening',
            r'how are you|how do you do'
        ]
        
        # Enhanced mental health keywords
        self.mental_health_keywords = [
            'stress', 'anxiety', 'depress', 'sad', 'worry', 'panic',
            'mental', 'therapy', 'counsel', 'psycholog', 'psychiatr',
            'meditat', 'relax', 'breathe', 'calm', 'mindful',
            'sleep', 'insomnia', 'overwhelm', 'burnout', 'trauma',
            'lonely', 'worthless', 'useless', 'scared', 'suicide',
            'bullying', 'hate', 'stressed', 'anxious', 'hopeless',
            'bad', 'not good', 'not well', 'terrible', 'awful',
            'feeling down', 'low', 'miserable', 'unhappy'
        ]
        
        self.medicine_keywords = [
            'medicine', 'medication', 'pill', 'drug', 'prescription',
            'ssri', 'prozac', 'zoloft', 'lexapro', 'xanax', 'ativan'
        ]
        
        self.app_keywords = [
            'app', 'application', 'feature', 'function', 'setting',
            'profile', 'account', 'premium', 'subscription'
        ]
        
        self.doctor_keywords = [
            'doctor', 'therapist', 'psychiatrist', 'counselor',
            'professional', 'specialist', 'referral'
        ]
        
        # Emergency keywords that need immediate attention
        self.emergency_keywords = [
            'suicide', 'kill myself', 'want to die', 'end my life',
            'harm myself', 'self harm', 'hurting myself'
        ]
        
        # Negative feeling patterns
        self.negative_feeling_patterns = [
            r'not good', r'not well', r'feeling bad', r'very bad', r'terrible',
            r'awful', r'miserable', r'hate life', r'can\'t take it'
        ]
        
        # Offensive language patterns
        self.offensive_patterns = [
            r'fuck you', r'stupid', r'dumb', r'hate you', r'shut up'
        ]
        
        self.initialize_responses()
        self.conversation_history = []
    
    def initialize_responses(self):
        self.responses = {
            'greeting': [
                "Hello! I'm here to support your mental health journey. How can I help you today?",
                "Hi there! I'm your mental health assistant. What's on your mind?",
                "Welcome! I'm here to provide mental health support. How are you feeling today?"
            ],
            
            'negative_feelings': [
                "I'm sorry to hear you're not feeling well. Would you like to talk about what's bothering you?",
                "That sounds difficult. I'm here to listen if you want to share what's going on.",
                "I understand you're having a tough time. Remember that it's okay to not be okay. What's on your mind?",
                "Thank you for sharing that with me. I'm here to support you. Can you tell me more about how you're feeling?"
            ],
            
            'mental_health_suggestions': {
                'meditation': [
                    "Try this simple meditation: Sit comfortably, close your eyes, and focus on your breath for 5 minutes.",
                    "Guided meditation can help. Try focusing on different parts of your body, starting from your toes up to your head.",
                    "Mindful breathing: Inhale for 4 counts, hold for 4, exhale for 6. Repeat 10 times."
                ],
                'relaxation': [
                    "Progressive muscle relaxation: Tense and relax each muscle group from feet to head.",
                    "Try the 5-4-3-2-1 technique: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste.",
                    "Warm tea and deep breathing can help relax your nervous system."
                ],
                'anxiety': [
                    "For anxiety, try the 3-3-3 rule: Name 3 things you see, 3 sounds you hear, and move 3 parts of your body.",
                    "Deep breathing: 4-7-8 technique (inhale 4s, hold 7s, exhale 8s) can help calm anxiety.",
                    "Grounding techniques can help when feeling anxious. Focus on your physical surroundings."
                ],
                'general': [
                    "Regular exercise can significantly improve mental health. Even a 10-minute walk helps.",
                    "Maintain a consistent sleep schedule. Aim for 7-9 hours of quality sleep.",
                    "Journaling your thoughts and feelings can provide clarity and emotional release.",
                    "Connect with supportive friends or family members regularly.",
                    "Limit screen time before bed and practice good sleep hygiene."
                ]
            },
            
            'anxiety_info': [
                "Anxiety is a natural response to stress, but when it becomes overwhelming, it can help to practice relaxation techniques.",
                "Many people experience anxiety. The 3-3-3 rule can be helpful: name 3 things you see, 3 sounds you hear, and move 3 body parts.",
                "For anxiety management, try focusing on your breath or practicing mindfulness exercises."
            ],
            
            '333_rule': [
                "The 3-3-3 rule for anxiety: Look around and name 3 things you see. Listen and name 3 sounds you hear. Move 3 parts of your body.",
                "3-3-3 technique: Identify 3 objects you can see, 3 sounds you can hear, and move 3 different body parts. This helps ground you in the present moment.",
                "When anxious, try this: Name 3 things in your environment, identify 3 sounds around you, and physically move 3 parts of your body like fingers, toes, and shoulders."
            ],
            
            'medicine_info': {
                'ssri': "SSRIs (Selective Serotonin Reuptake Inhibitors) are commonly prescribed for depression and anxiety. They work by increasing serotonin levels in the brain.",
                'prozac': "Prozac (fluoxetine) is an SSRI used for depression, OCD, and panic disorder. It may take 4-6 weeks to show full effects.",
                'zoloft': "Zoloft (sertraline) is an SSRI for depression, anxiety, and PTSD. Common side effects include nausea and sleep changes.",
                'lexapro': "Lexapro (escitalopram) is an SSRI known for having fewer side effects. Used for depression and generalized anxiety.",
                'xanax': "Xanax (alprazolam) is a benzodiazepine for anxiety. It's fast-acting but can be habit-forming. Use only as prescribed.",
                'general': "Always consult with a healthcare professional before starting or changing medications. Never stop medication abruptly without medical guidance."
            },
            
            'doctor_referral': [
                "I recommend consulting with a licensed mental health professional for personalized advice.",
                "For proper diagnosis and treatment, please see a qualified psychiatrist or therapist.",
                "Consider reaching out to a mental health specialist who can provide comprehensive care."
            ],
            
            'app_info': [
                {
                    'general': "This app provides mental health support including meditation guides, mood tracking, and relaxation techniques.",
                    'features': "Key features: Chat support, meditation library, mood journal, relaxation exercises, and progress tracking.",
                    'settings': "You can customize notifications, themes, and privacy settings in the app settings menu.",
                    'premium': "Premium version offers advanced features like personalized plans and unlimited meditation sessions."
                }
            ],
            
            'offensive_response': [
                "I'm here to provide supportive mental health care. Let's keep our conversation respectful.",
                "I understand you might be frustrated. I'm here to help if you want to talk about what's bothering you.",
                "I'm programmed to be supportive and non-judgmental. Would you like to discuss what's making you feel this way?"
            ],
            
            'emergency': [
                "I'm very concerned about what you're saying. Please contact a crisis helpline immediately: National Suicide Prevention Lifeline at 1-800-273-8255 or text HOME to 741741.",
                "Your life is precious. Please reach out to emergency services or a crisis helpline right now. You can call 911 or the National Suicide Prevention Lifeline at 1-800-273-8255.",
                "This sounds serious. Please contact emergency services or a trusted person immediately. Help is available 24/7 at the Crisis Text Line by texting HOME to 741741."
            ],
            
            'fallback': [
                "I'm here to listen and support you with mental health concerns. Could you tell me more about how you're feeling?",
                "I specialize in mental health support. If you're dealing with stress, anxiety, depression, or other concerns, I'm here to help.",
                "I want to understand how I can support you better. Could you share what's on your mind related to your mental wellbeing?"
            ]
        }
    
    def classify_intent(self, message):
        message_lower = message.lower().strip()
        
        # Check for emergency situations first (highest priority)
        if any(keyword in message_lower for keyword in self.emergency_keywords):
            return 'emergency'
        
        # Check for offensive language
        for pattern in self.offensive_patterns:
            if re.search(pattern, message_lower):
                return 'offensive'
        
        # Check for greetings
        for pattern in self.greeting_patterns:
            if re.search(pattern, message_lower):
                return 'greeting'
        
        # Check for 3-3-3 rule queries
        if re.search(r'333|3.3.3|three three three', message_lower.replace(' ', '')):
            return '333_rule'
        if '3 3 3' in message_lower or 'three three three' in message_lower:
            return '333_rule'
        
        # Check for negative feelings
        for pattern in self.negative_feeling_patterns:
            if re.search(pattern, message_lower):
                return 'negative_feelings'
        
        # Check for anxiety-related queries
        if 'anxiety' in message_lower or 'anxious' in message_lower:
            if 'what' in message_lower or 'why' in message_lower:
                return 'anxiety_info'
            return 'mental_health'
        
        # Check for mental health topics
        if any(keyword in message_lower for keyword in self.mental_health_keywords):
            return 'mental_health'
        
        # Check for medicine questions
        if any(keyword in message_lower for keyword in self.medicine_keywords):
            return 'medicine'
        
        # Check for doctor referrals
        if any(keyword in message_lower for keyword in self.doctor_keywords):
            return 'doctor'
        
        # Check for app questions
        if any(keyword in message_lower for keyword in self.app_keywords):
            return 'app'
        
        # Check for simple negative responses
        if message_lower in ['bad', 'not good', 'not well', 'terrible']:
            return 'negative_feelings'
        
        return 'fallback'
    
    def generate_response(self, message):
        try:
            intent = self.classify_intent(message)
            message_lower = message.lower()
            
            print(f"Detected intent: {intent}")  # Debug logging
            
            if intent == 'emergency':
                response = random.choice(self.responses['emergency'])
            
            elif intent == 'offensive':
                response = random.choice(self.responses['offensive_response'])
            
            elif intent == 'greeting':
                response = random.choice(self.responses['greeting'])
            
            elif intent == 'negative_feelings':
                response = random.choice(self.responses['negative_feelings'])
            
            elif intent == '333_rule':
                response = random.choice(self.responses['333_rule'])
            
            elif intent == 'anxiety_info':
                response = random.choice(self.responses['anxiety_info'])
            
            elif intent == 'mental_health':
                response = "I understand you're dealing with some challenges. "
                
                # Add specific suggestions based on keywords
                if any(word in message_lower for word in ['anxiety', 'anxious', 'panic']):
                    response += random.choice(self.responses['mental_health_suggestions']['anxiety'])
                elif any(word in message_lower for word in ['stress', 'overwhelm', 'burnout']):
                    response += random.choice(self.responses['mental_health_suggestions']['relaxation'])
                elif any(word in message_lower for word in ['meditat', 'mindful', 'breathe']):
                    response += random.choice(self.responses['mental_health_suggestions']['meditation'])
                else:
                    response += random.choice(self.responses['mental_health_suggestions']['general'])
                
                response += " Would you like to talk more about what you're experiencing?"
            
            elif intent == 'medicine':
                for med_keyword, info in self.responses['medicine_info'].items():
                    if med_keyword != 'general' and med_keyword in message_lower:
                        response = f"About {med_keyword.upper()}: {info}"
                        break
                else:
                    response = self.responses['medicine_info']['general']
            
            elif intent == 'doctor':
                response = random.choice(self.responses['doctor_referral'])
            
            elif intent == 'app':
                if 'feature' in message_lower:
                    response = "App Features: " + self.responses['app_info']['features']
                elif 'setting' in message_lower:
                    response = self.responses['app_info']['settings']
                elif 'premium' in message_lower:
                    response = self.responses['app_info']['premium']
                else:
                    response = self.responses['app_info']['general']
            
            else:  # fallback
                response = random.choice(self.responses['fallback'])
            
            self.log_conversation(message, response)
            return response
                
        except Exception as e:
            print(f"Error generating response: {e}")  # Debug logging
            error_response = "I apologize, but I encountered an error. Please try again. If the problem persists, try rephrasing your question."
            self.log_conversation(message, error_response)
            return error_response
    
    def log_conversation(self, user_message, bot_response):
        """Log conversation for context and improvement"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'timestamp': timestamp,
            'user': user_message,
            'bot': bot_response
        })
        # Keep only last 50 messages to prevent memory issues
        if len(self.conversation_history) > 50:
            self.conversation_history.pop(0)

# Singleton instance
chatbot_instance = MentalHealthChatbot()

# Test the improved chatbot
if __name__ == "__main__":
    chatbot = MentalHealthChatbot()
    
    test_messages = [
        "Hello",
        "Bad very bad",
        "I said i am not felling very well today",
        "Who is srk",
        "Shahrukh", 
        "Ehy",
        "For what go on",
        "Why is anxiety",
        "Fuck you",
        "3 3  3 rule",
        "I'm feeling anxious",
        "What should I do when I feel stressed?",
        "I can't sleep at night"
    ]
    
    for msg in test_messages:
        print(f"User: {msg}")
        response = chatbot.generate_response(msg)
        print(f"Bot: {response}")
        print("-" * 80)