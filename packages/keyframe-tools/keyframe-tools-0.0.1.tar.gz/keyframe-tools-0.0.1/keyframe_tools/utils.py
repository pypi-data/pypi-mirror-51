import math
import numpy as np


def angle_diff_arrays(array1, array2, is_degrees=True):

    if not is_1d_array(array1) or not is_1d_array(array2):
        raise ValueError("Arrays must be a one dimensional numpy.ndarray")

    if not len(array1) == len(array2):
        raise ValueError("Arrays must be the same length")

    result = np.zeros(len(array1))
    for i in range(len(array1)):
        result[i] = angle_diff(array1[i], array2[i], is_degrees=is_degrees)
    return result


def angle_diff(angle1, angle2, is_degrees=True):

    if is_degrees:
        angle1 = math.radians(angle1)
        angle2 = math.radians(angle2)

    result = -math.atan2(math.sin(angle1-angle2), math.cos(angle1-angle2))
    if result == -math.pi:
        result = math.pi

    if is_degrees:
        result = math.degrees(result)

    return result


def is_1d_array(array):
    return type(array) is np.ndarray and array.ndim == 1


def find_changing_indicies(lists):

    # check all lists are the same length
    if not (all(len(l) == len(lists[0]) for l in lists)):
        raise ValueError("Arrays must be equal in length")

    changing_indicies = []
    for i in range(len(lists[0])):
        # check if the i-th element in all lists are equal
        if not all(l[i] == lists[0][i] for l in lists):
            changing_indicies.append(i)

    return changing_indicies


def get_proportional_index(normalized_value, array_length):
    if not (0 <= normalized_value <= 1):
        raise ValueError("Normalized value must between 0 and 1")
    return int(normalized_value * (array_length - 1))


def get_linear_distance_between_bounds(value, lower_bound, upper_bound):
    if upper_bound <= lower_bound:
        raise ValueError("Lower bound must be strictly less than upper bound")
    value = clip(value, lower_bound, upper_bound)
    return (value - lower_bound) / (upper_bound - lower_bound)


def clip(value, min_limit=None, max_limit=None):
    if min_limit is not None:
        value = max(value, min_limit)
    if max_limit is not None:
        value = min(value, max_limit)
    return value