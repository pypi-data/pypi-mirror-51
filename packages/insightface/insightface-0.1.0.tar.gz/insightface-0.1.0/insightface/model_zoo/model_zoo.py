# pylint: disable=wildcard-import, unused-wildcard-import
"""Model store which handles pretrained models from both
mxnet.gluon.model_zoo.vision and gluoncv.models
"""
from .face_recognition import *
from .face_detection import *
#from .face_alignment import *

__all__ = ['get_model', 'get_model_list']

_models = {
    'arcface_r100_v1': arcface_r100_v1,
    'arcface_mfn_v1': arcface_mfn_v1,
    'arcface_outofreach_v1': arcface_outofreach_v1,
    'retinaface_r50_v1': retinaface_r50_v1,
}


def get_model(name, **kwargs):
    """Returns a pre-defined model by name

    Parameters
    ----------
    name : str
        Name of the model.
    root : str, default '~/.insightface/models'
        Location for keeping the model parameters.

    Returns
    -------
    Model
        The model.
    """
    name = name.lower()
    if name not in _models:
        err_str = '"%s" is not among the following model list:\n\t' % (name)
        err_str += '%s' % ('\n\t'.join(sorted(_models.keys())))
        raise ValueError(err_str)
    net = _models[name](**kwargs)
    return net


def get_model_list():
    """Get the entire list of model names in model_zoo.

    Returns
    -------
    list of str
        Entire list of model names in model_zoo.

    """
    return _models.keys()

