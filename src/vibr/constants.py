import torch
from os import path

PROJECT_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
DATA_DIR = path.join(PROJECT_DIR, "data")
MODELS_DIR = path.join(PROJECT_DIR, "models")
RESULT_DIR = path.join(PROJECT_DIR, "results")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEFAULT_SEED = 100
DEFAULT_BATCH_SIZE = 2000
DEFAULT_WORKERS = 4

