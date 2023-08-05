# -*- coding: utf-8 -*-

from .base import dppd, register_verb, register_type_methods_as_verbs
from . import single_verbs  # noqa:F401

__version__ = "0.19"

__all_ = [dppd, register_verb, register_type_methods_as_verbs, __version__]
