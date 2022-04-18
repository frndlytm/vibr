#!/bin/bash
#SBATCH --job-name=listening_mood.%j
#SBATCH --cpus-per-task=1
#SBATCH --mem=100Gb
#SBATCH --partition=netsi_standard
#SBATCH -t 5-00:00
#SBATCH --output=listening_mood.%j.out
#SBATCH --mail-user=$USER@northeastern.edu
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=END

python run.py --n_layers 4 --n_units 3909 --lr 4e-4 --dropout 0.25 --weight_decay 0.0 --feature tp