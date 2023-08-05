import numpy as np

from keyframe_tools.Mover import Mover
from keyframe_tools import config


class Follower(Mover):

    def __init__(
            self,
            function_to_check_performance,
            names,
            positions,
            repetitions=1,
            is_move_forward_then_backwards=False,
            is_only_jump_forward=False,
            step_size=config.STEP_SIZE,
            is_keyframes_using_degrees=config.IS_DEGREES,
            is_remove_unchanging_keyframe_indicies=config.IS_REMOVE_UNCHANGING_KEYFRAMES,
    ):
        super().__init__(
            names,
            positions,
            repetitions=repetitions,
            step_size=step_size,
            is_move_forward_then_backwards=is_move_forward_then_backwards,
            is_keyframes_using_degrees=is_keyframes_using_degrees,
            is_remove_unchanging_keyframe_indicies=is_remove_unchanging_keyframe_indicies,
            is_only_jump_forward=is_only_jump_forward,
        )
        self._performance_function = function_to_check_performance

    def step(self):
        status = self._performance_function()
        self._index_looper.jump_normalized_index(status)
        return self.get_frame()

if __name__ == '__main__':

    _names = ['joint1', 'joint2', 'joint3']
    _positions = np.array([
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 1],
        [0, 0, 1],
    ])
    _repetitions = 2
    _step_size = 1

    def gen_performance_function():
        num_calls = 0

        def p_func():
            nonlocal num_calls
            value = min(1, num_calls/len(_positions))
            num_calls += 1
            return value
        return p_func

    _follower = Follower(
        gen_performance_function(),
        _names,
        _positions,
        repetitions=_repetitions,
        step_size=_step_size,
        is_move_forward_then_backwards=False,
        is_remove_unchanging_keyframe_indicies=True,
    )
    for _ in range(_repetitions * len(_positions)):
        _out = _follower.step()
        print(_out)
