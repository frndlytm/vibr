
import json
import logging
import logging.config
from functools import partial
from typing import Callable

import torch

from ignite.contrib.metrics import AveragePrecision
from ignite.engine import (
    create_supervised_evaluator,
    create_supervised_trainer,
    Events,
)
from ignite.metrics import (
    Accuracy,
    Fbeta,
    Loss,
    Precision,
    Recall,
    RunningAverage,
)

from vibr import constants


def classify_at_threshold(
    output: tuple,
    activate: Callable = torch.sigmoid,
    threshold: float = 0.5,
):
    y_pred, y_true = output
    return (activate(y_pred) >= threshold).float(), y_true


# Make a trainer 
def configure(
    model,
    optimizer,
    criterion,
    train_loader,
    validate_loader,
    threshold: float = 0.5,
    activate: Callable = torch.sigmoid,
    device: str = constants.DEVICE,
):
    # Set up the metrics we'll be logging throughout the traininer pipeline
    classify = partial(classify_at_threshold, activate=activate, threshold=threshold)
    metrics = {
        "loss": Loss(criterion),
        "accuracy": Accuracy(classify, is_multilabel=True),
        "precision": Precision(classify, average=True),
        "recall": Recall(classify, average=True),
        "f1": Fbeta(1.0, output_transform=classify),
        "average_precision": AveragePrecision(
            output_transform=lambda o: (activate(o[0]), o[1])
        )
    }

    # Initialize the trainer and evaluator with metrics.
    trainer, evaluator = (
        create_supervised_trainer(model, optimizer, criterion, device),
        create_supervised_evaluator(model, metrics=metrics, device=device),
    )
    RunningAverage(output_transform=lambda x: x).attach(trainer, 'loss')

    # Every epoch...
    @trainer.on(Events.EPOCH_COMPLETED)
    def log_train_metrics(trainer):
        # Evaluate the training set for our metrics and log to file
        evaluator.run(train_loader)
        logging.info(
            f"Epoch[{trainer.state.epoch}] Complete", extra={
                "step": "train",
                "epoch": trainer.state.epoch,
                **evaluator.state.metrics
            }
        )

    @trainer.on(Events.EPOCH_COMPLETED)
    def log_validate_metrics(trainer):
        # Evaluate the validate set for our metrics and log to file
        evaluator.run(validate_loader)
        logging.info(
            f"Epoch[{trainer.state.epoch}] Complete", extra={
                "step": "validate",
                "epoch": trainer.state.epoch,
                **evaluator.state.metrics
            }
        )

    return trainer
