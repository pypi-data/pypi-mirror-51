import unittest
import numpy as np

from keyframe_tools import interpolator, utils


NUMERICAL_TOLERANCE = 1e-6


class TestInterpolator(unittest.TestCase):

    def test_valid_step_size(self):
        self.assertRaises(
            ValueError,
            interpolator._interpolate_two_keyframes,
            start_keyframe=np.array([0, 0, 0]),
            end_keyframe=np.array([0, 0, 1]),
            step_size=0
        )
        self.assertRaises(
            ValueError,
            interpolator._interpolate_two_keyframes,
            start_keyframe=np.array([0, 0, 0]),
            end_keyframe=np.array([0, 0, 1]),
            step_size=-1
        )

    def test_generate_keyframes(self):
        self.assertEqual(
            len(
                interpolator._interpolate_two_keyframes(
                    start_keyframe=np.array([0, 0, 0]),
                    end_keyframe=np.array([0, 0, 0]),
                    step_size=1
                )
            ),
            1
        )
        self.assertEqual(
            len(
                interpolator._interpolate_two_keyframes(
                    start_keyframe=np.array([0, 0, 0]),
                    end_keyframe=np.array([0, 0, 1]),
                    step_size=1
                )
            ),
            2
        )
        self.assertEqual(
            len(
                interpolator._interpolate_two_keyframes(
                    start_keyframe=np.array([0, 0, 0]),
                    end_keyframe=np.array([0, 0, 2]),
                    step_size=1
                )
            ),
            3
        )
        self.assertEqual(
            len(
                interpolator._interpolate_two_keyframes(
                    start_keyframe=np.array([0, 0, 0]),
                    end_keyframe=np.array([0, 0, 1]),
                    step_size=0.4
                )
            ),
            4
        )

    def test_interpolating_points_match_stepsize(self):

        start_config = np.array([0, 0, 0])
        end_config = np.array([0, 0, 2])
        step_size = 1

        waypoints = interpolator._interpolate_two_keyframes(
            start_keyframe=start_config,
            end_keyframe=end_config,
            step_size=step_size
        )

        self.assertTrue(
            np.allclose(
                waypoints[0],
                start_config
            )
        )
        self.assertTrue(
            np.allclose(
                waypoints[1],
                np.array([0, 0, 1]),
            )
        )
        self.assertTrue(
            np.allclose(
                waypoints[2],
                end_config,
            )
        )

    def test_interpolating_more_complicated_points_match_stepsize(self):

        start_pose = np.array([0, 0, 0])
        end_pose = np.array([-45, 45, -180])
        step_size = 2

        waypoints = interpolator._interpolate_two_keyframes(
            start_keyframe=start_pose,
            end_keyframe=end_pose,
            step_size=step_size
        )

        for i in range(1, len(waypoints)-1):
            norm_between_last_two_poses = np.linalg.norm(waypoints[i]-waypoints[i-1])

            if i <= len(waypoints)-1:
                self.assertAlmostEqual(norm_between_last_two_poses, step_size)
            elif i == len(waypoints):
                self.assertLessEqual(
                    norm_between_last_two_poses - NUMERICAL_TOLERANCE,
                    step_size
                )
            else:
                self.assertFalse(True, "This shouldn't ever happen")

    def test_order_when_connecting_multiple_keyframes_locations(self):

        sets_of_poses = [
            (
                np.array([0, 0, 0]),
            ),
            (
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
            ),
            (
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
                np.array([45, -45, -90]),
                np.array([0, 180, -180])
            ),
            (
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
                np.array([45, -45, -90]),
                np.array([0, 180, -180]),
                np.array([1, 0, 0]),
                np.array([-44, 45, 90]),
                np.array([46, -45, -90]),
                np.array([1, 180, -180])
            ),
            (
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
            ),
        ]
        step_size = 2

        for poses in sets_of_poses:
            waypoints = interpolator.interpolate_keyframes(poses, step_size, is_degrees=True)

            num_poses = len(poses)
            in_order_pose_match_count = 0
            for i in range(len(waypoints)):

                pose_diff = utils.angle_diff_arrays(
                    waypoints[i],
                    poses[in_order_pose_match_count],
                    is_degrees=True
                )
                norm_of_diff_pose = np.linalg.norm(pose_diff)
                if np.isclose(norm_of_diff_pose, 0):
                    in_order_pose_match_count += 1

            self.assertEqual(num_poses, in_order_pose_match_count)

    def test_distance_between_keyframes_is_less_than_or_equal_to_the_step_size(self):

        sets_of_poses = [
            (
                np.array([0, 0, 0]),
            ),
            (
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
            ),
            (
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
                np.array([45, -45, -90]),
                np.array([0, 180, -180])
            ),
            (
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
                np.array([45, -45, -90]),
                np.array([0, 180, -180]),
                np.array([1, 0, 0]),
                np.array([-44, 45, 90]),
                np.array([46, -45, -90]),
                np.array([1, 180, -180])
            ),
            (
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
                np.array([0, 0, 0]),
                np.array([-45, 45, 90]),
            ),
        ]
        step_size = 2

        for poses in sets_of_poses:
            waypoints = interpolator.interpolate_keyframes(poses, step_size, is_degrees=True)

            for i in range(1, len(waypoints)-1):
                pose_diff = utils.angle_diff_arrays(
                    waypoints[i-1],
                    waypoints[i],
                    is_degrees=True
                )
                norm_between_last_two_poses = np.linalg.norm(pose_diff)
                self.assertLessEqual(
                    norm_between_last_two_poses - NUMERICAL_TOLERANCE,
                    step_size
                )

    def test_empty_keyframes_list(self):
        self.assertRaises(
            ValueError,
            interpolator.interpolate_keyframes,
            (),
            2
        )
