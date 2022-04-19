import json
import logging
import logging.config
import os
import random
import time
import warnings
import pathlib
from typing import Optional, Set

import click
import numpy as np
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from sklearn.preprocessing import StandardScaler

import src.vibr
from src.vibr import constants, data, trainer, plotting
from src.vibr.model import MultiLayerPerceptron


class FilterIgniteLogs(logging.Filter):
    def filter(self, record: logging.LogRecord):
        if not record.name.startswith("ignite."):
            return record


class JsonFormatter(logging.Formatter):
    def __init__(self, *args, props: Optional[Set[str]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.props: Set[str] = props or {}

    def format(self, record: logging.LogRecord):
        super().format(record)  # responsible for attaching %(message)s to the record
        return json.dumps(
            {prop: getattr(record, prop, None) for prop in self.props},
            allow_nan=True, sort_keys=True,
        )


def configure_logging(outfile: str = "log.jsonl"):
    logging.config.dictConfig({
        "disable_existing_loggers": False,
        "version": 1,
        "filters": {
            "remove_ignite": {
                "()": FilterIgniteLogs
            }
        },
        "formatters": {
            "default": {
                "format": '(%(asctime)s) %(levelname)-8s %(name)-15s: %(message)s',
                "datefmt": '%Y-%m-%d %H:%M:%S',
            },
            "jsonl": {
                "()": JsonFormatter,
                "props": [
                    "asctime",
                    "levelname",
                    "message",
                    "step",
                    "loss",
                    "accuracy",
                    "precision",
                    "recall",
                    "f1",
                    "average_precision",
                ]
            }
        },
        "handlers": {
            "console": {
                "()": logging.StreamHandler,
                "level": logging.DEBUG,
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "()": logging.FileHandler,
                "level": logging.INFO,
                "formatter": outfile.split(".")[-1],
                "filters": ["remove_ignite"],
                "filename": outfile,
            }
        },
        "root": {
            "level": "NOTSET",
            "handlers": ["console", "file"]
        }
    })


def current_milli_time():
    return round(time.time() * 1000)


# Using a seed to maintain consistent and reproducible results
def set_seed(seed: int = constants.DEFAULT_SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name", type=str)
@click.option(  # Network Configuration options
    "--layers", type=int, default=4,
    help="Number of linear submodules."
)
@click.option(
    "--units", type=int, default=3909,
    help="Number of units linear submodule."
)
@click.option(
    "--dropout", type=float, default=0.25,
    help="Dropout probability for all linear submodules."
)
@click.option(
    "--lr", type=float, default=4e-4,
    help="Initial learning rate."
)
@click.option(  # Pipeline Configuration options
    "--epochs", type=int, default=100,
    help="Number of epochs to train."
)
@click.option(
    "--batch_size", type=int, default=constants.DEFAULT_BATCH_SIZE,
    help="Mini-batch size for training"
)
@click.option(
    "--workers", type=int, default=constants.DEFAULT_WORKERS,
    help="Number of workers for data loading."
)
@click.option(
    "--seed", type=int, default=constants.DEFAULT_SEED,
    help="Random seed to set"
)
@click.option(
    "--no-save", is_flag=True, show_default=True, type=bool, default=False,
    help="Save the model state after running."
)
@click.option(
    "--plot-result", is_flag=True, show_default=True, type=bool, default=False,
    help="Plot result after running."
)
def train(
    name: str,
    layers: int = 4,
    units: int = 3909,
    dropout: float = 0.25,
    lr: float = 1e-4,
    epochs: int = 100,
    batch_size: int = 128,
    workers: int = 4,
    seed: Optional[int] = None,
    no_save: bool = False,
    plot_result: bool = False
):
    run_id = f"{name}-{current_milli_time()}"
    output_path = os.path.join(constants.MODELS_DIR, f"{layers}-{units}-{dropout}-{lr}-{epochs}-{batch_size}-{workers}-{seed}", f"{run_id}")

    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    # Configure the run to save statistics
    set_seed(seed)
    # configure_logging(os.path.join(constants.DATA_DIR, "logs", f"{run_id}.log.jsonl"))
    configure_logging(os.path.join(output_path, f"{run_id}.log.jsonl"))

    # Load and split data
    d_in, d_out, datasets = data.load().values()
    train_loader, validate_loader = (
        DataLoader(
            datasets["train"],
            batch_size=batch_size,
            num_workers=workers,
            shuffle=True,
        ),
        DataLoader(
            datasets["validate"],
            batch_size=batch_size,
            num_workers=workers,
            shuffle=False,
        )
    )

    # Setup the model, using gpu if available, fit a scalar to the data to standardize
    scaler = StandardScaler().fit(datasets["train"][:][0])
    model = MultiLayerPerceptron(
        d_in=d_in,
        d_out=d_out,
        units=units,
        n_layers=layers,
        dropout=dropout,
        shift=torch.from_numpy(scaler.mean_.astype(np.float32)),
        scale=torch.from_numpy(scaler.scale_.astype(np.float32)),
    ).to(constants.DEVICE)

    # Configure a trainer and run it
    criterion = nn.BCEWithLogitsLoss().to(constants.DEVICE)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    pipeline = trainer.configure(
        model, optimizer, criterion, train_loader, validate_loader
    )

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        pipeline.run(train_loader, max_epochs=epochs)

    if  plot_result:
        # plotting.plot_result(os.path.join(constants.DATA_DIR, "logs", f"{run_id}.log.jsonl"), units, dropout, lr, os.path.join(constants.RESULT_DIR, "figures", f"{run_id}"))
        plotting.plot_result(os.path.join(output_path, f"{run_id}.log.jsonl"), units, dropout, lr, os.path.join(output_path, f"{run_id}"))
    # Save (or don't) the model state for futher testing
    if no_save: return
    torch.save(model.state_dict(), os.path.join(output_path,f"{run_id}.pt"))


@cli.command()
def test(name: str):
    pass


if __name__ == "__main__":
    cli()