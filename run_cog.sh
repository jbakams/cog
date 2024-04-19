#! /usr/bin/env bash

# Run for Hw3


if [[ $1 = "1.1" ]]; then
   python examples/cog.py \
       --env=Widow250PickTray-v0 \
       --max-path-length=40 \
       --prior-buffer=pickplace_prior.npy \
       --task-buffer=pickplace_task.npy
fi

