"""
Ascension AI - Memory System
Long-term memory across sessions for personalized AI
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

class MemoryBank:
    """Long-term memory storage"""
    
    def __init__(self, memory_path: str = "models/memory_bank.json"):
        self.memory_path = memory_path
        self.memory = self.load_memory()
    
    def load_memory(self) -> Dict:
        """Load memory from disk"""
        if os.path.exists(self.memory_path):
            with open(self.memory_path, 'r') as f:
                return json.load(f)
        return {
            'episodic': [],  # Specific events
            'semantic': [],  # General knowledge
            'procedural': [],  # Skills and procedures
            'user_preferences': {}
        }
    
    def save_memory(self):
        """Save memory to disk"""
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        with open(self.memory_path, 'w') as f:
            json.dump(self.memory, f)
    
    def add_episodic_memory(self, event: str, context: Dict):
        """Add an episodic memory (specific event)"""
        self.memory['episodic'].append({
            'event': event,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'importance': 1.0
        })
        self.save_memory()
    
    def add_semantic_memory(self, fact: str, confidence: float = 1.0):
        """Add semantic memory (general knowledge)"""
        self.memory['semantic'].append({
            'fact': fact,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
        self.save_memory()
    
    def add_procedural_memory(self, skill: str, procedure: List[str]):
        """Add procedural memory (skill/procedure)"""
        self.memory['procedural'].append({
            'skill': skill,
            'procedure': procedure,
            'timestamp': datetime.now().isoformat()
        })
        self.save_memory()
    
    def update_user_preference(self, key: str, value: any):
        """Update user preference"""
        self.memory['user_preferences'][key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        self.save_memory()
    
    def retrieve_relevant_memories(self, query: str, memory_type: str = 'all', top_k: int = 5) -> List[Dict]:
        """Retrieve relevant memories based on query"""
        relevant = []
        
        if memory_type in ['all', 'episodic']:
            for mem in self.memory['episodic']:
                if query.lower() in mem['event'].lower():
                    relevant.append(mem)
        
        if memory_type in ['all', 'semantic']:
            for mem in self.memory['semantic']:
                if query.lower() in mem['fact'].lower():
                    relevant.append(mem)
        
        if memory_type in ['all', 'procedural']:
            for mem in self.memory['procedural']:
                if query.lower() in mem['skill'].lower():
                    relevant.append(mem)
        
        # Sort by importance/recency
        relevant.sort(key=lambda x: x.get('importance', 0.5), reverse=True)
        
        return relevant[:top_k]
    
    def get_user_preferences(self) -> Dict:
        """Get all user preferences"""
        return self.memory['user_preferences']

class PersonalizationEngine:
    """Personalizes AI behavior based on user interactions"""
    
    def __init__(self, memory_bank: MemoryBank):
        self.memory_bank = memory_bank
        self.user_profile = self.build_user_profile()
    
    def build_user_profile(self) -> Dict:
        """Build user profile from memory"""
        preferences = self.memory_bank.get_user_preferences()
        
        profile = {
            'communication_style': preferences.get('communication_style', 'balanced'),
            'complexity_level': preferences.get('complexity_level', 'medium'),
            'preferred_topics': preferences.get('preferred_topics', []),
            'avoided_topics': preferences.get('avoided_topics', []),
            'interaction_patterns': self.analyze_patterns()
        }
        
        return profile
    
    def analyze_patterns(self) -> Dict:
        """Analyze user interaction patterns"""
        episodic = self.memory_bank.memory['episodic']
        
        patterns = {
            'most_common_topics': [],
            'interaction_frequency': {},
            'peak_times': []
        }
        
        # Analyze topics
        topic_counts = {}
        for mem in episodic[-100:]:
            event = mem['event'].lower()
            # Simple topic extraction
            for word in event.split():
                if len(word) > 3:
                    topic_counts[word] = topic_counts.get(word, 0) + 1
        
        patterns['most_common_topics'] = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return patterns
    
    def personalize_response(self, response: str) -> str:
        """Personalize response based on user profile"""
        profile = self.user_profile
        
        # Adjust complexity
        if profile['complexity_level'] == 'simple':
            response = self.simplify_response(response)
        elif profile['complexity_level'] == 'advanced':
            response = self.enhance_response(response)
        
        # Adjust style
        if profile['communication_style'] == 'concise':
            response = self.make_concise(response)
        elif profile['communication_style'] == 'detailed':
            response = self.add_detail(response)
        
        return response
    
    def simplify_response(self, response: str) -> str:
        """Simplify response for simple complexity level"""
        # In production, use NLP to simplify
        return response
    
    def enhance_response(self, response: str) -> str:
        """Enhance response for advanced complexity level"""
        # In production, add more detail and nuance
        return response
    
    def make_concise(self, response: str) -> str:
        """Make response more concise"""
        # In production, summarize
        return response
    
    def add_detail(self, response: str) -> str:
        """Add more detail to response"""
        # In production, expand with examples
        return response
    
    def update_from_interaction(self, interaction: Dict):
        """Update personalization from interaction"""
        # In production, learn from interaction
        pass

class ContextualMemory:
    """Context-aware memory for current session"""
    
    def __init__(self, max_context_length: int = 10):
        self.max_context_length = max_context_length
        self.context_window = []
    
    def add_context(self, user_input: str, ai_response: str):
        """Add interaction to context window"""
        self.context_window.append({
            'user': user_input,
            'ai': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent context
        if len(self.context_window) > self.max_context_length:
            self.context_window = self.context_window[-self.max_context_length:]
    
    def get_context(self) -> List[Dict]:
        """Get current context"""
        return self.context_window
    
    def clear_context(self):
        """Clear context window"""
        self.context_window = []
    
    def get_context_summary(self) -> str:
        """Get summary of current context"""
        if not self.context_window:
            return "No context available"
        
        summary = "Recent conversation:\n"
        for ctx in self.context_window[-3:]:
            summary += f"User: {ctx['user']}\nAI: {ctx['ai']}\n"
        
        return summary

class PersonalizedAI:
    """AI with personalization and memory"""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        
        # Initialize memory systems
        self.memory_bank = MemoryBank()
        self.personalization = PersonalizationEngine(self.memory_bank)
        self.contextual_memory = ContextualMemory()
    
    def generate_response(self, user_input: str) -> str:
        """Generate personalized response"""
        # Retrieve relevant memories
        relevant_memories = self.memory_bank.retrieve_relevant_memories(user_input)
        
        # Get current context
        context = self.contextual_memory.get_context_summary()
        
        # Generate base response
        base_response = self.generate_base_response(user_input, context, relevant_memories)
        
        # Personalize response
        personalized_response = self.personalization.personalize_response(base_response)
        
        # Update context
        self.contextual_memory.add_context(user_input, personalized_response)
        
        # Store episodic memory
        self.memory_bank.add_episodic_memory(user_input, {'response': personalized_response})
        
        return personalized_response
    
    def generate_base_response(self, user_input: str, context: str, memories: List[Dict]) -> str:
        """Generate base response using model"""
        # In production, use the actual model
        # For now, return a simple response
        return f"Based on your input: {user_input} and context: {len(memories)} relevant memories"

# For production, we'll implement:
- Vector embeddings for semantic search
- Memory consolidation during sleep
- Memory importance scoring
- Forgetting mechanism for old memories
- Cross-session memory persistence
- Privacy controls for memory storage

if __name__ == '__main__':
    print("Memory system ready")
