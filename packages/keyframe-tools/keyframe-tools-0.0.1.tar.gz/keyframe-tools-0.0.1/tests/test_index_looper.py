import unittest

from keyframe_tools.IndexLooper import IndexLooper


class TestIndexLooper(unittest.TestCase):

    def test_step_forward_loop(self):

        for num_eles in [2, 3, 5, 10]:
            for num_repetitions in [1, 2, 3, 5, 10]:
                looper = IndexLooper(
                    num_eles,
                    is_move_forward_then_backwards=False,
                    num_repetitions=num_repetitions,
                )

                out = []
                for _ in range(num_eles*num_repetitions):
                    looper.increment_index()
                    out.append(looper.idx)

                truth_array = [i for i in range(num_eles)]*num_repetitions
                self.assertEqual(
                    truth_array,
                    out,
                    f"Failed with {num_repetitions} rep for {num_eles} elements"
                )

    def test_step_forward_then_backwards_loop(self):

        for num_eles in [2, 3, 5, 10]:
            for num_repetitions in [1, 2, 3, 5, 10]:
                looper = IndexLooper(
                    num_eles,
                    is_move_forward_then_backwards=True,
                    num_repetitions=num_repetitions,
                )

                out = []
                for _ in range(1 + num_repetitions*2*(num_eles-1)):
                    looper.increment_index()
                    out.append(looper.idx)

                base = [i for i in range(num_eles)]
                truth_array = [base[0]] + (base[1:] + base[-2::-1]) * num_repetitions
                self.assertEqual(
                    truth_array,
                    out,
                    f"Failed with {num_repetitions} rep for {num_eles} elements"
                )

    def test_terminate_forward_loop(self):

        for num_eles in [2, 3, 5, 10]:
            for num_repetitions in [1, 2, 3, 5, 10]:
                looper = IndexLooper(
                    num_eles,
                    is_move_forward_then_backwards=False,
                    num_repetitions=num_repetitions,
                )

                for _ in range(1 + num_repetitions*num_eles):
                    self.assertFalse(
                        looper.is_finished,
                        msg=f"Failed for {num_eles} elements with {num_repetitions} reps"
                    )
                    looper.increment_index()

                out = []
                self.assertTrue(looper.is_finished)

                for _ in range(num_eles):
                    looper.increment_index()
                    self.assertTrue(looper.is_finished)
                    out.append(looper.idx)

                self.assertEqual(
                    [num_eles-1 for _ in range(num_eles)],
                    out
                )

    def test_terminate_forward_then_backwards_loop(self):

        for num_eles in [2, 3, 5, 10]:
            for num_repetitions in [1, 2, 3, 5, 10]:
                looper = IndexLooper(
                    num_eles,
                    is_move_forward_then_backwards=True,
                    num_repetitions=num_repetitions,
                )

                for _ in range(1 + num_repetitions * 2 * (num_eles - 1)):
                    self.assertFalse(looper.is_finished)
                    looper.increment_index()

                out = [looper.increment_index()]
                self.assertTrue(looper.is_finished)

                for _ in range(num_eles):
                    looper.increment_index()
                    self.assertTrue(looper.is_finished)
                    out.append(looper.idx)

                self.assertEqual(
                    [0 for _ in range(num_eles+1)],
                    out
                )

    def test_jump_index(self):
        num_eles = 10
        looper = IndexLooper(
            num_eles,
            is_move_forward_then_backwards=False,
            is_only_jump_forward=False,
        )
        for i in range(num_eles):
            self.assertEqual(
                i,
                looper.jump_normalized_index(i/(num_eles-1))
            )
        for i in range(num_eles-1, -1, -1):
            self.assertEqual(
                i,
                looper.jump_normalized_index(i/(num_eles-1))
            )

    def test_jump_index_only_forward(self):
        num_eles = 10
        looper = IndexLooper(
            num_eles,
            is_move_forward_then_backwards=False,
            is_only_jump_forward=True,
        )
        for i in range(num_eles):
            self.assertEqual(
                i,
                looper.jump_normalized_index(i/(num_eles-1))
            )
        for i in range(num_eles-1, -1, -1):
            self.assertEqual(
                num_eles-1,
                looper.jump_normalized_index(i/(num_eles-1))
            )

    def test_exceptions_on_bad_constructor(self):

        for n in [-1, 1]:
            self.assertRaises(
                ValueError,
                IndexLooper,
                num_elements=n,
            )

        for r in [-1, 0]:
            self.assertRaises(
                ValueError,
                IndexLooper,
                num_elements=2,
                num_repetitions=r,
            )

    def test_reset(self):

        for num_eles in [2, 3, 5, 10]:
            for num_repetitions in [1, 2, 3, 5, 10]:
                looper = IndexLooper(
                    num_eles,
                    is_move_forward_then_backwards=True,
                    num_repetitions=num_repetitions,
                )

                for _ in range(10):
                    for _ in range(1 + num_repetitions * 2 * (num_eles - 1)):
                        self.assertFalse(looper.is_finished)
                        looper.increment_index()

                    looper.increment_index()
                    self.assertTrue(looper.is_finished)
                    looper.reset()
