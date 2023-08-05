import numpy as np

from keyframe_tools import utils, config


def interpolate_keyframes(
        keyframes,
        step_size=config.STEP_SIZE,
        is_degrees=config.IS_DEGREES
):

    if len(keyframes) < 1:
        raise ValueError("Must have at least one keyframe")

    result = [keyframes[0]]
    for i in range(1, len(keyframes)):
        intermediate_keyframes = _interpolate_two_keyframes(
            keyframes[i - 1],
            keyframes[i],
            step_size=step_size,
            is_degrees=is_degrees,
        )
        result = result + [*intermediate_keyframes[1:]]

    return tuple(result)


def _interpolate_two_keyframes(
        start_keyframe,
        end_keyframe,
        step_size=config.STEP_SIZE,
        is_degrees=config.IS_DEGREES,
):

    if step_size <= 0:
        raise ValueError("Stepsize must be a positive real number")

    current_keyframe = start_keyframe
    intermediate_keyframes = [start_keyframe]
    while True:
        keyframe_diff = utils.angle_diff_arrays(
            current_keyframe,
            end_keyframe,
            is_degrees=is_degrees
        )
        norm_of_diff_keyframe = np.linalg.norm(keyframe_diff)
        if np.isclose(norm_of_diff_keyframe, 0):
            break
        elif norm_of_diff_keyframe >= step_size:
            d_keyframe = step_size*keyframe_diff/norm_of_diff_keyframe
        else:
            d_keyframe = keyframe_diff
        current_keyframe = current_keyframe + d_keyframe
        intermediate_keyframes.append(current_keyframe)

    return tuple(intermediate_keyframes)
