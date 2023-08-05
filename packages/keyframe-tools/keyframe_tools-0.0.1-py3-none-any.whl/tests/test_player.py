import unittest
import numpy as np

from keyframe_tools.Player import Player


class TestMover(unittest.TestCase):

    def test_1d_names(self):

        names = ['joint1', 'joint2', 'joint3']
        positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        repetitions = 1
        step_size = 1

        mover = Player(
            names,
            positions,
            repetitions,
            step_size=step_size,
            is_remove_unchanging_keyframe_indicies=False,
        )
        out = mover.step()
        _names, _positions = out
        self.assertEqual(names, _names)

    def test_2d_names(self):

        names = [
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
        ]
        positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        repetitions = 1
        step_size = 1

        mover = Player(
            names,
            positions,
            repetitions,
            step_size=step_size,
            is_remove_unchanging_keyframe_indicies=False,
        )
        out = mover.step()
        _names, _positions = out
        self.assertEqual(names[0], _names)

    def test_step(self):
        names = [
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
        ]
        positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        repetitions = 1
        step_size = 1

        mover = Player(
            names,
            positions,
            repetitions,
            step_size=step_size,
            is_remove_unchanging_keyframe_indicies=False,
        )
        for i in range(len(positions)):
            out = mover.step()
            _names, _positions = out
            self.assertEqual(names[i], _names)
            self.assertTrue(all(positions[i] == _positions),
                            msg=f"Failed for i={i}: {positions[i]} != {_positions}")
        for _ in range(len(positions)):
            out = mover.step()
            _names, _positions = out
            self.assertEqual(names[0], _names)
            self.assertTrue(all(positions[-1] == _positions),
                            msg=f"Failed: {positions[-1]} != {_positions}")

    def test_step_with_removing_unchanging(self):
        names = [
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
        ]
        positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        repetitions = 1
        step_size = 1

        mover = Player(
            names,
            positions,
            repetitions,
            step_size=step_size,
            is_remove_unchanging_keyframe_indicies=True,
        )
        for i in range(len(positions)):
            out = mover.step()
            _names, _positions = out
            self.assertEqual(names[i][1:], _names)
            self.assertTrue(all(positions[i][1:] == _positions),
                            msg=f"Failed for i={i}: {positions[i][1:]} != {_positions}")
        for _ in range(len(positions)):
            out = mover.step()
            _names, _positions = out
            self.assertEqual(names[i][1:], _names)
            self.assertTrue(all(positions[-1][1:] == _positions),
                            msg=f"Failed: {positions[-1][1:]} != {_positions}")

    def test_is_finished(self):
        names = [
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
            ['joint1', 'joint2', 'joint3'],
        ]
        positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        repetitions = 1
        step_size = 1

        mover = Player(
            names,
            positions,
            repetitions,
            step_size=step_size,
            is_move_forward_then_backwards=False,
            is_remove_unchanging_keyframe_indicies=True,
        )
        for _ in range(len(positions)):
            mover.step()
            self.assertFalse(mover.is_finished)
        for _ in range(len(positions)):
            mover.step()
            self.assertTrue(mover.is_finished)

    def test_reset(self):
        names = ['joint1', 'joint2', 'joint3']
        positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        repetitions = 1
        step_size = 1

        mover = Player(
            names,
            positions,
            repetitions,
            step_size=step_size,
            is_move_forward_then_backwards=False,
            is_remove_unchanging_keyframe_indicies=True,
        )
        for _ in range(10):
            for _ in range(len(positions)):
                mover.step()
                self.assertFalse(mover.is_finished)
            mover.step()
            self.assertTrue(mover.is_finished)
            mover.reset()

    def test_get_first_and_last_frames(self):
        names = ['joint1', 'joint2', 'joint3']
        positions = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 1],
        ])
        repetitions = 1
        step_size = 1

        mover = Player(
            names,
            positions,
            repetitions,
            step_size=step_size,
            is_move_forward_then_backwards=False,
            is_remove_unchanging_keyframe_indicies=False,
        )

        self.assertTrue(
            all(
                positions[0] == mover.get_first_frame()[1]
            )
        )
        self.assertTrue(
            all(
                positions[-1] == mover.get_last_frame()[1]
            )
        )
