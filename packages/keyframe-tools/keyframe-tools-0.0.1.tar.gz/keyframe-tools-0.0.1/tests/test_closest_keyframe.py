import unittest
import numpy as np

from keyframe_tools import closest_keyframe


class TestClosestKeyframe(unittest.TestCase):

    def test_determine_closest_keyframe(self):
        keyframe = (
            np.array([0, 0, 0]),
            np.array([0, 90, 90])
        )
        locations_closer_to_first_keyframe = (
            np.array([0, 0, 0]),
            np.array([0, 10, 0]),
            np.array([-10, 0, 0]),
        )
        locations_closer_to_second_keyframe = (
            np.array([0, 90, 90]),
            np.array([0, 80, 90]),
            np.array([-10, 90, 90]),
        )

        for l in locations_closer_to_first_keyframe:
            self.assertEqual(
                closest_keyframe.find_closest_keyframe_index(keyframes=keyframe, target=l),
                0
            )
        for l in locations_closer_to_second_keyframe:
            self.assertEqual(
                closest_keyframe.find_closest_keyframe_index(keyframes=keyframe, target=l),
                1
            )

    def test_empty_keyframes_list(self):
        self.assertRaises(
            ValueError,
            closest_keyframe.find_closest_keyframe_index,
            (),
            np.array([0, 0, 0]),
        )
