#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Sequence

import numpy

from neodroid.interfaces.spaces import ActionSpace, signed_ternary_encoding, EnvironmentDescription
from neodroid.interfaces.specifications import Motion
from neodroid.utilities.transformations.action_transformations import normalise_action

__author__ = 'cnheider'

import numpy as np

from neodroid.interfaces import specifications as M




def maybe_infer_single_motion_reaction(*,
                                       input_reactions,
                                       normalise:bool,
                                       description:EnvironmentDescription,
                                       action_space: ActionSpace):
  '''

  :param action_space:
:param verbose:
:type verbose:
:param input_reactions:
:type input_reactions:
:param normalise:
:type normalise:
:param description:
:type description:
:return:
:rtype:
'''
  if description:
    out_reaction = construct_step_reaction(reaction_input=input_reactions,
                                           environment_description=description,
                                           normalise=normalise,
                                           space=action_space
                                           )
  else:
    out_reaction = construct_step_reaction(reaction_input=input_reactions,
                                           environment_description=None,
                                           normalise=False,
                                           space=action_space
                                           )

  return out_reaction


def maybe_infer_single_configuration_reaction(input_reaction,
                                              description:EnvironmentDescription):
  if description:
    input_reaction = verify_configuration_reaction(input_reaction=input_reaction,
                                                   environment_description=description
                                                   )
  else:
    input_reaction = verify_configuration_reaction(input_reaction=input_reaction,
                                                   environment_description=description)

  return input_reaction


# @debug_print_return_value
def construct_step_reaction(*,
                            reaction_input,
                            environment_description:EnvironmentDescription,
                            space:ActionSpace,
                            normalise:bool=False
                            ):
  """

  :param space:
  :param environment_description:
  :param normalise:
  :type reaction_input: object
  """
  if reaction_input is None:
    logging.info('Received empty reaction, Constructing empty counting terminal step reaction')
    parameters = M.ReactionParameters(terminable=True,
                                      step=True,
                                      episode_count=True)
    return M.Reaction(parameters=parameters)

  if isinstance(reaction_input, M.Reaction):
    return reaction_input
  if isinstance(reaction_input, list):
    if len(reaction_input) > 0 and numpy.array([isinstance(ri, M.Reaction) for ri in reaction_input]).all():
      return reaction_input

  if isinstance(reaction_input, dict):
    parameters = M.ReactionParameters(terminable=True,
                                      step=True,
                                      episode_count=True)
    if isinstance(list(reaction_input.values())[0], dict):
      return M.Reaction(parameters=parameters,
                        motions=[Motion(p, k, v)
                                 for p, a in reaction_input.items() for k, v in a.items()])

    return M.Reaction(parameters=parameters,
                      motions=[Motion('Actor', k, v)
                               for k, v in reaction_input.items()])

  if environment_description:
    parameters = M.ReactionParameters(terminable=True,
                                      step=True,
                                      episode_count=True)
    actors = environment_description.actors.values()
    if actors:
      if isinstance(reaction_input, M.Reaction):
        is_valid_motions = all(isinstance(m, M.Motion) for m in reaction_input.motions)
        if is_valid_motions:
          return reaction_input
        else:
          reaction_input.motions = construct_motions_from_list(reaction_input.motions,
                                                               actors,
                                                               normalise,
                                                               space)
          return reaction_input
      elif isinstance(reaction_input, list):
        is_valid_motions = all(isinstance(m, M.Motion) for m in reaction_input)
        if is_valid_motions:
          return M.Reaction(parameters=parameters,
                            motions=reaction_input)
        else:
          return construct_reaction_from_list(reaction_input,
                                              actors,
                                              normalise,
                                              space)
      elif isinstance(reaction_input, (int, float)):
        return construct_reaction_from_list([reaction_input],
                                            actors,
                                            normalise,
                                            space)
      elif isinstance(reaction_input, (np.ndarray, np.generic)):
        a = construct_reaction_from_list(reaction_input.astype(float).tolist(),
                                         actors,
                                         normalise,
                                         space)
        return a

  parameters = M.ReactionParameters(describe=True)
  return M.Reaction(parameters=parameters)


def construct_reaction_from_list(motion_list, actors, normalise, space):
  if not isinstance(motion_list, list):
    motion_list = [motion_list]
  motions = construct_motions_from_list(motion_list,
                                        actors,
                                        normalise,
                                        space)
  parameters = M.ReactionParameters(terminable=True,
                                    step=True,
                                    episode_count=True)
  return M.Reaction(motions=motions, parameters=parameters)


def construct_motions_from_list(input_list,
                                actors,
                                normalise:bool,
                                space: ActionSpace):
  actor_actuator_tuples = [(actor.actor_name,
                            actuator.actuator_name,
                            actuator.motion_space)
                           for actor in actors
                           for actuator in actor.actuators.values()
                           ]
  if isinstance(input_list[0], list):
    if len(input_list) == 1:
      input_list = input_list[0]

  if space.is_discrete:
    if (isinstance(input_list, Sequence) and len(input_list) == 1) or not isinstance(input_list, Sequence):
      input_list = signed_ternary_encoding(size=space.num_ternary_actions // 3,
                                           index=input_list)[0]

  if normalise:
    new_motions = [M.Motion(actor_actuator_tuple[0],
                            actor_actuator_tuple[1],
                            normalise_action(list_val,
                                             actor_actuator_tuple[2]),
                            )
                   for (list_val, actor_actuator_tuple) in zip(input_list, actor_actuator_tuples)
                   ]
    return new_motions
  else:
    new_motions = [M.Motion(actor_actuator_tuple[0],
                            actor_actuator_tuple[1],
                            list_val)
                   for (list_val, actor_actuator_tuple) in zip(input_list, actor_actuator_tuples)
                   ]
    return new_motions


# @print_return_value
def verify_configuration_reaction(*,
                                  input_reaction,
                                  environment_description: EnvironmentDescription):
  if environment_description:
    parameters = M.ReactionParameters(reset=True,
                                      configure=True,
                                      describe=True)
    configurables = environment_description.configurables.values()
    if configurables:
      if isinstance(input_reaction, M.Reaction):
        if input_reaction.configurations:
          is_valid_configurations = all(isinstance(m, M.Configuration) for m in input_reaction.configurations)
          if is_valid_configurations:
            return input_reaction
          else:
            input_reaction.motions(construct_configurations_from_known_observables(
                input_reaction.configurations,
                configurables
                )
                )
          return input_reaction
      elif isinstance(input_reaction, list):
        is_valid_configurations = all(isinstance(c, M.Configuration) for c in input_reaction)
        if is_valid_configurations:
          return M.Reaction(parameters=parameters, configurations=input_reaction)
        else:
          return construct_configuration_reaction_from_list(input_reaction, configurables)
      elif isinstance(input_reaction, (int, float)):
        return construct_configuration_reaction_from_list([input_reaction], configurables)
      elif isinstance(input_reaction, (np.ndarray, np.generic)):
        a = construct_configuration_reaction_from_list(input_reaction.astype(float).tolist(), configurables)
        return a
  if isinstance(input_reaction, M.Reaction):
    return input_reaction
  parameters = M.ReactionParameters(reset=True,
                                    configure=True,
                                    describe=True)
  return M.Reaction(parameters=parameters)


def construct_configuration_reaction_from_list(configuration_list, configurables):
  configurations = construct_configurations_from_known_observables(configuration_list,
                                                                   configurables
                                                                   )
  parameters = M.ReactionParameters(reset=True, configure=True, describe=True)
  return M.Reaction(parameters=parameters, configurations=configurations)


def construct_configurations_from_known_observables(input_list, configurables):
  new_configurations = [M.Configuration(configurable.configurable_name,
                                        list_val)
                        for (list_val, configurable) in zip(input_list, configurables)
                        ]
  return new_configurations
