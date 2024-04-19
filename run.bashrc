export SLURM_ACCOUNT=def-sponsor00
export SBATCH_ACCOUNT=$SLURM_ACCOUNT
export SALLOC_ACCOUNT=$SLURM_ACCOUNT


#!/bin/bash
### Here are the SBATCH parameters that you should always consider:
#SBATCH --time=3-30:45:00   ## days-hours:minutes:seconds
#SBATCH --ntasks=1          ## Not strictly necessary because default is 1
#SBATCH --job-name=dispnetc
#SBATCH --output=/home/rbavib/data/disparity-deep-learning/saved_jobs/psmnet_basic.out
#SBATCH --cpus-per-task=48
#SBATCH --mem 128G
#SBATCH --gres=gpu:4
module load anaconda3
module load v100-32g
### module load gpu
### conda update -n base -c defaults conda
source activate slurmtk

python3 /home/rbavib/data/disparity-deep-learning/training_script_folder/training_script.py