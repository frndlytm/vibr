#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --mem=10Gb
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --job-name=vibr.%j
#SBATCH --output=results/slurm/vibr.%j.out
#SBATCH --mail-user=$USER@northeastern.edu
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=END

set -x
module load cuda
python cli.py train model-name --layers 8 --units 4000 --lr=4e-4 --epochs=100 --plot-result