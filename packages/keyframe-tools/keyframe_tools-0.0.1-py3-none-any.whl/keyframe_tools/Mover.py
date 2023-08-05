import numpy as np

from keyframe_tools.IndexLooper import IndexLooper
from keyframe_tools.interpolator import interpolate_keyframes

from keyframe_tools import utils, config


class Mover:

    def __init__(
            self,
            names,
            positions,
            repetitions=1,
            is_move_forward_then_backwards=False,
            step_size=config.STEP_SIZE,
            is_keyframes_using_degrees=config.IS_DEGREES,
            is_remove_unchanging_keyframe_indicies=config.IS_REMOVE_UNCHANGING_KEYFRAMES,
            is_only_jump_forward=config.IS_ONLY_JUMP_FORWARD_ON_FOLLOWER,
    ):

        # Collapse _names into one dimensional list
        if isinstance(names[0], list):
            if not all(n == names[0] for n in names):
                raise ValueError("Each sublist in _names must be the same")
            names = names[0]

        if is_remove_unchanging_keyframe_indicies:
            idxs = utils.find_changing_indicies(positions)
            if len(idxs) > 0:
                names = [names[i] for i in idxs]
                positions = [np.array([j[i] for i in idxs]) for j in positions]

        self._names = names
        self._is_degrees = is_keyframes_using_degrees
        self._waypoints = interpolate_keyframes(
            positions,
            step_size=step_size,
            is_degrees=is_keyframes_using_degrees,
        )
        self._index_looper = IndexLooper(
            num_elements=len(self._waypoints),
            num_repetitions=repetitions,
            is_move_forward_then_backwards=is_move_forward_then_backwards,
            is_only_jump_forward=is_only_jump_forward,
        )

    @property
    def is_finished(self):
        return self._index_looper.is_finished

    @property
    def keyframe(self):
        idx = self._index_looper.idx
        return self._waypoints[idx]

    @property
    def names(self):
        return self._names

    @property
    def is_degrees(self):
        return self._is_degrees

    def get_frame(self, idx=None, is_dict=False):
        if idx is None:
            idx = self._index_looper.idx
        if is_dict:
            return dict(zip(self.names, self._waypoints[idx]))
        else:
            return self.names, self._waypoints[idx]

    def get_first_frame(self, is_dict=False):
        return self.get_frame(idx=0, is_dict=is_dict)

    def get_last_frame(self, is_dict=False):
        return self.get_frame(idx=-1, is_dict=is_dict)

    def reset(self):
        self._index_looper.reset()

    def step(self):
        raise NotImplementedError
