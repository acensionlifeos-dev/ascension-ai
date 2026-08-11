"""
Ascension AI - Model Serving
Serve trained models via API
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Mount static files
app.mount("/static", StaticFiles(directory="public"), name="static")

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
    
    # Load tokenizer with sample data
    sample_texts = ["The quick brown fox", "Machine learning", "Ascension AI", "The future of AI", "Building the best AI"]
    tokenizer = CharTokenizer(sample_texts)
    
    # Load model configuration
    config = get_model_config('nano')
    config.vocab_size = tokenizer.vocab_size
    
    # Load model
    model = AscensionTransformer(config)
    
    # For demo, use random weights (no checkpoint needed)
    print("Using demo mode with random weights")
    
    model = model.to(device)
    model.eval()
    
    print("Model loaded successfully")

@app.get("/")
async def root():
    """Serve the frontend"""
    return FileResponse('public/index.html')

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
        "vocab_size": tokenizer.vocab_size if tokenizer else 0,
        "mode": "demo"
    }

@app.post("/document/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """Analyze uploaded document"""
    try:
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Import document analyzer
        import importlib.util
        spec = importlib.util.spec_from_file_location("document_analysis", os.path.join(os.path.dirname(__file__), "..", "documents", "document_analysis.py"))
        doc_analysis_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(doc_analysis_module)
        DocumentAnalyzer = doc_analysis_module.DocumentAnalyzer
        
        # Analyze document
        analyzer = DocumentAnalyzer()
        analysis = analyzer.analyze_document(file.filename, text_content)
        
        return {
            "file_name": file.filename,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/document/recreate")
async def recreate_document(file: UploadFile = File(...), style: str = "original"):
    """Recreate uploaded document"""
    try:
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Import document analyzer and recreator
        import importlib.util
        spec = importlib.util.spec_from_file_location("document_analysis", os.path.join(os.path.dirname(__file__), "..", "documents", "document_analysis.py"))
        doc_analysis_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(doc_analysis_module)
        DocumentAnalyzer = doc_analysis_module.DocumentAnalyzer
        DocumentRecreator = doc_analysis_module.DocumentRecreator
        
        # Analyze document
        analyzer = DocumentAnalyzer()
        analysis = analyzer.analyze_document(file.filename, text_content)
        analysis['content'] = text_content
        
        # Recreate document
        recreator = DocumentRecreator()
        recreation = recreator.recreate_document(analysis, style)
        
        return {
            "file_name": file.filename,
            "style": style,
            "recreation": recreation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
