"""
Ascension AI - Distributed Training
Multi-GPU training support for large models
"""

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.architecture.transformer import AscensionTransformer, get_model_config
from src.data.tokenizer import CharTokenizer
from src.data.collector import DataCollector
from src.data.processor import DataProcessor
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
import time

class TextDataset(Dataset):
    """Dataset for distributed training"""
    def __init__(self, sequences):
        self.sequences = sequences
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        return torch.tensor(self.sequences[idx], dtype=torch.long)

def setup_ddp(rank, world_size):
    """Setup distributed training"""
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    
    # Initialize process group
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)

def cleanup_ddp():
    """Cleanup distributed training"""
    dist.destroy_process_group()

class DistributedTrainer:
    """Trainer for distributed training"""
    
    def __init__(self, rank, world_size, config, device):
        self.rank = rank
        self.world_size = world_size
        self.config = config
        self.device = device
        
        # Create model
        self.model = AscensionTransformer(config).to(device)
        
        # Wrap with DDP
        self.model = DDP(self.model, device_ids=[rank])
        
        # Optimizer
        self.optimizer = AdamW(self.model.parameters(), lr=1e-4)
        
        # Scheduler
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=1000,
            num_training_steps=100000
        )
        
        # Loss function
        self.criterion = torch.nn.CrossEntropyLoss()
    
    def train_epoch(self, dataloader, epoch):
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        start_time = time.time()
        
        for batch_idx, batch in enumerate(dataloader):
            batch = batch.to(self.device)
            
            # Forward pass
            logits = self.model.module(batch[:, :-1])
            
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
            
            if batch_idx % 10 == 0 and self.rank == 0:
                print(f"Rank {self.rank}, Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(dataloader)
        epoch_time = time.time() - start_time
        
        if self.rank == 0:
            print(f"Epoch {epoch} completed in {epoch_time:.2f}s, Avg Loss: {avg_loss:.4f}")
        
        return avg_loss
    
    def save_checkpoint(self, epoch, path):
        """Save checkpoint (only on rank 0)"""
        if self.rank == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': self.model.module.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'config': self.config
            }, path)
            print(f"Checkpoint saved to {path}")

def train_ddp(rank, world_size):
    """Main training function for each process"""
    # Setup
    setup_ddp(rank, world_size)
    device = f'cuda:{rank}'
    
    # Configuration
    config = get_model_config('small')  # 1B parameters for distributed training
    
    # Collect data
    if rank == 0:
        print("Collecting data...")
        collector = DataCollector()
        raw_texts = collector.collect_sample_data()
    else:
        raw_texts = []
    
    # Synchronize
    dist.barrier()
    
    # Broadcast data from rank 0
    if rank == 0:
        for r in range(1, world_size):
            dist.send(raw_texts, dst=r)
    else:
        raw_texts = dist.recv(src=0)
    
    # Build tokenizer
    if rank == 0:
        print("Building tokenizer...")
        from data.tokenizer import CharTokenizer
        tokenizer = CharTokenizer(raw_texts)
        config.vocab_size = tokenizer.vocab_size
    else:
        tokenizer = None
    
    # Broadcast tokenizer
    if rank == 0:
        for r in range(1, world_size):
            dist.send(tokenizer, dst=r)
    else:
        tokenizer = dist.recv(src=0)
    
    # Process data
    if rank == 0:
        print("Processing data...")
        processor = DataProcessor()
        processed_sequences = processor.process_texts(raw_texts, tokenizer, max_length=128)
        train_data, val_data, test_data = processor.split_data(processed_sequences)
    else:
        processed_sequences = []
        train_data = []
        val_data = []
        test_data = []
    
    # Synchronize
    dist.barrier()
    
    # Broadcast data
    if rank == 0:
        for r in range(1, world_size):
            dist.send((train_data, val_data, test_data), dst=r)
    else:
        train_data, val_data, test_data = dist.recv(src=0)
    
    # Create dataset
    train_dataset = TextDataset(train_data)
    val_dataset = TextDataset(val_data)
    
    # Create sampler for distributed training
    train_sampler = DistributedSampler(train_dataset, num_replicas=world_size, rank=rank)
    val_sampler = DistributedSampler(val_dataset, num_replicas=world_size, rank=rank)
    
    # Create dataloader
    train_loader = DataLoader(train_dataset, batch_size=4, sampler=train_sampler)
    val_loader = DataLoader(val_dataset, batch_size=4, sampler=val_sampler)
    
    # Create trainer
    trainer = DistributedTrainer(rank, world_size, config, device)
    
    # Training loop
    num_epochs = 5
    for epoch in range(num_epochs):
        if rank == 0:
            print(f"\nEpoch {epoch + 1}/{num_epochs}")
        
        train_sampler.set_epoch(epoch)
        train_loss = trainer.train_epoch(train_loader, epoch)
        
        if rank == 0:
            trainer.save_checkpoint(epoch, f'models/checkpoints/distributed_epoch_{epoch + 1}.pt')
    
    # Cleanup
    cleanup_ddp()

def main():
    """Main function to launch distributed training"""
    world_size = torch.cuda.device_count()
    if world_size < 2:
        print("Need at least 2 GPUs for distributed training")
        return
    
    print(f"Starting distributed training on {world_size} GPUs")
    mp.spawn(train_ddp, args=(world_size,), nprocs=world_size)

if __name__ == '__main__':
    main()
