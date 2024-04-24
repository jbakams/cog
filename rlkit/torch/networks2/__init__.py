"""
General networks for pytorch.

Algorithm-specific networks should go else-where.
"""
from rlkit.torch.networks2.basic import (
    Clamp, ConcatTuple, Detach, Flatten, FlattenEach, Split, Reshape,
)
from rlkit.torch.networks2.cnn import BasicCNN, CNN, MergedCNN, CNNPolicy
from rlkit.torch.networks2.dcnn import DCNN, TwoHeadDCNN
from rlkit.torch.networks2.feat_point_mlp import FeatPointMlp
from rlkit.torch.networks2.image_state import ImageStatePolicy, ImageStateQ
from rlkit.torch.networks2.linear_transform import LinearTransform
from rlkit.torch.networks2.normalization import LayerNorm
from rlkit.torch.networks2.mlp import (
    Mlp, ConcatMlp, MlpPolicy, TanhMlpPolicy,
    MlpQf,
    MlpQfWithObsProcessor,
    ConcatMultiHeadedMlp,
)
from rlkit.torch.networks2.pretrained_cnn import PretrainedCNN
from rlkit.torch.networks2.two_headed_mlp import TwoHeadMlp

__all__ = [
    'Clamp',
    'ConcatMlp',
    'ConcatMultiHeadedMlp',
    'ConcatTuple',
    'BasicCNN',
    'CNN',
    'CNNPolicy',
    'DCNN',
    'Detach',
    'FeatPointMlp',
    'Flatten',
    'FlattenEach',
    'LayerNorm',
    'LinearTransform',
    'ImageStatePolicy',
    'ImageStateQ',
    'MergedCNN',
    'Mlp',
    'PretrainedCNN',
    'Reshape',
    'Split',
    'TwoHeadDCNN',
    'TwoHeadMlp',
]

