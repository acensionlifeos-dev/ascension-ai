"""
Ascension AI - Minimal Transformer Implementation
A simple, trainable transformer model that can be scaled to production.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Optional
import math

@dataclass
class ModelConfig:
    """Configuration for Ascension Transformer model"""
    vocab_size: int = 50000
    max_length: int = 512
    num_layers: int = 6
    num_heads: int = 8
    hidden_size: int = 256
    ff_size: int = 1024
    dropout: float = 0.1
    # Scaling to larger models
    # Small (1B): num_layers=24, num_heads=16, hidden_size=1024, ff_size=4096
    # Medium (7B): num_layers=32, num_heads=32, hidden_size=2048, ff_size=8192
    # Large (13B): num_layers=40, num_heads=40, hidden_size=2560, ff_size=10240
    # XL (70B): num_layers=80, num_heads=64, hidden_size=4096, ff_size=16384

class MultiHeadAttention(nn.Module):
    """Multi-head self-attention mechanism"""
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.num_heads = config.num_heads
        self.head_dim = config.hidden_size // config.num_heads
        if config.hidden_size % config.num_heads != 0:
            raise ValueError("hidden_size must be divisible by num_heads")
        
        self.qkv = nn.Linear(config.hidden_size, config.hidden_size * 3)
        self.out = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(config.dropout)
        self.scale = self.head_dim ** -0.5
        self.register_buffer(
            "causal_mask",
            torch.tril(torch.ones(config.max_length, config.max_length, dtype=torch.bool))
            .view(1, 1, config.max_length, config.max_length),
            persistent=False,
        )
    
    def forward(self, x, mask=None):
        B, T, C = x.shape
        if T > self.causal_mask.size(-1):
            raise ValueError(
                f"sequence length {T} exceeds configured maximum {self.causal_mask.size(-1)}"
            )
        
        # Generate Q, K, V
        qkv = self.qkv(x).reshape(B, T, 3, self.num_heads, self.head_dim)
        q, k, v = qkv.unbind(2)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        
        # Attention
        attn = (q @ k.transpose(-2, -1)) * self.scale
        allowed = self.causal_mask[:, :, :T, :T]
        if mask is not None:
            external = mask.to(device=x.device, dtype=torch.bool)
            if external.ndim == 2 and external.shape == (B, T):
                external = external[:, None, None, :]
            elif external.ndim == 2 and external.shape == (T, T):
                external = external[None, None, :, :]
            elif external.ndim == 3:
                external = external[:, None, :, :]
            if external.ndim != 4:
                raise ValueError("attention mask must be [batch, sequence], [sequence, sequence], or broadcastable 4D")
            allowed = allowed & external
        attn = attn.masked_fill(~allowed, torch.finfo(attn.dtype).min)
        
        attn = F.softmax(attn, dim=-1)
        attn = self.dropout(attn)
        
        # Output
        out = (attn @ v).transpose(1, 2).contiguous().reshape(B, T, C)
        return self.out(out)

class FeedForward(nn.Module):
    """Feed-forward network"""
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.hidden_size, config.ff_size),
            nn.GELU(),
            nn.Linear(config.ff_size, config.hidden_size),
            nn.Dropout(config.dropout)
        )
    
    def forward(self, x):
        return self.net(x)

class TransformerBlock(nn.Module):
    """Transformer block with attention and feed-forward"""
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.attention = MultiHeadAttention(config)
        self.ff = FeedForward(config)
        self.ln1 = nn.LayerNorm(config.hidden_size)
        self.ln2 = nn.LayerNorm(config.hidden_size)
    
    def forward(self, x, mask=None):
        x = x + self.attention(self.ln1(x), mask)
        x = x + self.ff(self.ln2(x))
        return x

class AscensionTransformer(nn.Module):
    """Main Ascension Transformer model"""
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.config = config
        
        # Embeddings
        self.token_embedding = nn.Embedding(config.vocab_size, config.hidden_size)
        self.position_embedding = nn.Embedding(config.max_length, config.hidden_size)
        self.dropout = nn.Dropout(config.dropout)
        
        # Transformer blocks
        self.blocks = nn.ModuleList([
            TransformerBlock(config) for _ in range(config.num_layers)
        ])
        
        # Output layer
        self.ln = nn.LayerNorm(config.hidden_size)
        self.output = nn.Linear(config.hidden_size, config.vocab_size)
        
        # Initialize weights
        self.apply(self._init_weights)
    
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
    
    def forward(self, input_ids, mask=None):
        B, T = input_ids.shape
        
        # Embeddings
        token_emb = self.token_embedding(input_ids)
        pos_emb = self.position_embedding(torch.arange(T, device=input_ids.device))
        x = self.dropout(token_emb + pos_emb)
        
        # Transformer blocks
        for block in self.blocks:
            x = block(x, mask)
        
        # Output
        x = self.ln(x)
        logits = self.output(x)
        
        return logits
    
    def generate(self, input_ids, max_new_tokens, temperature=1.0, top_k=None):
        """Generate text autoregressively"""
        for _ in range(max_new_tokens):
            # Forward pass
            logits = self(input_ids[:, -self.config.max_length:])
            
            # Get last token logits
            logits = logits[:, -1, :] / temperature
            
            # Top-k filtering
            if top_k is not None:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = -float('inf')
            
            # Sample
            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            
            # Append
            input_ids = torch.cat([input_ids, next_token], dim=1)
        
        return input_ids

def get_model_config(size: str = 'nano') -> ModelConfig:
    """Get model configuration for different sizes"""
    configs = {
        'nano': ModelConfig(
            vocab_size=50000,
            max_length=512,
            num_layers=6,
            num_heads=8,
            hidden_size=256,
            ff_size=1024
        ),
        'small': ModelConfig(
            vocab_size=50000,
            max_length=2048,
            num_layers=24,
            num_heads=16,
            hidden_size=1024,
            ff_size=4096
        ),
        'medium': ModelConfig(
            vocab_size=50000,
            max_length=2048,
            num_layers=32,
            num_heads=32,
            hidden_size=2048,
            ff_size=8192
        ),
        'large': ModelConfig(
            vocab_size=50000,
            max_length=2048,
            num_layers=40,
            num_heads=40,
            hidden_size=2560,
            ff_size=10240
        ),
        'xl': ModelConfig(
            vocab_size=50000,
            max_length=2048,
            num_layers=80,
            num_heads=64,
            hidden_size=4096,
            ff_size=16384
        )
    }
    return configs.get(size, configs['nano'])

if __name__ == '__main__':
    # Test the model
    config = get_model_config('nano')
    model = AscensionTransformer(config)
    
    # Forward pass
    input_ids = torch.randint(0, config.vocab_size, (1, 10))
    logits = model(input_ids)
    print(f"Model output shape: {logits.shape}")
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Generation
    generated = model.generate(input_ids, max_new_tokens=20)
    print(f"Generated shape: {generated.shape}")
