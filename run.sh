#!/bin/bash
#SBATCH --job-name=vibr.%j
#SBATCH --cpus-per-task=1
#SBATCH --mem=100Gb
#SBATCH --output=vibr.%j.out
#SBATCH --mail-user=$USER@northeastern.edu
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=END

python cli.py train model-name --layers 2 --units 20 --lr=4e-5 --epochs=100 --plot-result --no-save