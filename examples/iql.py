import argparse
import json
import os
import copy

import comet_ml

import torch
import roboverse

import rlkit.torch.pytorch_util as ptu
from rlkit.data_management.load_buffer import load_data_from_npy_chaining
from rlkit.samplers.data_collector import MdpPathCollector, \
    CustomMDPPathCollector

import rlkit.torch.pytorch_util as ptu
from rlkit.data_management.load_buffer import load_data_from_npy_chaining
from rlkit.launchers.launcher_util import setup_logger
from rlkit.samplers.data_collector import MdpPathCollector
from rlkit.torch.conv_networks import ConcatCNN
from rlkit.torch.sac.sac import SACTrainer
from rlkit.torch.sac.iql_trainer import IQLTrainer
from rlkit.torch.sac.policies import TanhGaussianPolicy, MakeDeterministic
#from rlkit.torch.sac.policies2.gaussian_policy import TanhGaussianPolicy
from rlkit.torch.conv_networks import CNN, ConcatCNN
from rlkit.torch.torch_rl_algorithm import TorchBatchRLAlgorithm
from rlkit.util.video import VideoSaveFunction
from rlkit.data_management.obs_dict_replay_buffer import \
    ObsDictReplayBuffer
    
from rlkit.util.video import VideoSaveFunction
from rlkit.launchers.launcher_util import setup_logger


import argparse, os
import roboverse
import numpy as np

DEFAULT_PRIOR_BUFFER = ('/media/avi/data/Work/github/avisingh599/minibullet'
                        '/data/oct6_Widow250DrawerGraspNeutral-v0_20K_save_all'
                        '_noise_0.1_2020-10-06T19-37-26_100.npy')
DEFAULT_TASK_BUFFER = ('/media/avi/data/Work/github/avisingh599/minibullet'
                        '/data/oct6_Widow250DrawerGraspNeutral-v0_20K_save_all'
                        '_noise_0.1_2020-10-06T19-37-26_100.npy')
CUSTOM_LOG_DIR = '/nfs/kun1/users/avi/doodad-output/'

class Log:
    def __init__(self, PATH):
        from logging_utils import Logger as TableLogger
        self._logger = TableLogger()
        self._logger.add_folder_output(folder_name=f"{PATH}")
        self._logger.add_tabular_output(file_name=f"{PATH}/log_data.csv")
        os.makedirs(PATH, exist_ok=True)

    def log_dict(self, dico):
        for k, v in dico.items():
            if isinstance(v, list) and len(v) == 0:
                continue
            self._logger.record_tabular_misc_stat(k, v)
        self._logger.dump_tabular()


def experiment(variant, comet_logger):
    eval_env = roboverse.make(variant['env'], transpose_image=True)
    expl_env = eval_env
    action_dim = eval_env.action_space.low.size

    cnn_params = variant['cnn_params']
    cnn_params_v = copy.deepcopy(cnn_params)
    
    cnn_params.update(
        input_width=48,
        input_height=48,
        input_channels=3,
        output_size=1,
        added_fc_input_size=action_dim,
    )
    
    
    qf1 = ConcatCNN(**cnn_params)
    qf2 = ConcatCNN(**cnn_params)
    target_qf1 = ConcatCNN(**cnn_params)
    target_qf2 = ConcatCNN(**cnn_params)
    
    cnn_params_v.update(
        input_width=48,
        input_height=48,
        input_channels=3,
        output_size=1,
    )    
    
    vf = ConcatCNN(**cnn_params_v)

    cnn_params.update(
        output_size=256,
        added_fc_input_size=0,
        hidden_sizes=[1024, 512],
    )

    policy_obs_processor = CNN(**cnn_params)
    policy = TanhGaussianPolicy(
        obs_dim=cnn_params['output_size'],
        action_dim=action_dim,
        hidden_sizes=[256, 256, 256],
        obs_processor=policy_obs_processor,
    )

    eval_policy = policy#MakeDeterministic(policy)
    eval_path_collector = MdpPathCollector(
        eval_env,
        eval_policy,
    )
    expl_path_collector = CustomMDPPathCollector(
        eval_env,
    )

    observation_key = 'image'
    replay_buffer = load_data_from_npy_chaining(
        variant, expl_env, observation_key)

    # Translate 0/1 rewards to +4/+10 rewards.
    if variant['use_positive_rew']:
        if set(np.unique(replay_buffer._rewards)).issubset({0, 1}):
            replay_buffer._rewards = replay_buffer._rewards * 6.0
            replay_buffer._rewards = replay_buffer._rewards + 4.0
        assert set(np.unique(replay_buffer._rewards)).issubset(
            set(6.0 * np.array([0, 1]) + 4.0))



    trainer = IQLTrainer(
        env=eval_env,
        policy=policy,
        qf1=qf1,
        qf2=qf2,
        target_qf1=target_qf1,
        target_qf2=target_qf2,
        vf=vf,
        **variant['trainer_kwargs'],
    )
    algorithm = TorchBatchRLAlgorithm(
        trainer=trainer,
        exploration_env=expl_env,
        evaluation_env=eval_env,
        exploration_data_collector=expl_path_collector,
        evaluation_data_collector=eval_path_collector,
        replay_buffer=replay_buffer,
        eval_both=False,
        batch_rl=True,
        **variant['algorithm_kwargs']
    )
    video_func = VideoSaveFunction(variant)
    algorithm.post_epoch_funcs.append(video_func)

    algorithm.to(ptu.device)
    algorithm.train(comet_logger=comet_logger)


def enable_gpus(gpu_str):
    if (gpu_str is not ""):
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_str
    return


if __name__ == "__main__":
    # noinspection PyTypeChecker
    
    
    comet_exp = comet_ml.Experiment(
        api_key='QsmVNJzwh5dbTTI6ECRGBtZfm',
        project_name='cog_project',
        workspace="jbakams"
    )
    logger = Log(PATH='/home/jey/cog/logs')
    comet_exp.add_tag("project")
    comet_exp.set_name("iql_3")
    comet_exp.set_filename(fname="cometML_test")
    logger._logger.set_comet_logger(comet_exp)
    
    variant = dict(
        algorithm="CQL",
        version="normal",
        algorithm_kwargs=dict(
            # num_epochs=100,
            # num_eval_steps_per_epoch=50,
            # num_trains_per_train_loop=100,
            # num_expl_steps_per_train_loop=100,
            # min_num_steps_before_training=100,
            # max_path_length=10,
            num_epochs=3000,
            num_eval_steps_per_epoch=300,
            num_trains_per_train_loop=1000,
            num_expl_steps_per_train_loop=1000,
            min_num_steps_before_training=1000,
            max_path_length=30,
            batch_size=256,
        ),
        
        trainer_kwargs=dict(
        discount=0.99,
        policy_lr=3E-4,
        qf_lr=3E-4,
        reward_scale=1,

        policy_weight_decay=0,
        q_weight_decay=0,

        #reward_transform_kwargs=dict(m=1, b=-1),
        terminal_transform_kwargs=None,

        beta=0.1,
        quantile=0.9,
        clip_score=100,
        
        policy_eval_start=10000,
   	 ),
   	 
        cnn_params=dict(
            kernel_sizes=[3, 3, 3],
            n_channels=[16, 16, 16],
            strides=[1, 1, 1],
            hidden_sizes=[1024, 512, 256],
            paddings=[1, 1, 1],
            pool_type='max2d',
            pool_sizes=[2, 2, 1],  # the one at the end means no pool
            pool_strides=[2, 2, 1],
            pool_paddings=[0, 0, 0],
            image_augmentation=True,
            image_augmentation_padding=4,
        ),
        dump_video_kwargs=dict(
            imsize=48,
            save_video_period=1,
        ),
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, required=True)
    parser.add_argument("--max-path-length", type=int, required=True)
    parser.add_argument("--prior-buffer", type=str, default=DEFAULT_PRIOR_BUFFER)
    parser.add_argument("--task-buffer", type=str, default=DEFAULT_TASK_BUFFER)
    parser.add_argument("--gpu", default='0', type=str)
    parser.add_argument("--min-q-weight", default=1.0, type=float,
                        help="Value of alpha in CQL")
    parser.add_argument("--use-lagrange", action="store_true", default=False)
    parser.add_argument("--lagrange-thresh", default=5.0, type=float,
                        help="Value of tau, used with --use-lagrange")
    parser.add_argument("--use-positive-rew", action="store_true", default=False)
    parser.add_argument("--max-q-backup", action="store_true", default=False,
                        help="For max_{a'} backups, set this to true")
    parser.add_argument("--no-deterministic-backup", action="store_true",
                        default=False,
                        help="By default, deterministic backup is used")
    parser.add_argument("--policy-eval-start", default=10000,
                        type=int)
    parser.add_argument("--policy-lr", default=1e-4, type=float)
    parser.add_argument("--min-q-version", default=3, type=int,
                        help=("min_q_version = 3 (CQL(H)), "
                              "version = 2 (CQL(rho))"))
    parser.add_argument("--num-eval-per-epoch", type=int, default=5)
    parser.add_argument("--seed", default=10, type=int)

    args = parser.parse_args()
    enable_gpus(args.gpu)
    variant['env'] = args.env
    variant['algorithm_kwargs']['max_path_length'] = args.max_path_length
    variant['algorithm_kwargs']['num_eval_steps_per_epoch'] = \
        args.num_eval_per_epoch*args.max_path_length

    variant['prior_buffer'] = args.prior_buffer
    variant['task_buffer'] = args.task_buffer

    """variant['trainer_kwargs']['max_q_backup'] = args.max_q_backup
    variant['trainer_kwargs']['deterministic_backup'] = \
        not args.no_deterministic_backup
    variant['trainer_kwargs']['min_q_weight'] = args.min_q_weight
    variant['trainer_kwargs']['policy_lr'] = args.policy_lr
    variant['trainer_kwargs']['min_q_version'] = args.min_q_version
    variant['trainer_kwargs']['policy_eval_start'] = args.policy_eval_start
    variant['trainer_kwargs']['lagrange_thresh'] = args.lagrange_thresh
    variant['trainer_kwargs']['with_lagrange'] = args.use_lagrange"""

    # Translate 0/1 rewards to +4/+10 rewards.
    variant['use_positive_rew'] = args.use_positive_rew
    variant['seed'] = args.seed

    ptu.set_gpu_mode(True)
    exp_prefix = 'cql-iql-{}'.format(args.env)
    if os.path.isdir(CUSTOM_LOG_DIR):
        base_log_dir = CUSTOM_LOG_DIR
    else:
        base_log_dir = None

    setup_logger(exp_prefix, variant=variant, base_log_dir=base_log_dir,
                 snapshot_mode='gap_and_last', snapshot_gap=10,)
    experiment(variant, logger)
