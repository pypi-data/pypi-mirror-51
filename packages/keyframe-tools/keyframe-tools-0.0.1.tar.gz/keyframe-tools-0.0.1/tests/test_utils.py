import unittest
import numpy as np
import math

from keyframe_tools import utils


class TestUtils(unittest.TestCase):

    def test_angle_difference(self):
        self.assertAlmostEqual(0, utils.angle_diff(0, 0, is_degrees=True))
        self.assertAlmostEqual(45, utils.angle_diff(0, 45, is_degrees=True))
        self.assertAlmostEqual(-45, utils.angle_diff(0, -45, is_degrees=True))
        self.assertAlmostEqual(180, utils.angle_diff(0, 180, is_degrees=True))
        self.assertAlmostEqual(180, utils.angle_diff(180, 0, is_degrees=True))
        self.assertAlmostEqual(179, utils.angle_diff(0, 179, is_degrees=True))
        self.assertAlmostEqual(-179, utils.angle_diff(0, -179, is_degrees=True))
        self.assertAlmostEqual(90, utils.angle_diff(90, 180, is_degrees=True))

        self.assertAlmostEqual(0, utils.angle_diff(math.pi, math.pi, is_degrees=False))
        self.assertAlmostEqual(0, utils.angle_diff(0, 2 * math.pi, is_degrees=False))

        self.assertAlmostEqual(0, utils.angle_diff(0, 2 * 6 * 360, is_degrees=True))
        self.assertAlmostEqual(0, utils.angle_diff(0, 2 * 6 * math.pi, is_degrees=False))

    def test_get_angle_diff_for_numpy_arrays(self):
        self.assertTrue(
            np.array_equal(
                np.array([0, 0, 0, 0, 0]),
                utils.angle_diff_arrays(
                    np.array([0, 90, 180, 360, 450]),
                    np.array([0, 90, 180, 360, 450]),
                    is_degrees=True
                )
            )
        )
        self.assertTrue(
            np.allclose(
                np.array([0, 90, 180, 0, 90]),
                utils.angle_diff_arrays(
                    np.array([0, 0, 0, 0, 0]),
                    np.array([0, 90, 180, 360, 450]),
                    is_degrees=True
                ),
            )
        )

    def test_exceptions_for_get_angle_diff_for_numpy_arrays(self):
        self.assertRaises(
            ValueError,
            utils.angle_diff_arrays,
            np.array([0, 180, 360, 450]),
            np.array([0, 90, 180, 360, 450]),
        )
        self.assertRaises(
            ValueError,
            utils.angle_diff_arrays,
            np.array([0, 90, 180, 360, 450]),
            np.array([0, 180, 360, 450]),
        )

        self.assertRaises(
            ValueError,
            utils.angle_diff_arrays,
            np.array([[1, 3], [2, 4]]),
            np.array([0, 90, 180, 360, 450]),
        )
        self.assertRaises(
            ValueError,
            utils.angle_diff_arrays,
            np.array([0, 90, 180, 360, 450]),
            np.array([[1, 3], [2, 4]]),
        )
        self.assertRaises(
            ValueError,
            utils.angle_diff_arrays,
            np.array([[1, 3], [2, 4]]),
            np.array([[1, 3], [2, 4]]),
        )

    def test_find_changing_indicies(self):
        array = [1, 2, 3]

        self.assertEqual(
            [],
            utils.find_changing_indicies([array, array])
        )
        self.assertEqual(
            [],
            utils.find_changing_indicies([array, array, array])
        )
        self.assertEqual(
            [1],
            utils.find_changing_indicies([array, [1, 200, 3]])
        )
        self.assertEqual(
            [0, 1, 2],
            utils.find_changing_indicies([array, [100, 200, 300]])
        )
        self.assertEqual(
            [0, 1, 2],
            utils.find_changing_indicies([array, array, array, [100, 200, 300]])
        )

    def test_bad_input_for_find_changing_indicies(self):
        array = [1, 2, 3]
        self.assertRaises(
            ValueError,
            utils.find_changing_indicies,
            [
                array,
                array + [4]
            ]
        )

    def test_get_proportional_index(self):
        array_len = 10
        self.assertEqual(
            0,
            utils.get_proportional_index(0, array_len)
        )
        self.assertEqual(
            array_len-1,
            utils.get_proportional_index(1, array_len)
        )
        self.assertEqual(
            array_len/2-1,
            utils.get_proportional_index(.5, array_len)
        )
        self.assertEqual(
            round(array_len/4),
            utils.get_proportional_index(.25, array_len)
        )

    def test_input_out_of_range_on_get_proportional_index(self):

        array_len = 10
        self.assertRaises(
            ValueError,
            utils.get_proportional_index,
            -1, array_len
        )
        self.assertRaises(
            ValueError,
            utils.get_proportional_index,
            1.1, array_len
        )

    def test_get_linear_distance_between_bounds(self):

        self.assertEqual(
            0,
            utils.get_linear_distance_between_bounds(0, 0, 1)
        )

        self.assertEqual(
            1,
            utils.get_linear_distance_between_bounds(1, 0, 1)
        )

        self.assertEqual(
            0,
            utils.get_linear_distance_between_bounds(3, 3, 4)
        )
        self.assertEqual(
            1,
            utils.get_linear_distance_between_bounds(4, 3, 4)
        )

        self.assertEqual(
            0,
            utils.get_linear_distance_between_bounds(3, 3, 5.5)
        )
        self.assertEqual(
            1,
            utils.get_linear_distance_between_bounds(5.5, 3, 5.5)
        )

        self.assertEqual(
            0.5,
            utils.get_linear_distance_between_bounds(16.5, 10, 23)
        )

        self.assertEqual(
            0,
            utils.get_linear_distance_between_bounds(-1, 0, 1)
        )

        self.assertEqual(
            1,
            utils.get_linear_distance_between_bounds(2, 0, 1)
        )

    def test_out_of_range_input_for_get_linear_distance_between_bounds(self):
        self.assertRaises(
            ValueError,
            utils.get_linear_distance_between_bounds,
            0, 0, 0
        )
        self.assertRaises(
            ValueError,
            utils.get_linear_distance_between_bounds,
            0, 2, 1
        )

    def test_clip(self):
        self.assertEqual(
            10,
            utils.clip(10, 0)
        )
        self.assertEqual(
            0,
            utils.clip(-10, 0)
        )
        self.assertEqual(
            0,
            utils.clip(10, max_limit=0)
        )
        self.assertEqual(
            10,
            utils.clip(10, min_limit=0)
        )
        self.assertEqual(
            0,
            utils.clip(10, 0, 0)
        )
        self.assertEqual(
            1,
            utils.clip(10, 0, 1)
        )
