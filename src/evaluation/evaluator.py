"""
Ascension AI - Evaluation System
Comprehensive evaluation for model performance
"""

import torch
import torch.nn as nn
from typing import Dict, List
import json
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from architecture.transformer import AscensionTransformer
from data.tokenizer import CharTokenizer

class Evaluator:
    """Evaluate model performance"""
    
    def __init__(self, model, tokenizer, device='cuda'):
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        self.model.eval()
    
    def calculate_perplexity(self, dataloader) -> float:
        """Calculate perplexity on dataset"""
        total_loss = 0
        total_tokens = 0
        
        with torch.no_grad():
            for batch in dataloader:
                batch = batch.to(self.device)
                logits = self.model(batch[:, :-1])
                
                # Calculate loss
                loss = nn.functional.cross_entropy(
                    logits.reshape(-1, logits.size(-1)),
                    batch[:, 1:].reshape(-1),
                    reduction='sum'
                )
                
                total_loss += loss.item()
                total_tokens += batch[:, 1:].numel()
        
        avg_loss = total_loss / total_tokens
        perplexity = torch.exp(torch.tensor(avg_loss)).item()
        
        return perplexity
    
    def calculate_bleu(self, generated_texts, reference_texts) -> float:
        """Calculate BLEU score (simplified)"""
        # In production, use proper BLEU implementation
        from collections import Counter
        
        total_bleu = 0
        for gen, ref in zip(generated_texts, reference_texts):
            # Simple word overlap
            gen_words = set(gen.split())
            ref_words = set(ref.split())
            overlap = len(gen_words & ref_words)
            total = len(gen_words | ref_words)
            bleu = overlap / total if total > 0 else 0
            total_bleu += bleu
        
        return total_bleu / len(generated_texts)
    
    def benchmark_generation(self, prompts, max_new_tokens=50) -> Dict:
        """Benchmark generation performance"""
        results = {
            'avg_generation_time': 0,
            'tokens_per_second': 0,
            'avg_length': 0
        }
        
        import time
        total_time = 0
        total_tokens = 0
        
        with torch.no_grad():
            for prompt in prompts:
                input_tokens = self.tokenizer.encode(prompt, max_length=128)
                input_tensor = torch.tensor([input_tokens], dtype=torch.long).to(self.device)
                
                start_time = time.time()
                generated = self.model.generate(input_tensor, max_new_tokens=max_new_tokens, temperature=0.8)
                generation_time = time.time() - start_time
                
                total_time += generation_time
                total_tokens += max_new_tokens
        
        results['avg_generation_time'] = total_time / len(prompts)
        results['tokens_per_second'] = total_tokens / total_time
        results['avg_length'] = total_tokens / len(prompts)
        
        return results
    
    def run_full_evaluation(self, train_loader, val_loader, prompts) -> Dict:
        """Run complete evaluation"""
        print("Running full evaluation...")
        
        results = {}
        
        # Perplexity
        print("Calculating perplexity...")
        results['train_perplexity'] = self.calculate_perplexity(train_loader)
        results['val_perplexity'] = self.calculate_perplexity(val_loader)
        
        # Generation benchmark
        print("Benchmarking generation...")
        results['generation'] = self.benchmark_generation(prompts)
        
        # Save results
        Path('models/evaluation').mkdir(parents=True, exist_ok=True)
        with open('models/evaluation/results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("Evaluation complete!")
        print(f"Train Perplexity: {results['train_perplexity']:.2f}")
        print(f"Val Perplexity: {results['val_perplexity']:.2f}")
        print(f"Tokens/Second: {results['generation']['tokens_per_second']:.2f}")
        
        return results

# Benchmark datasets for production
# - MMLU (Massive Multitask Language Understanding)
# - HellaSwag (Common sense reasoning)
# - HumanEval (Code generation)
# - PIQA (Physical reasoning)
# - WinoGrande (Winograd schema)
# - BIG-Bench (Broad language understanding)

if __name__ == '__main__':
    print("Evaluation system ready")
