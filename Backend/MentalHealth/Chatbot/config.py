"""
UPDATED Configuration with better response templates
"""

# Therapeutic response patterns - IMPROVED
THERAPEUTIC_RESPONSES = {
    'validation': [
        "That sounds really {emotion}. It makes complete sense you'd feel that way.",
        "I can hear how {emotion} this is for you. Thank you for sharing that.",
        "It's completely understandable to feel {emotion} when facing something like that.",
        "That sounds incredibly challenging. Your feelings are valid.",
        "I can imagine how {emotion} that must feel. Thank you for telling me."
    ],
    'exploration': [
        "Can you tell me more about what that's like for you?",
        "What goes through your mind when you experience that?",
        "How does this affect your daily life?",
        "When did you first start noticing these feelings?",
        "What's the hardest part about this for you?"
    ],
    'reflection': [
        "So what I'm hearing is that {summary}. Is that right?",
        "It sounds like {summary}. Am I understanding you correctly?",
        "Let me see if I'm following - {summary}.",
        "You're saying that {summary}. Did I get that right?",
        "If I understand correctly, {summary}. Is that accurate?"
    ],
    'support': [
        "What has helped you cope with similar feelings in the past?",
        "Is there anything that brings you even a small sense of relief?",
        "How do you usually take care of yourself when feeling this way?",
        "What would feel supportive to you right now?",
        "What kind of support would be most helpful for you currently?"
    ]
}

# Crisis keywords and resources
CRISIS_KEYWORDS = {
    'suicide', 'kill myself', 'end it all', 'want to die', 'harm myself',
    'no point', 'can\'t go on', 'better off dead', 'end my life'
}

CRISIS_RESPONSE = """
🚨 **Immediate Support Available**

Please reach out to these resources right now:
• **National Suicide Prevention Lifeline**: 988 (US & Canada)
• **Crisis Text Line**: Text HOME to 741741
• **International Emergency**: 112 or your local emergency number

You are not alone, and there are people who want to help you.
"""

# Coping techniques
COPING_TECHNIQUES = {
    'breathing': {
        'name': "4-7-8 Breathing",
        'steps': [
            "Find a comfortable sitting position",
            "Breathe in quietly through your nose for 4 seconds",
            "Hold your breath for 7 seconds", 
            "Exhale completely through your mouth for 8 seconds",
            "Repeat this cycle 3-4 times"
        ]
    },
    'grounding': {
        'name': "5-4-3-2-1 Senses",
        'steps': [
            "Name 5 things you can see around you",
            "Name 4 things you can touch",
            "Name 3 things you can hear",
            "Name 2 things you can smell", 
            "Name 1 thing you can taste"
        ]
    },
    'mindfulness': {
        'name': "Quick Mindfulness",
        'steps': [
            "Close your eyes and take 3 deep breaths",
            "Notice how your body feels without judgment",
            "Observe your thoughts like clouds passing by",
            "Gently return your focus to your breathing"
        ]
    }
}

# Emotional vocabulary - EXPANDED
EMOTION_WORDS = {
    'sad': ['sad', 'depressed', 'hopeless', 'empty', 'grief', 'sorrow', 'down', 'bad', 'terrible', 'awful'],
    'anxious': ['anxious', 'worried', 'nervous', 'panicked', 'scared', 'fear', 'overwhelmed', 'stressed'],
    'angry': ['angry', 'frustrated', 'irritated', 'annoyed', 'rage', 'mad', 'furious'],
    'tired': ['tired', 'exhausted', 'drained', 'fatigued', 'burned out', 'sleepy'],
    'lonely': ['lonely', 'isolated', 'alone', 'abandoned'],
    'confused': ['confused', 'lost', 'uncertain', 'unsure', 'mixed']
}