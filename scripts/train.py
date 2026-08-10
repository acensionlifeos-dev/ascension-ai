"""
Ascension AI - Training Script
Complete training pipeline for Ascension models
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.architecture.transformer import AscensionTransformer, get_model_config
from src.data.tokenizer import CharTokenizer
from src.data.collector import DataCollector
from src.data.processor import DataProcessor
import time
import json
from pathlib import Path

class TextDataset(Dataset):
    """Dataset for training"""
    def __init__(self, sequences):
        self.sequences = sequences
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        return torch.tensor(self.sequences[idx], dtype=torch.long)

class Trainer:
    """Trainer for Ascension models"""
    def __init__(self, model, config, device='cuda'):
        self.model = model.to(device)
        self.config = config
        self.device = device
        
        # Optimizer
        self.optimizer = AdamW(model.parameters(), lr=1e-4)
        
        # Scheduler
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=100,
            num_training_steps=1000
        )
        
        # Loss function
        self.criterion = nn.CrossEntropyLoss()
    
    def train_epoch(self, dataloader):
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        start_time = time.time()
        
        for batch_idx, batch in enumerate(dataloader):
            batch = batch.to(self.device)
            
            # Forward pass
            logits = self.model(batch[:, :-1])
            
            # Calculate loss
            loss = self.criterion(
                logits.reshape(-1, logits.size(-1)),
                batch[:, 1:].reshape(-1)
            )
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            self.scheduler.step()
            
            total_loss += loss.item()
            
            if batch_idx % 10 == 0:
                print(f"Batch {batch_idx}, Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(dataloader)
        epoch_time = time.time() - start_time
        print(f"Epoch completed in {epoch_time:.2f}s, Avg Loss: {avg_loss:.4f}")
        
        return avg_loss
    
    def evaluate(self, dataloader):
        """Evaluate the model"""
        self.model.eval()
        total_loss = 0
        
        with torch.no_grad():
            for batch in dataloader:
                batch = batch.to(self.device)
                logits = self.model(batch[:, :-1])
                loss = self.criterion(
                    logits.reshape(-1, logits.size(-1)),
                    batch[:, 1:].reshape(-1)
                )
                total_loss += loss.item()
        
        avg_loss = total_loss / len(dataloader)
        print(f"Evaluation Loss: {avg_loss:.4f}")
        
        return avg_loss
    
    def save_checkpoint(self, path):
        """Save model checkpoint"""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'config': self.config
        }, path)
        print(f"Checkpoint saved to {path}")
    
    def load_checkpoint(self, path):
        """Load model checkpoint"""
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        print(f"Checkpoint loaded from {path}")

def main():
    """Main training function"""
    print("=" * 60)
    print("ASCENSION AI - TRAINING")
    print("=" * 60)
    
    # Configuration
    config = get_model_config('nano')  # 100M parameters
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"\nDevice: {device}")
    
    # Collect data
    print("\n" + "=" * 60)
    print("STEP 1: DATA COLLECTION")
    print("=" * 60)
    collector = DataCollector()
    raw_texts = collector.collect_sample_data()
    print(f"Collected {len(raw_texts)} raw texts")
    
    # Build tokenizer
    print("\n" + "=" * 60)
    print("STEP 2: TOKENIZATION")
    print("=" * 60)
    tokenizer = CharTokenizer(raw_texts)
    config.vocab_size = tokenizer.vocab_size
    print(f"Tokenizer vocabulary size: {config.vocab_size}")
    
    # Process data
    print("\n" + "=" * 60)
    print("STEP 3: DATA PROCESSING")
    print("=" * 60)
    processor = DataProcessor()
    processed_sequences = processor.process_texts(raw_texts, tokenizer, max_length=128)
    
    # Split data
    train_data, val_data, test_data = processor.split_data(processed_sequences)
    
    # Create datasets
    train_dataset = TextDataset(train_data)
    val_dataset = TextDataset(val_data)
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=4)
    
    # Create model
    print("\n" + "=" * 60)
    print("STEP 4: MODEL CREATION")
    print("=" * 60)
    model = AscensionTransformer(config)
    num_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {num_params:,}")
    
    # Create trainer
    print("\n" + "=" * 60)
    print("STEP 5: TRAINING")
    print("=" * 60)
    trainer = Trainer(model, config, device)
    
    # Training loop
    num_epochs = 5
    for epoch in range(num_epochs):
        print(f"\nEpoch {epoch + 1}/{num_epochs}")
        train_loss = trainer.train_epoch(train_loader)
        val_loss = trainer.evaluate(val_loader)
        
        # Save checkpoint
        trainer.save_checkpoint(f'models/checkpoints/epoch_{epoch + 1}.pt')
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED")
    print("=" * 60)
    
    # Test generation
    print("\n" + "=" * 60)
    print("STEP 6: GENERATION TEST")
    print("=" * 60)
    model.eval()
    with torch.no_grad():
        test_text = "The future of AI"
        test_tokens = tokenizer.encode(test_text, max_length=32)
        test_input = torch.tensor([test_tokens], dtype=torch.long).to(device)
        
        generated = model.generate(test_input, max_new_tokens=20, temperature=0.8)
        generated_text = tokenizer.decode(generated[0].tolist())
        print(f"\nInput: {test_text}")
        print(f"Generated: {generated_text}")
    
    print("\n" + "=" * 60)
    print("ASCENSION AI TRAINING COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    main()
