"""
Ascension AI - Python SDK
Easy-to-use Python client for Ascension AI
"""

import requests
from typing import Dict, List, Optional
import json

class AscensionAI:
    """Python SDK for Ascension AI"""
    
    def __init__(self, api_key: str, base_url: str = "https://ascension-ai.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def generate(self, prompt: str, max_tokens: int = 50, temperature: float = 0.8) -> Dict:
        """Generate text from prompt"""
        response = self.session.post(
            f'{self.base_url}/generate',
            json={
                'prompt': prompt,
                'max_new_tokens': max_tokens,
                'temperature': temperature
            }
        )
        response.raise_for_status()
        return response.json()
    
    def chat(self, messages: List[Dict], temperature: float = 0.8) -> Dict:
        """Chat with the AI"""
        # Convert messages to prompt
        prompt = '\n'.join([f"{m['role']}: {m['content']}" for m in messages])
        
        response = self.session.post(
            f'{self.base_url}/generate',
            json={
                'prompt': prompt,
                'max_new_tokens': 200,
                'temperature': temperature
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        response = self.session.get(f'{self.base_url}/model/info')
        response.raise_for_status()
        return response.json()
    
    def get_capabilities(self) -> Dict:
        """Get available capabilities"""
        response = self.session.get(f'{self.base_url}/capabilities')
        response.raise_for_status()
        return response.json()
    
    def get_usage(self) -> Dict:
        """Get usage statistics"""
        response = self.session.get(f'{self.base_url}/usage')
        response.raise_for_status()
        return response.json()

class AscensionAIImage:
    """Image generation SDK"""
    
    def __init__(self, api_key: str, base_url: str = "https://ascension-ai.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def generate_image(self, prompt: str, size: str = "512x512") -> Dict:
        """Generate image from prompt"""
        response = self.session.post(
            f'{self.base_url}/image/generate',
            json={
                'prompt': prompt,
                'size': size
            }
        )
        response.raise_for_status()
        return response.json()

class AscensionAIAudio:
    """Audio generation SDK"""
    
    def __init__(self, api_key: str, base_url: str = "https://ascension-ai.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def text_to_speech(self, text: str, voice: str = "default") -> Dict:
        """Convert text to speech"""
        response = self.session.post(
            f'{self.base_url}/audio/tts',
            json={
                'text': text,
                'voice': voice
            }
        )
        response.raise_for_status()
        return response.json()

class AscensionAIAgent:
    """Agent execution SDK"""
    
    def __init__(self, api_key: str, base_url: str = "https://ascension-ai.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def execute_task(self, goal: str) -> Dict:
        """Execute a task using agents"""
        response = self.session.post(
            f'{self.base_url}/agent/execute',
            json={
                'goal': goal
            }
        )
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == '__main__':
    # Initialize client
    ai = AscensionAI(api_key="your-api-key")
    
    # Generate text
    response = ai.generate("The future of AI is")
    print(response)
    
    # Chat
    messages = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I help?"}
    ]
    chat_response = ai.chat(messages)
    print(chat_response)
