"""Inference helpers for Ascension-native PyTorch checkpoints."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import torch
import torch.serialization

try:
    from tokenizers import Tokenizer as HFTokenizer
    HAS_TOKENIZERS = True
except Exception:
    HAS_TOKENIZERS = False

from .transformer import AscensionTransformer, ModelConfig


class EliteInference:
    """Load and generate from an Ascension-native .pt checkpoint."""

    def __init__(self, checkpoint_dir: str | Path, prefix: str = "ascension_elite") -> None:
        self.root = Path(checkpoint_dir)
        self.prefix = prefix
        self.meta = self._load_json(self.root / f"{prefix}_meta.json")
        self.tokenizer_path = Path(self.meta["tokenizer_path"])
        self.tokenizer = self._load_tokenizer(self.tokenizer_path)
        self.config = ModelConfig(**self.meta["config"])
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = AscensionTransformer(self.config).to(self.device)
        with torch.serialization.safe_globals([ModelConfig]):
            checkpoint = torch.load(
                self.root / f"{prefix}.pt",
                map_location=self.device,
                weights_only=True,
            )
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

    @staticmethod
    def _load_json(path: Path) -> dict:
        if not path.is_file():
            raise FileNotFoundError(f"Missing file: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _load_tokenizer(self, path: Path):
        if not path.is_file():
            raise FileNotFoundError(f"Missing tokenizer: {path}")
        if HAS_TOKENIZERS:
            try:
                return HFTokenizer.from_file(str(path))
            except Exception:
                pass
        return self._load_json(path)

    def _encode(self, text: str, max_length: int = 128) -> torch.Tensor:
        if isinstance(self.tokenizer, HFTokenizer):
            ids = self.tokenizer.encode(text).ids
        else:
            ids = [
                self.tokenizer["char_to_idx"].get(c, self.tokenizer["char_to_idx"].get("<unk>", 0))
                for c in text
            ]
        if len(ids) > max_length:
            ids = ids[-max_length:]
        return torch.tensor([ids], dtype=torch.long, device=self.device)

    def _decode(self, ids: list[int]) -> str:
        if isinstance(self.tokenizer, HFTokenizer):
            return self.tokenizer.decode(ids)
        return "".join(
            self.tokenizer["idx_to_char"].get(str(i), self.tokenizer["idx_to_char"].get(i, ""))
            for i in ids
        )

    def _stop_token(self, token_id: int) -> bool:
        if isinstance(self.tokenizer, HFTokenizer):
            token = self.tokenizer.id_to_token(token_id)
            if token is None:
                return False
            return token in {"</s>", ".", "!", "?", "\n"} or token.endswith(".")
        char = self.tokenizer["idx_to_char"].get(str(token_id), self.tokenizer["idx_to_char"].get(token_id, ""))
        return char in {".", "!", "?", "\n"}

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 128,
        temperature: float = 0.8,
        top_k: int = 10,
    ) -> str:
        if not prompt:
            return ""

        input_ids = self._encode(prompt)
        generated = input_ids[0].tolist()

        with torch.no_grad():
            for _ in range(max_new_tokens):
                if len(generated) >= self.config.max_length:
                    break
                input_tensor = torch.tensor([generated], dtype=torch.long, device=self.device)
                logits = self.model(input_tensor)
                next_logits = logits[0, -1, :]
                next_logits = next_logits / max(temperature, 0.01)

                if top_k > 0:
                    values, indices = torch.topk(next_logits, min(top_k, next_logits.size(-1)))
                    next_logits = torch.full_like(next_logits, float("-inf"))
                    next_logits[indices] = values

                probs = torch.softmax(next_logits, dim=-1)
                next_id = torch.multinomial(probs, num_samples=1).item()
                generated.append(next_id)

                if self._stop_token(next_id) and len(generated) > len(input_ids[0]):
                    break

        # Return only the continuation. Re-decoding the input alongside newly
        # sampled tokens made evaluation and chat surfaces falsely look like
        # the model was echoing the user's entire prompt.
        return self._decode(generated[len(input_ids[0]):])

    def status(self) -> dict:
        return {
            "ready": True,
            "model": "Ascension Elite",
            "checkpoint": str(self.root),
            "vocab_size": self.config.vocab_size,
            "num_layers": self.config.num_layers,
            "hidden_size": self.config.hidden_size,
            "device": self.device,
            "loss": self.meta.get("final_loss"),
        }
