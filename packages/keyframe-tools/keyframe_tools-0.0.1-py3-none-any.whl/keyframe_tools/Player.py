import numpy as np

from keyframe_tools.Mover import Mover
from keyframe_tools import config


class Player(Mover):

    def __init__(
            self,
            names,
            positions,
            repetitions=1,
            is_move_forward_then_backwards=False,
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
        )

    def step(self):
        """
        Note that the first step steps into the 0th array
        :return:
        """
        self._index_looper.increment_index()
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

    _player = Player(
        _names,
        _positions,
        _repetitions,
        step_size=_step_size,
        is_move_forward_then_backwards=False,
        is_remove_unchanging_keyframe_indicies=True,
    )
    for _ in range(_repetitions * len(_positions)):
        _out = _player.step()
        print(_out)
