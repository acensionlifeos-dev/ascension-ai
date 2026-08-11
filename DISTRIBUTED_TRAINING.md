"""
Ascension AI - Distributed Training Documentation
How to scale training to multiple GPUs
"""

# Distributed Training for Ascension AI

## Setup

### Hardware Requirements
- 2-4 GPUs for small models (1B parameters)
- 8-16 GPUs for medium models (7B parameters)
- 32-64 GPUs for large models (13B parameters)
- 256+ GPUs for XL models (70B parameters)

### Software Stack
- PyTorch with CUDA support
- NCCL for GPU communication
- DeepSpeed or FSDP for large model training
- TorchRun for process launching

## Distributed Training Approaches

### 1. DDP (DistributedDataParallel)
```bash
# Simple DDP with torchrun
torchrun --nproc_per_node=4 scripts/train.py --config configs/small.yaml
```

### 2. DeepSpeed
```bash
# DeepSpeed for large models
deepspeed --num_gpus=4 scripts/train.py --deepspeed_config ds_config.json
```

### 3. FSDP (Fully Sharded Data Parallel)
```bash
# FSDP for very large models
torchrun --nproc_per_node=8 scripts/train.py --use_fsdp
```

## Configuration

### DeepSpeed Config (ds_config.json)
```json
{
  "train_batch_size": 32,
  "train_micro_batch_size": 4,
  "gradient_accumulation_steps": 8,
  "optimizer": {
    "type": "AdamW",
    "params": {
      "lr": "1e-4"
    }
  },
  "fp16": {
    "enabled": true
  },
  "zero_optimization": {
    "stage": 2
  }
}
```

## Training Commands

### Single GPU
```bash
python scripts/train.py --config configs/nano.yaml
```

### Multi-GPU (DDP)
```bash
torchrun --nproc_per_node=4 scripts/train.py --config configs/small.yaml
```

### Multi-Node
```bash
torchrun --nproc_per_node=8 --nnodes=2 --node_rank=0 --master_addr="10.0.0.1" scripts/train.py
```

## Monitoring

### TensorBoard
```bash
tensorboard --logdir=models/logs
```

### Weights & Biases
```bash
wandb login
wandb init ascension-ai
```

## Checkpointing

### Save Checkpoint
```python
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': epoch
}, 'models/checkpoints/checkpoint.pt')
```

### Load Checkpoint
```python
checkpoint = torch.load('models/checkpoints/checkpoint.pt')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
```

## Scaling Strategy

### Phase 1: Single GPU (100M parameters)
- 1 GPU (A100 40GB)
- Training time: 1 week
- Data: 10GB

### Phase 2: Multi-GPU (1B parameters)
- 4 GPUs (A100 40GB)
- Training time: 1 month
- Data: 100GB

### Phase 3: Multi-Node (7B parameters)
- 32 GPUs (H100 80GB)
- Training time: 3 months
- Data: 1TB

### Phase 4: Large Scale (13B+ parameters)
- 64-256 GPUs (H100 80GB)
- Training time: 6-12 months
- Data: 2-10TB

## Cost Estimation

### Cloud Providers
- AWS: $3-5 per GPU hour (p3/p4 instances)
- GCP: $2-4 per GPU hour (a2 instances)
- Azure: $3-5 per GPU hour (ND series)

### On-Premise
- H100 80GB: $30,000 per GPU
- A100 40GB: $15,000 per GPU
- Networking: $10,000-$50,000
- Storage: $1-5 per TB per month

## Next Steps

1. Set up multi-GPU environment
2. Implement DDP training
3. Add DeepSpeed for large models
4. Set up monitoring
5. Train production models

This is the path to training competitive AI models.
