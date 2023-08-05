import unittest
import numpy as np

from keyframe_tools.Follower import Follower


class TestFollower(unittest.TestCase):

    def test_call_function_on_step(self):

        _names = ['joint1', 'joint2', 'joint3']
        _positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        _repetitions = 5
        _step_size = 1

        num_calls = 0

        def p_func():
            nonlocal num_calls
            value = min(1, num_calls / len(_positions))
            num_calls += 1
            return value

        _follower = Follower(
            p_func,
            _names,
            _positions,
            repetitions=_repetitions,
            step_size=_step_size,
            is_move_forward_then_backwards=False,
            is_remove_unchanging_keyframe_indicies=True,
        )
        for i in range(_repetitions * len(_positions)):
            self.assertEquals(
                i,
                num_calls
            )
            _follower.step()
