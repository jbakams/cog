#!/bin/bash
#SBATCH --mem=16G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --time=5-3:0:0
#SBATCH --mail-user=jeremie.bakambana@umontreal.ca
#SBATCH --mail-type=ALL
#SBATCH --gres=gpu:p100l:1


module purge
module load python/3.9 cuda cudnn scipy-stack
source ~/py39/bin/activate

python /home/jey/projects/def-sponsor00/jey/cog/examples/cog.py \
     --env=Widow250PickTray-v0 \
     --max-path-length=40 \
     --prior-buffer=pickplace_prior.npy \
     --task-buffer=pickplace_task.npy
