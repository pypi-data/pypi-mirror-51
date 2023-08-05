import math
import numpy as np

from keyframe_tools import utils


def find_closest_keyframe_index(
        keyframes,
        target,
        is_return_distance=False,
        is_degrees=True
):

    if not keyframes:
        raise ValueError("Must have more than 0 _positions")

    best_idx = None
    min_dist = math.inf
    for i in range(len(keyframes)):
        dist = np.linalg.norm(
            utils.angle_diff_arrays(keyframes[i], target, is_degrees=is_degrees)
        )
        if dist < min_dist:
            best_idx = i
            min_dist = dist

    if is_return_distance:
        return best_idx, min_dist
    else:
        return best_idx
