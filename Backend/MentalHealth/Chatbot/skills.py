"""
Coping skills and techniques module
"""
import random
from .config import COPING_TECHNIQUES

class CopingSkills:
    def __init__(self):
        self.techniques = COPING_TECHNIQUES
    
    def get_technique(self, technique_type):
        """Get a specific coping technique"""
        if technique_type in self.techniques:
            tech = self.techniques[technique_type]
            response = f"**{tech['name']}**\n\n"
            for i, step in enumerate(tech['steps'], 1):
                response += f"{i}. {step}\n"
            return response
        return self.get_random_technique()
    
    def get_random_technique(self):
        """Get a random coping technique"""
        tech_type = random.choice(list(self.techniques.keys()))
        return self.get_technique(tech_type)
    
    def get_technique_menu(self):
        """Get menu of available techniques"""
        menu = "**Available Coping Techniques:**\n\n"
        for i, (key, tech) in enumerate(self.techniques.items(), 1):
            menu += f"{i}. {tech['name']} ({key})\n"
        menu += "\nJust type the number or name of the technique you'd like to try!"
        return menu
    
    def suggest_technique_based_on_emotion(self, emotion):
        """Suggest appropriate technique based on emotion"""
        suggestions = {
            'anxious': 'breathing',
            'stressed': 'breathing', 
            'angry': 'mindfulness',
            'sad': 'grounding',
            'tired': 'mindfulness',
            'overwhelmed': 'grounding'
        }
        technique_type = suggestions.get(emotion, 'breathing')
        return self.get_technique(technique_type)