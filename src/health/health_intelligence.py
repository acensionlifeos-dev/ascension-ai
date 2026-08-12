"""
Ascension AI - Health and Wellness Intelligence
Advanced health monitoring, wellness planning, and medical assistance
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
from collections import defaultdict

class HealthData:
    """Store and process health data"""
    
    def __init__(self):
        self.health_data = defaultdict(list)
        self.wearable_data = {}
    
    def record_vitals(self, user_id: str, vitals: Dict) -> Dict:
        """Record vital signs"""
        data = {
            'vitals': vitals,
            'recorded_at': datetime.now().isoformat()
        }
        
        self.health_data[user_id].append(data)
        
        return {
            'user_id': user_id,
            'vitals': vitals,
            'recorded_at': data['recorded_at']
        }
    
    def record_sleep(self, user_id: str, sleep_data: Dict) -> Dict:
        """Record sleep data"""
        data = {
            'sleep': sleep_data,
            'recorded_at': datetime.now().isoformat()
        }
        
        self.health_data[user_id].append(data)
        
        return data
    
    def record_activity(self, user_id: str, activity_data: Dict) -> Dict:
        """Record physical activity"""
        data = {
            'activity': activity_data,
            'recorded_at': datetime.now().isoformat()
        }
        
        self.health_data[user_id].append(data)
        
        return data

class WellnessPlanner:
    """Create personalized wellness plans"""
    
    def __init__(self):
        self.wellness_domains = {
            'sleep': self.plan_sleep,
            'nutrition': self.plan_nutrition,
            'exercise': self.plan_exercise,
            'stress': self.plan_stress,
            'mental': self.plan_mental
        }
    
    def create_wellness_plan(self, user_id: str, health_data: Dict, goals: List[str]) -> Dict:
        """Create personalized wellness plan"""
        plan = {
            'user_id': user_id,
            'goals': goals,
            'created_at': datetime.now().isoformat()
        }
        
        for goal in goals:
            if goal in self.wellness_domains:
                plan[goal] = self.wellness_domains[goal](user_id, health_data)
        
        return plan
    
    def plan_sleep(self, user_id: str, health_data: Dict) -> Dict:
        """Plan sleep improvements"""
        return {
            'target_hours': 8,
            'bedtime': '10:30 PM',
            'wake_time': '6:30 AM',
            'recommendations': [
                'Maintain consistent sleep schedule',
                'Avoid screens 1 hour before bed',
                'Keep bedroom cool and dark',
                'Limit caffeine after 2 PM'
            ]
        }
    
    def plan_nutrition(self, user_id: str, health_data: Dict) -> Dict:
        """Plan nutrition improvements"""
        return {
            'daily_calories': 2000,
            'protein': '120g',
            'carbs': '250g',
            'fats': '70g',
            'recommendations': [
                'Eat whole foods',
                'Stay hydrated',
                'Limit processed sugar',
                'Include vegetables with every meal'
            ]
        }
    
    def plan_exercise(self, user_id: str, health_data: Dict) -> Dict:
        """Plan exercise routine"""
        return {
            'weekly_minutes': 150,
            'cardio_days': 3,
            'strength_days': 2,
            'recommendations': [
                'Start with 30-minute walks',
                'Add strength training twice weekly',
                'Include flexibility work',
                'Track progress weekly'
            ]
        }
    
    def plan_stress(self, user_id: str, health_data: Dict) -> Dict:
        """Plan stress management"""
        return {
            'daily_practices': [
                '10-minute meditation',
                'Deep breathing exercises',
                'Nature walks',
                'Journaling'
            ]
        }
    
    def plan_mental(self, user_id: str, health_data: Dict) -> Dict:
        """Plan mental health support"""
        return {
            'practices': [
                'Daily reflection',
                'Gratitude practice',
                'Social connection',
                'Professional support when needed'
            ]
        }

class SymptomChecker:
    """Check symptoms and provide guidance"""
    
    def __init__(self):
        self.urgent_symptoms = [
            'chest pain', 'difficulty breathing', 'severe bleeding',
            'loss of consciousness', 'severe headache', 'high fever'
        ]
    
    def check_symptoms(self, user_id: str, symptoms: List[str]) -> Dict:
        """Check symptoms and provide guidance"""
        # Check for urgent symptoms
        urgent = [s for s in symptoms if any(us in s.lower() for us in self.urgent_symptoms)]
        
        if urgent:
            return {
                'user_id': user_id,
                'urgent_symptoms': urgent,
                'advice': 'Seek immediate medical attention or call emergency services.',
                'disclaimer': 'This is not medical advice. Call emergency services for serious symptoms.',
                'timestamp': datetime.now().isoformat()
            }
        
        # General guidance
        return {
            'user_id': user_id,
            'symptoms': symptoms,
            'advice': 'Monitor your symptoms and consider consulting a healthcare provider if they persist or worsen.',
            'self_care': [
                'Rest and stay hydrated',
                'Monitor symptom changes',
                'Consider over-the-counter remedies if appropriate',
                'Consult a doctor if symptoms persist'
            ],
            'disclaimer': 'This is not medical advice. Consult a healthcare professional.',
            'timestamp': datetime.now().isoformat()
        }

class HealthIntelligence:
    """Integrated health and wellness intelligence"""
    
    def __init__(self):
        self.health_data = HealthData()
        self.wellness_planner = WellnessPlanner()
        self.symptom_checker = SymptomChecker()
    
    def analyze_health(self, user_id: str, data: Dict) -> Dict:
        """Analyze overall health"""
        vitals = data.get('vitals', {})
        sleep = data.get('sleep', {})
        activity = data.get('activity', {})
        
        # Record data
        self.health_data.record_vitals(user_id, vitals)
        self.health_data.record_sleep(user_id, sleep)
        self.health_data.record_activity(user_id, activity)
        
        # Generate insights
        insights = self.generate_health_insights(vitals, sleep, activity)
        
        # Create wellness plan
        wellness_plan = self.wellness_planner.create_wellness_plan(user_id, data, ['sleep', 'nutrition', 'exercise', 'stress'])
        
        return {
            'user_id': user_id,
            'insights': insights,
            'wellness_plan': wellness_plan,
            'analyzed_at': datetime.now().isoformat(),
            'disclaimer': 'This is wellness guidance, not medical diagnosis. Consult healthcare professionals.'
        }
    
    def generate_health_insights(self, vitals: Dict, sleep: Dict, activity: Dict) -> List[str]:
        """Generate health insights"""
        insights = []
        
        if sleep.get('hours', 0) < 7:
            insights.append('Sleep duration is below recommended 7-9 hours')
        
        if activity.get('minutes', 0) < 30:
            insights.append('Daily activity is below 30 minutes')
        
        if vitals.get('heart_rate', 70) > 100:
            insights.append('Resting heart rate is elevated')
        
        return insights

# For production, we will implement:
# - Medical disclaimer and safety checks
# - Wearable device integrations (Oura, Fitbit, Apple Watch)
# - HIPAA compliance and privacy
# - Real-time vitals monitoring
# - Symptom-to-condition mapping (not diagnosis)
# - Telehealth integration
# - Prescription tracking
# - Appointment reminders
# - Mental health crisis detection
# - Nutrition database integration
# - Exercise form analysis
# - Sleep stage analysis

if __name__ == '__main__':
    print("Health and wellness intelligence ready")
