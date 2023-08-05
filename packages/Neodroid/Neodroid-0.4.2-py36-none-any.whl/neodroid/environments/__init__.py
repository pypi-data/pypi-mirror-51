#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .neodroid_environment import NeodroidEnvironment
from .batched_neodroid_environments import BatchedNeodroidEnvironment
from .vector_environment import VectorEnvironment

__author__ = 'cnheider'
__doc__ = ''


def make(environment_name: str = None, clones=0, *args, **kwargs) -> NeodroidEnvironment:
  _environments = NeodroidEnvironment(environment_name=environment_name,
                                      clones=clones,
                                      *args,
                                      **kwargs)
  return _environments


def seed(random_seed) -> None:
  import numpy as np
  np.random.seed(random_seed)


def connect(ip='localhost', port=6969, **kwargs) -> NeodroidEnvironment:
  _environments = NeodroidEnvironment(connect_to_running=True, ip=ip, port=port,**kwargs)
  return _environments
