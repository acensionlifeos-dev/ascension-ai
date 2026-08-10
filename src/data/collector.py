"""
Ascension AI - Data Collector
Collects training data from various sources
"""

import requests
from typing import List, Optional
import time
import os
from pathlib import Path

class DataCollector:
    """Collects training data from various sources"""
    
    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def collect_from_url(self, url: str, filename: str) -> bool:
        """Download data from URL"""
        try:
            print(f"Downloading from {url}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Saved to {filepath}")
            return True
        except Exception as e:
            print(f"Error downloading from {url}: {e}")
            return False
    
    def collect_sample_data(self) -> List[str]:
        """Collect sample data for training"""
        print("Collecting sample data...")
        
        texts = []
        
        # Sample texts from various domains
        sample_texts = [
            # Technology
            "Artificial intelligence is transforming every industry.",
            "Machine learning algorithms learn patterns from data.",
            "Deep learning uses neural networks with many layers.",
            "Natural language processing enables computers to understand text.",
            "Computer vision allows machines to see and interpret images.",
            
            # Science
            "The speed of light is approximately 299,792,458 meters per second.",
            "The periodic table organizes chemical elements by atomic number.",
            "DNA contains the genetic instructions for all living organisms.",
            "Gravity is the force that attracts objects with mass.",
            "The universe is approximately 13.8 billion years old.",
            
            # Literature
            "To be or not to be, that is the question.",
            "It was the best of times, it was the worst of times.",
            "All that glitters is not gold.",
            "The journey of a thousand miles begins with a single step.",
            "Knowledge is power.",
            
            # Business
            "Supply and demand determine market prices.",
            "Innovation drives economic growth.",
            "Customer satisfaction is key to business success.",
            "Strategic planning guides long-term decisions.",
            "Effective communication builds strong teams.",
            
            # Philosophy
            "I think, therefore I am.",
            "The unexamined life is not worth living.",
            "Knowledge comes from experience.",
            "Ethics guides moral decision-making.",
            "Logic and reason lead to truth."
        ]
        
        # Repeat to create more data
        texts = sample_texts * 1000
        
        # Save to file
        filepath = self.output_dir / "sample_data.txt"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(texts))
        
        print(f"Saved {len(texts)} samples to {filepath}")
        return texts
    
    def collect_from_common_crawl(self, sample_size: int = 1000) -> List[str]:
        """
        Collect data from Common Crawl (simplified for demo)
        In production, use Common Crawl's actual dataset
        """
        print("Collecting from Common Crawl (simplified)...")
        
        # For demo, return sample data
        # In production, download and process Common Crawl snapshots
        return self.collect_sample_data()
    
    def collect_from_wikipedia(self, sample_size: int = 1000) -> List[str]:
        """
        Collect data from Wikipedia (simplified for demo)
        In production, use Wikipedia dumps
        """
        print("Collecting from Wikipedia (simplified)...")
        
        # For demo, return sample data
        # In production, download and process Wikipedia dumps
        return self.collect_sample_data()
    
    def collect_from_github(self, sample_size: int = 1000) -> List[str]:
        """
        Collect code from GitHub (simplified for demo)
        In production, use GitHub API or dataset
        """
        print("Collecting from GitHub (simplified)...")
        
        # Sample code snippets
        code_samples = [
            "def hello_world():\n    print('Hello, World!')",
            "class Node:\n    def __init__(self, value):\n        self.value = value",
            "for i in range(10):\n    print(i)",
            "if x > 0:\n    return True\nelse:\n    return False",
            "import numpy as np\narr = np.array([1, 2, 3])"
        ]
        
        texts = code_samples * 200
        return texts

# For production, implement:
# - Common Crawl downloader
# - Wikipedia dump processor
# - GitHub scraper
# - ArXiv paper downloader
# - Book corpus downloader
# - Image dataset downloader
# - Video dataset downloader
# - Audio dataset downloader

if __name__ == '__main__':
    collector = DataCollector()
    texts = collector.collect_sample_data()
    print(f"Collected {len(texts)} texts")
