#!/usr/bin/env python3
"""
TEST the improved mental health chatbot
"""

import sys
import os

# Add the chatbot module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Chatbot'))

from Chatbot.chatbot import MentalHealthChatbot

def test_chatbot():
    """Test the chatbot with various inputs"""
    print("🧠 Testing Improved Mental Health Chatbot")
    print("Type 'quit' to exit\n")
    
    chatbot = MentalHealthChatbot()
    
    # Test cases that were previously failing
    test_messages = [
        "Sleep at late night",
        "I'm felling bad today", 
        "felling good i get yesterday",
        "it is not challengable i fell good",
        "I'm feeling great today!",
        "I feel anxious about my exam",
        "Not feeling well today",
        "I'm so happy everything worked out"
    ]
    
    print("=== Running Test Cases ===")
    for message in test_messages:
        print(f"\nYou: {message}")
        response = chatbot.get_response(message)
        print(f"Bot: {response}")
    
    print("\n" + "="*50)
    print("Now you can chat with the bot directly:")
    
    # Interactive chat
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye! Take care. 💙")
                break
                
            if not user_input:
                continue
                
            response = chatbot.get_response(user_input)
            print(f"Bot: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Take care. 💙")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_chatbot()