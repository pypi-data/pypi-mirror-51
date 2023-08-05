import numpy as np

from keyframe_tools.Mover import Mover
from keyframe_tools.Player import Player


class ActivityRunner:

    def __init__(
            self,
            *movements,
    ):
        self._movement_idx = 0
        self._movements = []

        self.append_movements(*movements)

    def append_movements(self, *movers):
        for m in movers:
            self._append_movement(m)

    def _append_movement(
            self,
            movement,
    ):
        if not isinstance(movement, Mover):
            raise ValueError()

        self._movements.append(
            movement
        )

    @property
    def is_finished(self):
        return (
                self._is_movement_finished
                and self._movement_idx + 1 >= len(self._movements)
        )

    @property
    def _is_movement_finished(self):
        return self._movements[self._movement_idx].is_finished

    def step(self):

        if len(self._movements) < 1:
            raise RuntimeError("Must have at least one movement to step")

        out = self._movements[self._movement_idx].step()
        if self._is_movement_finished:
            if not self.is_finished:
                self._movement_idx += 1
                self._movements[self._movement_idx].reset()
            out = self._movements[self._movement_idx].step()
        return out


if __name__ == '__main__':

    _names = ['joint1', 'joint2', 'joint3']
    _positions = np.array([
        [0, 0, 0],
        [0, 0, 2],
    ])
    _step_size = 1
    _num_movers = 3
    _activity_runner = ActivityRunner(
        *[Player(
            names=_names,
            positions=_positions,
            step_size=_step_size,
            is_move_forward_then_backwards=False,
        )] * _num_movers,
    )
    for i in range(_num_movers * (2+len(_positions))):
        _out = _activity_runner.step()
        print(_out)
