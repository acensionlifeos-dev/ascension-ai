"""
Ascension AI - Model Serving
Serve trained models via API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import torch
import sys
import os

# Simple import fix
import importlib.util
spec = importlib.util.spec_from_file_location("transformer", os.path.join(os.path.dirname(__file__), "..", "architecture", "transformer.py"))
transformer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transformer_module)
AscensionTransformer = transformer_module.AscensionTransformer
get_model_config = transformer_module.get_model_config

spec2 = importlib.util.spec_from_file_location("tokenizer", os.path.join(os.path.dirname(__file__), "..", "data", "tokenizer.py"))
tokenizer_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(tokenizer_module)
CharTokenizer = tokenizer_module.CharTokenizer

app = FastAPI(title="Ascension AI API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = None
tokenizer = None
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class GenerationRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50
    temperature: float = 0.8
    top_k: Optional[int] = None

class GenerationResponse(BaseModel):
    content: str
    model: str
    tokens_generated: int
    generation_time_ms: float

@app.on_event("startup")
async def load_model():
    """Load model on startup"""
    global model, tokenizer
    
    print("Loading Ascension AI model...")
    
    # Load tokenizer
    tokenizer = CharTokenizer()  # In production, load trained tokenizer
    
    # Load model configuration
    config = get_model_config('nano')
    config.vocab_size = tokenizer.vocab_size
    
    # Load model
    model = AscensionTransformer(config)
    
    # Load checkpoint if exists
    checkpoint_path = 'models/checkpoints/epoch_5.pt'
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        print(f"Loaded checkpoint from {checkpoint_path}")
    else:
        print("No checkpoint found, using random weights")
    
    model = model.to(device)
    model.eval()
    
    print("Model loaded successfully")

@app.get("/")
async def root():
    return {"message": "Ascension AI API", "status": "ready"}

@app.get("/health")
async def health():
    return {"status": "healthy", "device": device}

@app.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    """Generate text"""
    import time
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.time()
    
    # Tokenize input
    input_tokens = tokenizer.encode(request.prompt, max_length=128)
    input_tensor = torch.tensor([input_tokens], dtype=torch.long).to(device)
    
    # Generate
    with torch.no_grad():
        generated = model.generate(
            input_tensor,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_k=request.top_k
        )
    
    # Decode
    generated_text = tokenizer.decode(generated[0].tolist())
    generation_time = (time.time() - start_time) * 1000
    
    return GenerationResponse(
        content=generated_text,
        model="ascension-nano",
        tokens_generated=request.max_new_tokens,
        generation_time_ms=generation_time
    )

@app.get("/model/info")
async def model_info():
    """Get model information"""
    if model is None:
        return {"status": "not_loaded"}
    
    num_params = sum(p.numel() for p in model.parameters())
    
    return {
        "model": "ascension-nano",
        "parameters": num_params,
        "device": device,
        "vocab_size": tokenizer.vocab_size if tokenizer else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
