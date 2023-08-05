import numpy as np

from keyframe_tools.Player import Player
from keyframe_tools import config


def segue_to_movement(
        current_names,
        current_positions,
        movement,
        step_size=config.STEP_SIZE,
        is_degrees=config.IS_DEGREES,
        is_remove_unchanging_indicies=config.IS_REMOVE_UNCHANGING_KEYFRAMES,
):

    current_dict = dict(zip(current_names, current_positions))
    desired_dict = movement.get_first_frame(is_dict=True)

    if current_dict != desired_dict:
        current_dict_ = _add_non_matching_keys_as_default_value(current_dict, desired_dict)
        desired_dict_ = _add_non_matching_keys_as_default_value(desired_dict, current_dict)

        keys = list(current_dict_.keys())
        current_values = list(current_dict_.values())
        desired_values = [desired_dict_[k] for k in keys]
        positions = np.array([current_values, desired_values])
        return Player(
            names=keys,
            positions=positions,
            repetitions=1,
            is_move_forward_then_backwards=False,
            step_size=step_size,
            is_keyframes_using_degrees=is_degrees,
            is_remove_unchanging_keyframe_indicies=is_remove_unchanging_indicies,
        )


def _add_non_matching_keys_as_default_value(dict_, dict_with_new_keys, default_value=0):
    keys_set = {*dict_}
    new_keys = {*dict_with_new_keys}.difference(keys_set)

    _dict = {**dict_, **{}.fromkeys(new_keys, default_value)}

    return _dict

