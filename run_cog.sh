#! /usr/bin/env bash

# Run for Hw3


if [[ $1 = "1.1" ]]; then
   python examples/cog.py \
       --env=Widow250PickTray-v0 \
       --max-path-length=40 \
       --prior-buffer=pickplace_prior.npy \
       --task-buffer=pickplace_task.npy
fi

if [[ $1 = "1.1.1" ]]; then
   python examples/iql.py \
       --env=Widow250PickTray-v0 \
       --max-path-length=40 \
       --prior-buffer=pickplace_prior.npy \
       --task-buffer=pickplace_task.npy
fi


if [[ $1 = "1.1.2" ]]; then
   python examples/awac.py \
       --env=Widow250PickTray-v0 \
       --max-path-length=40 \
       --prior-buffer=pickplace_prior.npy \
       --task-buffer=pickplace_task.npy
fi

if [[ $1 = "1.2" ]]; then
   python examples/chaining_bc.py \
       --env=Widow250PickTray-v0 \
       --max-path-length=40 \
       --prior-buffer=pickplace_prior.npy \
       --task-buffer=pickplace_task.npy
fi


if [[ $1 = "1.3" ]]; then
   python examples/sac_from_bc_plus_reset.py \
      --checkpoint-epoch=180

fi

if [[ $1 = "1.4" ]]; then
   python examples/iql_from_BC.py \
      --checkpoint-epoch=180

fi
