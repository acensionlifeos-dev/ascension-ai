"""
Ascension AI - Simple Serving Script
Serve the model via HTTP API
"""

import http.server
import socketserver
import json
import torch
import sys
import os
from urllib.parse import urlparse, parse_qs

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from architecture.transformer import AscensionTransformer, get_model_config
from data.tokenizer import CharTokenizer

class AscensionHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for Ascension AI API"""
    
    def __init__(self, *args, **kwargs):
        self.model = None
        self.tokenizer = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        super().__init__(*args, **kwargs)
    
    def load_model(self):
        """Load model on first request"""
        if self.model is not None:
            return
        
        print("Loading model...")
        
        # Load tokenizer
        self.tokenizer = CharTokenizer()
        
        # Load model
        config = get_model_config('nano')
        config.vocab_size = self.tokenizer.vocab_size
        self.model = AscensionTransformer(config)
        
        # Load checkpoint if exists
        checkpoint_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'checkpoints', 'epoch_5.pt')
        if os.path.exists(checkpoint_path):
            checkpoint = torch.load(checkpoint_path)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            print(f"Loaded checkpoint from {checkpoint_path}")
        else:
            print("No checkpoint found, using random weights")
        
        self.model = self.model.to(self.device)
        self.model.eval()
        print("Model loaded")
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Ascension AI API", "status": "ready"}).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "device": self.device}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/generate':
            self.load_model()
            
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request = json.loads(post_data.decode('utf-8'))
            
            # Get parameters
            prompt = request.get('prompt', '')
            max_new_tokens = request.get('max_new_tokens', 50)
            temperature = request.get('temperature', 0.8)
            
            # Tokenize
            input_tokens = self.tokenizer.encode(prompt, max_length=128)
            input_tensor = torch.tensor([input_tokens], dtype=torch.long).to(self.device)
            
            # Generate
            import time
            start_time = time.time()
            with torch.no_grad():
                generated = self.model.generate(input_tensor, max_new_tokens=max_new_tokens, temperature=temperature)
            generation_time = (time.time() - start_time) * 1000
            
            # Decode
            generated_text = self.tokenizer.decode(generated[0].tolist())
            
            # Send response
            response = {
                "content": generated_text,
                "model": "ascension-nano",
                "tokens_generated": max_new_tokens,
                "generation_time_ms": generation_time
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def main():
    """Run the server"""
    PORT = 8000
    print(f"Starting Ascension AI API on port {PORT}")
    
    with socketserver.TCPServer(("", PORT), AscensionHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
