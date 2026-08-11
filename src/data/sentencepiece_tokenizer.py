"""
Ascension AI - Production Tokenizer
SentencePiece-based tokenizer for production training
"""

import sentencepiece as sp
from typing import List, Optional
import os

class SentencePieceTokenizer:
    """SentencePiece tokenizer for production use"""
    
    def __init__(self, model_path: Optional[str] = None, vocab_size: int = 50000):
        self.vocab_size = vocab_size
        self.sp = sp.SentencePieceProcessor()
        
        if model_path and os.path.exists(model_path):
            self.sp.load(model_path)
            print(f"Loaded SentencePiece model from {model_path}")
        else:
            print("SentencePiece model not found, will need to train")
    
    def train(self, texts: List[str], model_prefix: str = "ascension"):
        """Train SentencePiece tokenizer on texts"""
        import tempfile
        
        # Write texts to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            for text in texts:
                f.write(text + '\n')
            temp_file = f.name
        
        try:
            # Train SentencePiece model
            import subprocess
            cmd = [
                'spm_train',
                f'--input={temp_file}',
                f'--model_prefix={model_prefix}',
                f'--vocab_size={self.vocab_size}',
                '--model_type=bpe',
                '--max_sentence_length=512',
                '--shuffle_input_sentence=true',
                '--normalization_rule=nmt_nfkc',
                '--remove_extra_whitespaces=true',
                '--character_coverage=0.995',
                '--input_sentence_size=10000000'
            ]
            
            print("Training SentencePiece tokenizer...")
            subprocess.run(cmd, check=True)
            
            # Load trained model
            model_path = f'{model_prefix}.model'
            self.sp.load(model_path)
            print(f"Trained and loaded SentencePiece model: {model_path}")
            
            return model_path
        finally:
            os.unlink(temp_file)
    
    def encode(self, text: str, max_length: Optional[int] = None) -> List[int]:
        """Encode text to token IDs"""
        tokens = self.sp.encode(text, out_type=int)
        if max_length and len(tokens) > max_length:
            tokens = tokens[:max_length]
        return tokens
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs to text"""
        return self.sp.decode(token_ids)
    
    def get_vocab_size(self) -> int:
        """Get vocabulary size"""
        return self.sp.get_piece_size()
    
    def save(self, path: str):
        """Save tokenizer model"""
        self.sp.save(path)
        print(f"Tokenizer saved to {path}")
    
    def load(self, path: str):
        """Load tokenizer model"""
        self.sp.load(path)
        print(f"Tokenizer loaded from {path}")

# For smaller datasets, can use HuggingFace tokenizers
class HuggingFaceTokenizer:
    """HuggingFace tokenizer wrapper"""
    
    def __init__(self, tokenizer_name: str = 'gpt2'):
        try:
            from transformers import AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
            print(f"Loaded HuggingFace tokenizer: {tokenizer_name}")
        except ImportError:
            print("transformers not installed, falling back to simple tokenizer")
            self.tokenizer = None
    
    def encode(self, text: str, max_length: Optional[int] = None) -> List[int]:
        """Encode text to token IDs"""
        if not self.tokenizer:
            return []
        tokens = self.tokenizer.encode(text, max_length=max_length, truncation=True)
        return tokens
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs to text"""
        if not self.tokenizer:
            return ""
        return self.tokenizer.decode(token_ids)
    
    def get_vocab_size(self) -> int:
        """Get vocabulary size"""
        if not self.tokenizer:
            return 0
        return self.tokenizer.vocab_size

if __name__ == '__main__':
    # Test SentencePiece tokenizer
    tokenizer = SentencePieceTokenizer(vocab_size=10000)
    
    # Sample texts
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is transforming the world.",
        "Ascension AI is building the future."
    ]
    
    # Train tokenizer
    # tokenizer.train(texts, model_prefix="models/tokenizer/ascension")
    
    # For now, use character-level for demo
    from data.tokenizer import CharTokenizer
    simple_tokenizer = CharTokenizer(texts)
    
    text = "The future of AI"
    encoded = simple_tokenizer.encode(text)
    decoded = simple_tokenizer.decode(encoded)
    
    print(f"Original: {text}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
