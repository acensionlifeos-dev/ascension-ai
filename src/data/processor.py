"""
Ascension AI - Data Processor
Processes raw data for training
"""

from typing import List, Tuple
import re
from pathlib import Path
import json

class DataProcessor:
    """Processes raw data for training"""
    
    def __init__(self):
        self.stats = {
            'total_texts': 0,
            'total_tokens': 0,
            'avg_length': 0
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters (keep letters, numbers, basic punctuation)
        text = re.sub(r'[^a-zA-Z0-9\s.,!?;:\'"-]', '', text)
        # Trim
        text = text.strip()
        return text
    
    def tokenize(self, text: str, tokenizer) -> List[int]:
        """Tokenize text using tokenizer"""
        return tokenizer.encode(text)
    
    def process_texts(self, texts: List[str], tokenizer, max_length: int = 512) -> List[List[int]]:
        """Process texts for training"""
        processed = []
        total_tokens = 0
        
        for text in texts:
            # Clean
            cleaned = self.clean_text(text)
            if not cleaned:
                continue
            
            # Tokenize
            tokens = tokenizer.encode(cleaned, max_length=max_length)
            
            # Filter too short sequences
            if len(tokens) < 10:
                continue
            
            processed.append(tokens)
            total_tokens += len(tokens)
        
        # Update stats
        self.stats['total_texts'] = len(processed)
        self.stats['total_tokens'] = total_tokens
        self.stats['avg_length'] = total_tokens / len(processed) if processed else 0
        
        print(f"Processed {len(processed)} texts")
        print(f"Total tokens: {total_tokens:,}")
        print(f"Average length: {self.stats['avg_length']:.2f}")
        
        return processed
    
    def split_data(self, data: List, train_ratio: float = 0.8, val_ratio: float = 0.1) -> Tuple[List, List, List]:
        """Split data into train, validation, and test sets"""
        n = len(data)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + val_ratio))
        
        train = data[:train_end]
        val = data[train_end:val_end]
        test = data[val_end:]
        
        print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
        return train, val, test
    
    def save_processed_data(self, data: List[List[int]], path: str):
        """Save processed data to disk"""
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        print(f"Saved {len(data)} sequences to {path}")
    
    def load_processed_data(self, path: str) -> List[List[int]]:
        """Load processed data from disk"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} sequences from {path}")
        return data

if __name__ == '__main__':
    processor = DataProcessor()
    
    # Test processing
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is transforming the world.",
        "Ascension AI is building the future."
    ]
    
    from tokenizer import CharTokenizer
    tokenizer = CharTokenizer(texts)
    
    processed = processor.process_texts(texts, tokenizer)
    print(f"Processed: {processed}")
