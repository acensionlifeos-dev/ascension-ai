"""
Ascension AI - Emotional Intelligence System
Advanced emotion recognition and emotional intelligence
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
from collections import defaultdict

class EmotionRecognizer:
    """Recognize emotions from text and behavior"""
    
    def __init__(self):
        self.emotion_lexicon = {
            'positive': ['happy', 'joy', 'excited', 'pleased', 'satisfied', 'delighted', 'thrilled'],
            'negative': ['sad', 'angry', 'frustrated', 'disappointed', 'upset', 'worried', 'anxious'],
            'neutral': ['okay', 'fine', 'normal', 'average', 'typical', 'standard'],
            'energetic': ['energetic', 'motivated', 'driven', 'focused', 'productive', 'active'],
            'tired': ['tired', 'exhausted', 'fatigued', 'drained', 'weary', 'sleepy'],
            'stressed': ['stressed', 'overwhelmed', 'pressured', 'anxious', 'nervous', 'tense']
        }
    
    def recognize_emotion(self, text: str) -> Dict:
        """Recognize emotion from text"""
        text_lower = text.lower()
        
        emotion_scores = {}
        for emotion, keywords in self.emotion_lexicon.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Find dominant emotion
        if not emotion_scores or all(score == 0 for score in emotion_scores.values()):
            dominant_emotion = 'neutral'
            confidence = 0.5
        else:
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[dominant_emotion]
            total_score = sum(emotion_scores.values())
            confidence = max_score / total_score if total_score > 0 else 0.5
        
        return {
            'dominant_emotion': dominant_emotion,
            'confidence': confidence,
            'all_scores': emotion_scores,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def recognize_emotion_sequence(self, texts: List[str]) -> List[Dict]:
        """Recognize emotions from a sequence of texts"""
        return [self.recognize_emotion(text) for text in texts]

class EmotionalIntelligence:
    """Advanced emotional intelligence and empathy"""
    
    def __init__(self):
        self.emotion_recognizer = EmotionRecognizer()
        self.emotional_history = defaultdict(list)
    
    def analyze_emotional_state(self, user_id: str, recent_texts: List[str]) -> Dict:
        """Analyze user's emotional state"""
        emotion_sequence = self.emotion_recognizer.recognize_emotion_sequence(recent_texts)
        
        # Store in history
        self.emotional_history[user_id].extend(emotion_sequence)
        
        # Calculate emotional patterns
        patterns = self.calculate_emotional_patterns(emotion_sequence)
        
        # Calculate emotional stability
        stability = self.calculate_emotional_stability(emotion_sequence)
        
        # Generate emotional insights
        insights = self.generate_emotional_insights(patterns, stability)
        
        return {
            'current_emotion': emotion_sequence[-1] if emotion_sequence else None,
            'patterns': patterns,
            'stability': stability,
            'insights': insights,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def calculate_emotional_patterns(self, emotion_sequence: List[Dict]) -> Dict:
        """Calculate emotional patterns over time"""
        if not emotion_sequence:
            return {}
        
        emotion_counts = defaultdict(int)
        for emotion_data in emotion_sequence:
            emotion = emotion_data['dominant_emotion']
            emotion_counts[emotion] += 1
        
        total = len(emotion_sequence)
        patterns = {
            emotion: count / total for emotion, count in emotion_counts.items()
        }
        
        return patterns
    
    def calculate_emotional_stability(self, emotion_sequence: List[Dict]) -> Dict:
        """Calculate emotional stability"""
        if len(emotion_sequence) < 2:
            return {'stability': 'unknown', 'volatility': 0}
        
        emotions = [e['dominant_emotion'] for e in emotion_sequence]
        
        # Count emotion changes
        changes = sum(1 for i in range(1, len(emotions)) if emotions[i] != emotions[i-1])
        
        volatility = changes / len(emotions)
        
        if volatility < 0.2:
            stability = 'stable'
        elif volatility < 0.5:
            stability = 'moderate'
        else:
            stability = 'volatile'
        
        return {
            'stability': stability,
            'volatility': volatility,
            'emotion_changes': changes
        }
    
    def generate_emotional_insights(self, patterns: Dict, stability: Dict) -> List[str]:
        """Generate emotional insights"""
        insights = []
        
        # Pattern-based insights
        if patterns.get('positive', 0) > 0.6:
            insights.append('User is in a consistently positive emotional state')
        
        if patterns.get('negative', 0) > 0.4:
            insights.append('User shows significant negative emotional patterns')
        
        if patterns.get('stressed', 0) > 0.3:
            insights.append('User may be experiencing elevated stress levels')
        
        # Stability-based insights
        if stability['stability'] == 'stable':
            insights.append('Emotional state is stable and consistent')
        elif stability['stability'] == 'volatile':
            insights.append('Emotional state shows high volatility - may need support')
        
        return insights

class EmpathyEngine:
    """Generate empathetic responses"""
    
    def __init__(self):
        self.empathy_templates = {
            'sad': [
                "I understand this is difficult for you.",
                "It's completely normal to feel this way.",
                "I'm here to support you through this."
            ],
            'stressed': [
                "I can see you're under a lot of pressure.",
                "Let's work through this together.",
                "Taking things one step at a time can help."
            ],
            'happy': [
                "It's great to see you in good spirits!",
                "Your positive energy is wonderful.",
                "Let's build on this momentum."
            ],
            'neutral': [
                "I'm here to help you with whatever you need.",
                "How can I best support you right now?",
                "I'm listening and ready to assist."
            ]
        }
    
    def generate_empathetic_response(self, emotion: str, context: str) -> str:
        """Generate empathetic response based on emotion"""
        if emotion in self.empathy_templates:
            templates = self.empathy_templates[emotion]
            import random
            return random.choice(templates)
        
        return "I'm here to help you."
    
    def adjust_response_tone(self, base_response: str, emotion: str) -> str:
        """Adjust response tone based on emotion"""
        if emotion == 'sad':
            return f"I understand. {base_response}"
        elif emotion == 'stressed':
            return f"Let's take this step by step. {base_response}"
        elif emotion == 'happy':
            return f"That's great! {base_response}"
        
        return base_response

class EmotionalSupportSystem:
    """Provide emotional support and recommendations"""
    
    def __init__(self):
        self.emotional_intelligence = EmotionalIntelligence()
        self.empathy_engine = EmpathyEngine()
        self.support_history = defaultdict(list)
    
    def provide_support(self, user_id: str, text: str, context: Dict = None) -> Dict:
        """Provide emotional support based on text"""
        # Recognize emotion
        emotion = self.emotional_intelligence.emotion_recognizer.recognize_emotion(text)
        
        # Generate empathetic response
        empathetic_response = self.empathy_engine.generate_empathetic_response(
            emotion['dominant_emotion'],
            text
        )
        
        # Generate support recommendations
        recommendations = self.generate_support_recommendations(emotion['dominant_emotion'])
        
        # Store support history
        self.support_history[user_id].append({
            'emotion': emotion,
            'response': empathetic_response,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'recognized_emotion': emotion,
            'empathetic_response': empathetic_response,
            'recommendations': recommendations,
            'provided_at': datetime.now().isoformat()
        }
    
    def generate_support_recommendations(self, emotion: str) -> List[str]:
        """Generate support recommendations based on emotion"""
        recommendations = {
            'sad': [
                'Consider talking to someone you trust',
                'Take some time for self-care',
                'Engage in activities you usually enjoy'
            ],
            'stressed': [
                'Take a short break to decompress',
                'Prioritize your most important tasks',
                'Practice deep breathing exercises'
            ],
            'tired': [
                'Ensure you\'re getting enough rest',
                'Consider a short nap if possible',
                'Light exercise can help boost energy'
            ],
            'energetic': [
                'Channel this energy into important tasks',
                'This is a great time for creative work',
                'Consider starting that project you\'ve been planning'
            ]
        }
        
        return recommendations.get(emotion, ['Take care of yourself'])

# For production, we'll implement:
# - Advanced emotion recognition using transformers
# - Facial expression analysis
# - Voice emotion detection
# - Physiological signal analysis
# - Long-term emotional trend analysis
# - Emotional contagion detection
# - Crisis detection and intervention
# - Personalized support strategies
# - Integration with mental health resources
# - Privacy controls for emotional data

if __name__ == '__main__':
    print("Emotional intelligence system ready")
