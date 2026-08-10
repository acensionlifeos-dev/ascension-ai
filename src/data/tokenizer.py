"""
Ascension AI - Tokenizer
Efficient tokenizer for training Ascension models
"""

import json
from collections import Counter
from typing import List, Dict, Optional
import pickle
import os

class AscensionTokenizer:
    """BPE-style tokenizer for Ascension AI"""
    
    def __init__(self, vocab_size: int = 50000):
        self.vocab_size = vocab_size
        self.vocab = {}
        self.inverse_vocab = {}
        self.merges = []
        self.special_tokens = {
            '<pad>': 0,
            '<unk>': 1,
            '<bos>': 2,
            '<eos>': 3
        }
    
    def train(self, texts: List[str], min_frequency: int = 2):
        """Train tokenizer on texts"""
        print(f"Training tokenizer on {len(texts)} texts...")
        
        # Build initial character vocabulary
        word_counts = Counter()
        for text in texts:
            words = text.split()
            word_counts.update(words)
        
        # Add special tokens
        for token, idx in self.special_tokens.items():
            self.vocab[token] = idx
            self.inverse_vocab[idx] = token
        
        # Add frequent words
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        for word, count in sorted_words[:self.vocab_size - len(self.special_tokens)]:
            if count >= min_frequency:
                idx = len(self.vocab)
                self.vocab[word] = idx
                self.inverse_vocab[idx] = word
        
        print(f"Tokenizer trained with {len(self.vocab)} tokens")
    
    def encode(self, text: str, max_length: Optional[int] = None) -> List[int]:
        """Encode text to token IDs"""
        tokens = text.split()
        encoded = []
        
        for token in tokens:
            if token in self.vocab:
                encoded.append(self.vocab[token])
            else:
                # Handle unknown tokens (split into characters)
                for char in token:
                    if char in self.vocab:
                        encoded.append(self.vocab[char])
                    else:
                        encoded.append(self.special_tokens['<unk>'])
        
        if max_length and len(encoded) > max_length:
            encoded = encoded[:max_length]
        
        return encoded
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs to text"""
        tokens = []
        for token_id in token_ids:
            if token_id in self.inverse_vocab:
                tokens.append(self.inverse_vocab[token_id])
        return ' '.join(tokens)
    
    def save(self, path: str):
        """Save tokenizer to disk"""
        with open(path, 'wb') as f:
            pickle.dump({
                'vocab': self.vocab,
                'inverse_vocab': self.inverse_vocab,
                'merges': self.merges,
                'special_tokens': self.special_tokens,
                'vocab_size': self.vocab_size
            }, f)
        print(f"Tokenizer saved to {path}")
    
    def load(self, path: str):
        """Load tokenizer from disk"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.vocab = data['vocab']
            self.inverse_vocab = data['inverse_vocab']
            self.merges = data['merges']
            self.special_tokens = data['special_tokens']
            self.vocab_size = data['vocab_size']
        print(f"Tokenizer loaded from {path}")

# Character-level tokenizer for demonstration
class CharTokenizer:
    """Simple character-level tokenizer"""
    
    def __init__(self, texts: Optional[List[str]] = None):
        if texts:
            self.build_vocab(texts)
        else:
            self.char_to_idx = {}
            self.idx_to_char = {}
            self.vocab_size = 0
    
    def build_vocab(self, texts: List[str]):
        """Build vocabulary from texts"""
        chars = set(''.join(texts))
        self.char_to_idx = {c: i for i, c in enumerate(sorted(chars))}
        self.idx_to_char = {i: c for c, i in self.char_to_idx.items()}
        self.vocab_size = len(self.char_to_idx)
        print(f"Character tokenizer built with {self.vocab_size} characters")
    
    def encode(self, text: str, max_length: Optional[int] = None) -> List[int]:
        """Encode text to character IDs"""
        encoded = [self.char_to_idx.get(c, 0) for c in text]
        if max_length and len(encoded) > max_length:
            encoded = encoded[:max_length]
        return encoded
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode character IDs to text"""
        return ''.join([self.idx_to_char.get(idx, '') for idx in token_ids])

# For production, we'll use:
# - SentencePiece (subword tokenization)
# - HuggingFace tokenizers
# - Custom BPE implementation

if __name__ == '__main__':
    # Test tokenizer
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is transforming the world.",
        "Ascension AI is building the future."
    ]
    
    tokenizer = AscensionTokenizer(vocab_size=100)
    tokenizer.train(texts)
    
    text = "The future of AI"
    encoded = tokenizer.encode(text)
    decoded = tokenizer.decode(encoded)
    
    print(f"Original: {text}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
