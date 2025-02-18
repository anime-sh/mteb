from __future__ import annotations

import logging
import math
import os
from typing import Any

import torch
from sklearn import metrics
from torch.utils.data import DataLoader
from torchvision import transforms

from mteb.encoder_interface import Encoder

from ..Evaluator import Evaluator

logger = logging.getLogger(__name__)

# transform = transforms.Compose([transforms.PILToTensor()])
# Replace with appropriate audio thing


class AudioDataset(torch.utils.data.Dataset):
    def __init__(self, hf_dataset, audio_column_name: str = "image", transform=None):
        self.dataset = hf_dataset
        self.transform = transform
        self.audio_column_name = audio_column_name

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        # image = self.dataset[idx][self.image_column_name]
        # if image.mode != "RGB":
        #     image = image.convert("RGB")
        # image = self.transform(image)
        # return image
        pass #Change for audio appropriately


def custom_collate_fn(batch):
    return batch


class ZeroshotClassificationEvaluator(Evaluator):
    def __init__(
        self,
        dataset,
        audio_column_name: str,
        labels: list[int],
        candidate_labels: list[str],
        task_name: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.dataset = AudioDataset(
            dataset, audio_column_name=audio_column_name, transform=transform
        )
        self.audio_column_name = audio_column_name
        self.labels = labels
        self.candidate_labels = candidate_labels
        self.task_name = task_name

    def __call__(self, model: Encoder, *, encode_kwargs: dict[str, Any] = {}):
        if "batch_size" not in encode_kwargs:
            encode_kwargs["batch_size"] = 32

        dataloader = DataLoader(
            self.dataset,
            batch_size=encode_kwargs["batch_size"],
            shuffle=False,
            collate_fn=custom_collate_fn,
            num_workers=min(math.floor(os.cpu_count() / 2), 16),
        )

        text_embeddings = model.get_text_embeddings(
            self.candidate_labels, batch_size=encode_kwargs["batch_size"]
        )

        audio_embeddings = model.get_audio_embeddings(
            dataloader, batch_size=encode_kwargs["batch_size"]
        )

        probs = model.calculate_probs(text_embeddings, audio_embeddings)
        predictions = probs.argmax(dim=1)

        logger.info("Evaluating...")

        accuracy = metrics.accuracy_score(self.labels, predictions.tolist())
    
        return {"accuracy": accuracy}
