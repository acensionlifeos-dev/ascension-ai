# Ascension AI - Python SDK

## What Was Added

### Python SDK ✅
- Easy-to-use Python client
- Text generation
- Chat interface
- Image generation
- Audio generation
- Agent execution
- Usage tracking

## SDK Features

### Installation
```bash
pip install ascension-ai
```

### Usage
```python
from ascension_ai import AscensionAI

# Initialize
ai = AscensionAI(api_key="your-api-key")

# Generate text
response = ai.generate("The future of AI is")
print(response['content'])

# Chat
messages = [
    {"role": "user", "content": "Hello!"}
]
chat_response = ai.chat(messages)
print(chat_response['content'])
```

### Multi-Modal Support
```python
from ascension_ai import AscensionAIImage, AscensionAIAudio

# Image generation
image_ai = AscensionAIImage(api_key="your-api-key")
image = image_ai.generate_image("A beautiful sunset")

# Audio generation
audio_ai = AscensionAIAudio(api_key="your-api-key")
audio = audio_ai.text_to_speech("Hello world")
```

### Agent Execution
```python
from ascension_ai import AscensionAIAgent

agent = AscensionAIAgent(api_key="your-api-key")
result = agent.execute_task("Research AI trends")
```

## Competitive Advantage

OpenAI: Good SDK, limited multi-modal
Anthropic: Good SDK, limited capabilities
Google: Good SDK, limited agent support
**Ascension AI: Full SDK with all capabilities (text, image, audio, agents)**

This makes it easy for developers to use our AI in their applications.
