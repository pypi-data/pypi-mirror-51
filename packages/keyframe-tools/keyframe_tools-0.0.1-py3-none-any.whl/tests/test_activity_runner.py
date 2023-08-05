import unittest
import numpy as np

from keyframe_tools.ActivityRunner import ActivityRunner
from keyframe_tools.Player import Player


class TestActivityRunner(unittest.TestCase):

    def test_assert_if_no_movers_on_step(self):

        activity_runner = ActivityRunner()
        self.assertRaises(
            RuntimeError,
            activity_runner.step
        )

    def test_append_movement(self):
        activity_runner = ActivityRunner(make_mover(), make_mover())
        activity_runner._append_movement(make_mover())
        activity_runner.append_movements(make_mover(), make_mover(), make_mover())
        self.assertEqual(
            6,
            len(activity_runner._movements)
        )

    def test_is_finished(self):
        num_movers = 3
        activity_runner = ActivityRunner(*[make_mover()]*num_movers)
        for _ in range(num_movers*NUM_MOVES_PER_MOVER):
            activity_runner.step()
            self.assertFalse(activity_runner.is_finished)

        for _ in range(num_movers*NUM_MOVES_PER_MOVER):
            activity_runner.step()
            self.assertTrue(activity_runner.is_finished)

    def test_all_poses_are_reached(self):
        names = ['joint1', 'joint2', 'joint3']
        positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        repetitions = 1
        step_size = 1
        is_move_forward_then_backwards = False
        is_remove_unchanging_keyframe_indicies = False
        num_movers = 3
        activity_runner = ActivityRunner(
            *[Player(
                names=names,
                positions=positions,
                repetitions=repetitions,
                step_size=step_size,
                is_move_forward_then_backwards=is_move_forward_then_backwards,
                is_remove_unchanging_keyframe_indicies=is_remove_unchanging_keyframe_indicies,
            )]*num_movers,
        )
        for i in range(num_movers*len(positions)):
            out = activity_runner.step()
            _names, _positions = out
            self.assertEqual(names, _names)
            self.assertTrue(all(positions[i % len(positions)] == _positions))

        for _ in range(num_movers*len(positions)):
            activity_runner.step()



NUM_MOVES_PER_MOVER = 4


def make_mover():
    return Player(
        names=['joint1', 'joint2', 'joint3'],
        positions=np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ]),
        repetitions=1,
        step_size=1,
        is_move_forward_then_backwards=False,
        is_remove_unchanging_keyframe_indicies=True,
    )
